"""Timebudget is a stupidly-simple tool to help measure speed. 
Two main ways to use:

1) Put code to measure in a with statement:

with timebudget("load file"):
    text = open(filename,'rt').readlines()

2) Annotate any function to measure how long it takes

from timebudget import timebudget

@timebudget  # times how long we spend in this function
def my_possibly_slow_function(*args):
    # Do something

By default it prints time measurements immediately. Or:
timebudget.set_quiet()  # Sets `quiet=True` as global default
timebudget.report()  # prints a summary of all annotated functions
"""
import atexit
from collections import defaultdict
from functools import wraps
import sys
import time
from typing import Callable, Optional, Union
import warnings

__all__ = [
    'timebudget', 
    'annotate', 
    'report', 
    'set_quiet',
]

def ms_format(milliseconds:float) -> str:
    """Slightly smart formating of an elapsed time
    """
    assert milliseconds >= 0
    if milliseconds < 1:
        return f"{milliseconds:.3f}ms"
    if milliseconds < 1000:
        return f"{milliseconds:.2f}ms"
    return f"{(milliseconds/1000):.3f}sec"


class TimeBudgetRecorder():
    """The object that stores times used for different things and generates reports.
    This is mostly used through annotation and with-block helpers.
    """

    def __init__(self, quiet_mode:bool=False):
        self.quiet_mode = quiet_mode
        self.reset()
        self.out_stream = sys.stdout

    def reset(self):
        """Clear all stats collected so far.
        """
        self.start_times = {}
        self.elapsed_total = defaultdict(float)  # float defaults to 0
        self.elapsed_cnt = defaultdict(int)  # int defaults to 0

    def _print(self, msg:str):
        self.out_stream.write(msg)
        self.out_stream.write("\n")
        self.out_stream.flush()

    def start(self, block_name:str):
        if block_name in self.start_times:
            # End should clear out the record, so something odd has happened here.
            # try/finally should prevent this, but sometimes it doesn't.
            warnings.warn(f"timebudget is confused: timebudget.start({block_name}) without end")
        self.start_times[block_name] = time.time()

    def end(self, block_name:str, quiet:Optional[bool]=None) -> float:
        """Returns number of ms spent in this block this time.
        """
        if quiet is None:
            quiet = self.quiet_mode
        if block_name not in self.start_times:
            warnings.warn(f"timebudget is confused: timebudget.end({block_name}) without start")
            return float('NaN')
        elapsed = 1000*(time.time() - self.start_times[block_name])
        self.elapsed_total[block_name] += elapsed
        self.elapsed_cnt[block_name] += 1
        del self.start_times[block_name]
        if not quiet:
            self._print(f"{block_name} took {ms_format(elapsed)}")
        return elapsed

    def report(self, percent_of:str=None, reset:bool=False):
        """Prints a report summarizing all the times recorded by timebudget.
        If percent_of is specified, then times are shown as a percent of that function.
        If `reset` is set, then all stats will be cleared after this report.
        """
        results = []
        for name, cnt in self.elapsed_cnt.items():
            total = self.elapsed_total[name]
            results.append({
                'name': name,
                'total': total,
                'cnt': cnt,
                'avg': total / cnt,
            })
        results = sorted(results, key=lambda r: r['total'], reverse=True)
        if percent_of:
            assert percent_of in self.elapsed_cnt, f"Can't generate report for unrecognized block {percent_of}"
            self._print(f"timebudget report per {percent_of} cycle...")
            total_elapsed = self.elapsed_total[percent_of]
            total_cnt = self.elapsed_cnt[percent_of]
            for res in results:
                avg = res['total'] / total_cnt
                pct = 100.0 * res['total'] / total_elapsed
                avg_cnt = res['cnt'] / total_cnt
                self._print(f"{res['name']:>25s}:{pct: 6.1f}% {avg: 8.2f}ms/cyc @{avg_cnt: 8.1f} calls/cyc")
        else:
            self._print("timebudget report...")
            for res in results:
                self._print(f"{res['name']:>25}:{res['avg']: 8.2f}ms for {res['cnt']: 6d} calls")
        if reset:
            self.reset()


_default_recorder = TimeBudgetRecorder()  


def annotate(func:Callable, quiet:Optional[bool]):
    """Annotates a function or code-block to record how long the execution takes.
    Print summary with timebudget.report
    """
    name = func.__name__
    @wraps(func)
    def inner(*args, **kwargs):
        _default_recorder.start(name)
        try:
            return func(*args, **kwargs)
        finally:
            _default_recorder.end(name, quiet)
    return inner

class _timeblock():
    """Surround a code-block with a timer as in
        with timebudget('loadfile'):
    """

    def __init__(self, name:str, quiet:Optional[bool]):
        self.name = name
        self.quiet = quiet

    def __enter__(self):
        _default_recorder.start(self.name)

    def __exit__(self, typ, val, trace):
        _default_recorder.end(self.name, self.quiet)


def annotate_or_with_block(func_or_name:Union[Callable, str], quiet:Optional[bool]=None):
    if callable(func_or_name):
        return annotate(func_or_name, quiet)
    if isinstance(func_or_name, str):
        return _timeblock(func_or_name, quiet)
    raise RuntimeError("timebudget: Don't know what to do. Either @annotate or with:block")


def set_quiet(quiet:bool=True):
    """Tell timebudget not to print time measurements on every call, but instead
    to save them only for a report.  
    Alternately, you can reverse this by calling set_quiet(False).
    """
    _default_recorder.quiet_mode = quiet


# Create shortcuts for export
timebudget = annotate_or_with_block
report = _default_recorder.report
timebudget.report = report
timebudget.__doc__ = __doc__
timebudget.set_quiet = set_quiet
timebudget._default_recorder = _default_recorder

def report_at_exit(block_name:str=None):
    if block_name:
        atexit.register(lambda: report(block_name))
    else:
        atexit.register(report)

timebudget.report_at_exit = report_at_exit
timebudget.report_atexit = report_at_exit  # for backwards compat with v0.6

