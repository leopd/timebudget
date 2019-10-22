import time
from timebudget import timebudget

@timebudget
def possibly_slow():
    print('slow', end=' ', flush=True)
    time.sleep(0.06)

@timebudget
def should_be_fast():
    print('quick', end=' ', flush=True)
    time.sleep(0.03)

@timebudget
def outer_loop():
    possibly_slow()
    possibly_slow()
    should_be_fast()
    should_be_fast()
    possibly_slow()
    time.sleep(0.2)
    print("dance!")

for n in range(7):
    outer_loop()

timebudget.report('outer_loop')
