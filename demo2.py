import time
from timebudget import timebudget

with timebudget('load-file'):
    readme = open('README.md','rt').read()

timebudget.report()
