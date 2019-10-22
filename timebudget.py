"""Timebudget is a simple tool to help profile python programs.
Two main ways of using it

1) Use it as a function annotation:

from timebudget import timebudget

@timebudget  # times how long we spend in this function
def my_possibly_slow_function(*args):
    # Do something

timebudget.report()  # prints a summary of all annotated functions

OR
2) Surround specific code blocks using with like:

from timebudget import timebudget

with timebudget("load-file"):
    text = open(filename,'rt').readlines()


If you are doing something repeatedly you can get percent times in report like;

timebudget.report('process_record')

Assumes everything else is inside process_record() and displays accordingly.
"""
import atexit
from collections import defaultdict
from functools import wraps
import time
from typing import Union, Callable

__all__ = [
    'timebudget', 
    'annotate', 
    'report', 
    'recorder', 
    'TimeBudgetRecorder', 
    'timeblock',
]

class TimeBudgetRecorder():
    """The object that stores times used for different things and generates reports.
    This is mostly used through annotation and with-block helpers.
    """

    def __init__(self):
        self.start_times = {}
        self.elapsed_total = defaultdict(float)  # float defaults to 0
        self.elapsed_cnt = defaultdict(int)  # int defaults to 0

    def start(self, block_name:str):
        assert block_name not in self.start_times, f"timebudget.start({block_name}) without end"
        self.start_times[block_name] = time.time()

    def end(self, block_name:str, display:bool=False) -> float:
        """Returns number of ms spent in this block this time.
        """
        assert block_name in self.start_times, f"timebudget.end({block_name}) without start"
        elapsed = 1000*(time.time() - self.start_times[block_name])
        self.elapsed_total[block_name] += elapsed
        self.elapsed_cnt[block_name] += 1
        del self.start_times[block_name]
        if display:
            print("Spent {elapsed:.2f}ms in {block_name}")
        return elapsed

    def report(self, percent_of:str=None):
        """Prints a report summarizing all the times recorded by timebudget.
        If percent_of is specified, then times are shown as a percent of that function.
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
            assert percent_of in self.elapsed_cnt, f"Invalid block_name for percent_of {percent_of}"
            print(f"timebudget report per {percent_of} cycle...")
            total_elapsed = self.elapsed_total[percent_of]
            total_cnt = self.elapsed_cnt[percent_of]
            for res in results:
                avg = res['total'] / total_cnt
                pct = 100.0 * res['total'] / total_elapsed
                avg_cnt = res['cnt'] / total_cnt
                print(f"{res['name']:>25s}:{pct: 6.1f}% {avg: 8.2f}ms/cyc @{avg_cnt: 8.1f}execs/cyc")
        else:
            print("timebudget report...")
            for res in results:
                print(f"{res['name']:>25}:{res['avg']: 8.2f}ms for {res['cnt']: 6d} execs")


_singleton = TimeBudgetRecorder()  

def annotate(func):
    """Annotates a function or code-block to record how long the execution takes.
    Print summary with timebudget.report
    """
    name = func.__name__
    @wraps(func)
    def inner(*args, **kwargs):
        _singleton.start(name)
        try:
            return func(*args, **kwargs)
        finally:
            _singleton.end(name)
    return inner

class timeblock():
    """Surround a code-block with a timer as in
        with timeblock('loadfile'):
    """

    def __init__(self, name:str, recorder:TimeBudgetRecorder):
        self.name = name
        if recorder:
            self.recorder = recorder
        else:
            self.recorder = _singleton

    def __enter__(self):
        self.recorder.start(self.name)

    def __exit__(self, typ, val, trace):
        self.recorder.end(self.name)

def annotate_or_with_block(func_or_name:Union[Callable, str]):
    if callable(func_or_name):
        return annotate(func_or_name)
    if isinstance(func_or_name, str):
        return timeblock(func_or_name, _singleton)
    raise RuntimeError("Don't know what to do. Either annotate or with-block")

# Create shortcuts for export
recorder = _singleton
report = _singleton.report
timebudget = annotate_or_with_block
timebudget.report = report
timebudget.__doc__ = __doc__

def report_atexit(block_name:str=None):
    if block_name:
        atexit.register(lambda: report(block_name))
    else:
        atexit.register(report)

timebudget.report_atexit = report_atexit

