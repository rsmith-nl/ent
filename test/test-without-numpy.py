# file: test_routines.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2017-02-26 23:08:58 +0100
# Last modified: 2020-10-24T11:49:35+0200
"""Test routines from ent.py by comparing the results from a known batch of
random data to the results given by John Walker's ent.

Use “pytest-3.6 -v test/test_routines.py” from the main directory to run these
tests.
"""

import statistics as stat
import sys

sys.path.insert(1, ".")


from ent_without_numpy import readdata, entropy, pearsonchisquare, correlation, monte_carlo  # noqa

goodtxt = """0,File-bytes,Entropy,Chi-square,Mean,Monte-Carlo-Pi,Serial-Correlation
1,10485760,7.999982,259.031104,127.511638,3.139878,-0.000296"""
items = goodtxt.replace("\n", ",").split(",")
good = {j: float(k) for j, k in zip(items[1:7], items[8:])}

data, counts = readdata("test/random.dat")


def test_size():
    assert len(data) == good["File-bytes"]


def test_mean():
    e = good["Mean"]
    d = 0.00001
    assert (e - d) < stat.mean(data) < (e + d)


def test_entropy():
    e = good["Entropy"]
    d = 0.00001
    assert (e - d) < entropy(counts) < (e + d)


def test_chisquare():
    e = good["Chi-square"]
    d = 0.00001
    assert (e - d) < pearsonchisquare(counts) < (e + d)


def test_correlation():
    e = good["Serial-Correlation"]
    d = 0.000001
    assert (e - d) < correlation(data) < (e + d)


def test_mc():
    e = good["Monte-Carlo-Pi"]
    d = 0.001
    assert (e - d) < monte_carlo(data) < (e + d)
