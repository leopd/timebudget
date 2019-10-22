# timebudget
### A simple tool to see what's slow in your python program

Trying to figure out where the time's going in your python code?  Tired of writing `elapsed = time.time() - start_time`?  You can find out with just a few lines of code after you

```
pip install timebudget
```

## The simplest way

```python
from timebudget import timebudget
timebudget.report_atexit()  # Generate report when the program exits

@timebudget  # Measure how long this function takes
def possibly_slow():
    ...

@timebudget  # ... and this function too
def should_be_fast():
    ...
```

And now when you run your program, you'll see how much time was spent in each annotated function:

```
timebudget report...
            possibly_slow:  600.62ms for      3 execs
           should_be_fast:  300.35ms for      2 execs
```


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


## Requirements

Needs Python 3.6 or higher.  Because type annotations are awesome, and it's 2019, and python 2.7 is on its deathbed.

Tests require `pytest`.

## Inspiration

This tool is inspired by [TQDM](https://github.com/tqdm/tqdm), the awesome progress bar.  TQDM is stupidly simple to add to your code, and just makes it better.  I aspire to imitate that.

