import io
import pytest
import time

from timebudget import timebudget

def test_default_print_immediate():
    stream = io.StringIO()
    timebudget._default_recorder.out_stream = stream
    assert len(stream.getvalue()) == 0
    with timebudget("nothing much"):
        time.sleep(0.01)
    out = stream.getvalue()
    assert len(out) > 0, "Default timebudget didn't print"
    assert "much" in out


def test_disable_print_immediate():
    stream = io.StringIO()
    timebudget._default_recorder.out_stream = stream
    assert len(stream.getvalue()) == 0
    with timebudget("nothing much", quiet=True):
        time.sleep(0.01)
    out = stream.getvalue()
    assert len(out) == 0, "Failed to disable immediate printing"


def test_disable_print_globally():
    stream = io.StringIO()
    timebudget._default_recorder.out_stream = stream
    timebudget.set_quiet()
    assert len(stream.getvalue()) == 0
    with timebudget("nothing much"):
        time.sleep(0.01)
    out = stream.getvalue()
    assert len(out) == 0, "Failed to disable immediate printing"
    timebudget.set_quiet(False)


def test_ms_formatting():
    stream = io.StringIO()
    timebudget._default_recorder.out_stream = stream
    assert len(stream.getvalue()) == 0
    with timebudget("really fast"):
        time.sleep(0.001)
    out = stream.getvalue()
    assert "ms" in out, "Short time output did not get formatted in milliseconds"


def test_sec_formatting():
    stream = io.StringIO()
    timebudget._default_recorder.out_stream = stream
    assert len(stream.getvalue()) == 0
    with timebudget("slow"):
        time.sleep(1.1)
    out = stream.getvalue()
    assert "sec" in out, "Long time output did not get formatted in seconds"
    assert "ms" not in out


def test_data():
    timebudget.reset()
    with timebudget("fast"):
        time.sleep(0.01)
    with timebudget("slow"):
        time.sleep(0.1)
    d = timebudget.data()
    assert d['fast']['avg'] < d['slow']['avg']
