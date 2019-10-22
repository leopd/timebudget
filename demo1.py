import time
from timebudget import timebudget
timebudget.report_atexit()

@timebudget
def possibly_slow():
    print("slow")
    time.sleep(0.6)

@timebudget
def should_be_fast():
    print("quick")
    time.sleep(0.3)


possibly_slow()
possibly_slow()
should_be_fast()
should_be_fast()
possibly_slow()
