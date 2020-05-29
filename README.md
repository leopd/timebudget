# timebudget
### A stupidly-simple tool to see where your time is going in Python programs

Trying to figure out where the time's going in your python code?  Tired of writing `elapsed = time.time() - start_time`?  You can find out with just a few lines of code after you

```
pip install timebudget
```

## The simplest way

With just two lines of code (one is the import), you can see how long something takes...

```python
from timebudget import timebudget

with timebudget("Loading and processing the file"):
    raw = open(filename,'rt').readlines()
    lines = [line.rstrip() for line in raw]
```

will print

```
Loading and processing the file took 1.453sec
```


## Record times and print a report

To get a report on the total time from functions you care about, just annotate those functions:

```python
from timebudget import timebudget
timebudget.set_quiet()  # don't show measurements as they happen
timebudget.report_at_exit()  # Generate report when the program exits

@timebudget  # Record how long this function takes
def possibly_slow():
    ...

@timebudget  # ... and this function too
def should_be_fast():
    ...
```

And now when you run your program, you'll see how much time was spent in each annotated function:

```
timebudget report...
            possibly_slow:  901.12ms for      3 calls
           should_be_fast:   61.35ms for      2 calls
```

Or instead of calling `report_at_exit()` you can manually call 

```python
timebudget.report(reset=True)  # print out the report now, and reset the statistics
```

If you don't set `reset=True` then the statistics will accumulate into the next report.

You can also wrap specific blocks of code to be recorded in the report, and optionally override
the default `set_quiet` choice for any block:

```python
with timebudget("load-file", quiet=False):
    text = open(filename,'rt').readlines()
```


## Percent of time in a loop

If you are doing something repeatedly, and want to know the percent of time doing different things, time the loop itself, and pass the name to report.  That is, add a timebudget annotation or wrapper onto the thing which is happening repeatedly.  Each time this method or code-block is entered will now be considered one "cycle" and your report will tell you what fraction of time things take within this cycle.


```python
@timebudget
def outer_loop():
    if sometimes():
        possibly_slow()
    should_be_fast()
    should_be_fast()

for _ in range(NUM_CYCLES):
    outer_loop()
    
timebudget.report('outer_loop')
```

Then the report looks like:

```
timebudget report per outer_loop cycle...
               outer_loop: 100.0%   440.79ms/cyc @     1.0 calls/cyc
            possibly_slow:  40.9%   180.31ms/cyc @     0.6 calls/cyc
           should_be_fast:  13.7%    60.19ms/cyc @     2.0 calls/cyc
```

Here, the times in milliseconds are the totals (averages per cycle), not the average time per call.  So in the above example, `should_be_fast` is taking about 30ms per call, but being called twice per loop.  Similarly, `possibly_slow` is still about 300ms each time it's called, but it's only getting called on 60% of the cycles on average, so on average it's using 41% of the time in `outer_loop` or 180ms.


## Requirements

Needs Python 3.6 or higher.  Other libraries are in `requirements.txt` and can be installed like

```
pip install -r requirements.txt  # only needed for developing timebudget.
```

## Testing

To run tests:

```
pytest
```

## Inspiration

This tool is inspired by [TQDM](https://github.com/tqdm/tqdm), the awesome progress bar.  TQDM is stupidly simple to add to your code, and just makes it better.  I aspire to imitate that.

