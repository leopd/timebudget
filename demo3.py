import random
import time
from timebudget import timebudget

# More or less what's in the README for loops
# but 10x faster so we can test it 100x and get the averages about right.

@timebudget
def possibly_slow():
    time.sleep(0.03)

def sometimes():
    return random.random() < 0.6

@timebudget
def should_be_fast():
    time.sleep(0.003)

@timebudget
def outer_loop():
    if sometimes():
        possibly_slow()
    should_be_fast()
    should_be_fast()

for n in range(100):
    outer_loop()

timebudget.report('outer_loop')
