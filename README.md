# timebudget
### A simple tool to see what's slow in your python program

Trying to figure out where the time's going in your python code?  Tired of writing `elapsed = time.time() - start_time`?  Just add a few lines of code to find out.

## The simplest way

```python
from timebudget import timebudget
timebudget.report_atexit()

@timebudget
def possibly_slow():
    ...

@timebudget
def should_be_fast():
    ...
```

And now when you run your program, you'll see how much time was spent in each annotated function:

```
timebudget report...
            possibly_slow:  600.62ms for      3 execs
           should_be_fast:  300.35ms for      2 execs
```

See e.g. [demo1.py](demo1.py).

## More advanced useage

You can wrap specific blocks of code to be measured, and give them a name:

```python
with timebudget("load-file"):
    text = open(filename,'rt').readlines()
```

And you can pick when to print the report instead of doing it `atexit`:

```python
timebudget.report()
```

See e.g. [demo2.py](demo2.py).

## Percent of time in a loop

If you are doing something repeatedly, and want to know the percent of time doing different things, time the loop itself, and pass the name to report:

```python
@timebudget
def outer_loop():
    possibly_slow()
    should_be_fast()
    should_be_fast()
    
timebudget.report('outer_loop')
```

Then the report looks like:

```
timebudget report per outer_loop cycle...
               outer_loop: 100.0%   440.79ms/cyc @     1.0execs/cyc
            possibly_slow:  40.9%   180.31ms/cyc @     3.0execs/cyc
           should_be_fast:  13.7%    60.19ms/cyc @     2.0execs/cyc
```

See e.g. [demo3.py](demo3.py).

## Requirements

Needs Python 3.6 or higher.  Because it's 2019, and python 2.7 is on its deathbed.

## Inspiration

This tool is inspired by [TQDM](https://github.com/tqdm/tqdm), the awesome progress bar.  TQDM is stupidly simple to add to your code, and just makes it better.  I aspire to imitate that.

