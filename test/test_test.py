import core

def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4

def test_ghp():
  assert core.groupToHiPoly.toHiPolyName("dd_lo") == "dd_hi"
