ENT in Python
#############

:date: 2017-02-18
:author: Roland Smith

.. Last modified: 2022-12-27T18:13:28+0100

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Introduction
============

This is a partial Python_ port of the ent_ program by John "Random" Walker.
My motivation for doing this is basically as a learning experience about
randomness and algorithms.

.. _Python: http://www.python.org
.. _ent: http://www.fourmilab.ch/random/

It started out as a straight translation. But over time I replaced some of the
algorithms by more Pythonic ones. The latest refactoring was to use numpy_ for
handling the data. The fact that operators on numpy arrays act by element
makes the algorithms simpler and more elegant.

.. _numpy: http://www.numpy.org/

A version that not requires numpy_ is contained in ``ent_without_numpy.py``.
It gives the same output, but is a lot slower.

Development is done on Python 3.9+.


Status
======

Implemented are the calculation of:

* entropy.
* optimum compression,
* arithmetic mean,
* χ² distribution,
* Monte Carlo value for π and
* serial correlation coefficient.

The output format is slightly different.

.. code-block:: console

    > python3 ent.py test/random.dat
    - Entropy is 7.999982 bits per byte.
    - χ² distribution for 10485760 samples is 259.03, and randomly
      would exceed this value 41.80 percent of the times.
      According to the χ² test, this sequence looks random.
    - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
    - Monte Carlo value for π is 3.139877754 (error 0.05 %).
    - Serial correlation coefficient is -0.000296 (totally uncorrelated = 0.0).


Next to normal text output, terse output is also implemented.

.. code-block:: console

    > python3 ent.py -t test/random.dat
    0,File-bytes,Entropy,Chi-square,Mean,Monte-Carlo-Pi,Serial-Correlation
    1,10485760,7.999982,259.031104,127.511638,3.139878,-0.000296

The following will not be implemented;

* handling input as bits,
* printing occurrence counts,
* folding upper/lowercase.

Versions
========

This repository contains different versions of ``ent``:

* ``ent.py`` uses ``numpy``. This is the original and currently the fastest version.
  On my machine, it runs within 0.4 second on ``test/random.dat``.
* ``ent_without_numpy.py`` only uses modules from the standard library.
  This is approximately a factor of 9.5 slower than the numpy version.
* A Makefile is provided that compiled ``ent_without_numpy.py`` with ``cython``.
  (written for CPython 3.9 on UNIX) This is approximately 7× slower than
  the numpy version.
* ``ent_decimal.py`` used ``Decimal`` numbers. Approximately 38× slower than
  the numpy version.


Testing
=======

This program comes with a test suite, which requires py.test.
To run the tests, use the command::

    py.test -v test/*.py

Example output::

  ========================================== test session starts ==========================================
  platform freebsd13 - Python 3.9.16, pytest-7.1.3, pluggy-1.0.0 - /usr/local/bin/python3.9
  cachedir: .pytest_cache
  rootdir: /zstorage/home/rsmith/src/progs/ent
  plugins: pylama-7.7.1, black-0.3.12
  collected 12 items

  test/test-numpy.py::test_size PASSED                                                              [  8%]
  test/test-numpy.py::test_mean PASSED                                                              [ 16%]
  test/test-numpy.py::test_entropy PASSED                                                           [ 25%]
  test/test-numpy.py::test_chisquare PASSED                                                         [ 33%]
  test/test-numpy.py::test_correlation PASSED                                                       [ 41%]
  test/test-numpy.py::test_mc PASSED                                                                [ 50%]
  test/test-without-numpy.py::test_size PASSED                                                      [ 58%]
  test/test-without-numpy.py::test_mean PASSED                                                      [ 66%]
  test/test-without-numpy.py::test_entropy PASSED                                                   [ 75%]
  test/test-without-numpy.py::test_chisquare PASSED                                                 [ 83%]
  test/test-without-numpy.py::test_correlation PASSED                                               [ 91%]
  test/test-without-numpy.py::test_mc PASSED                                                        [100%]

  ========================================== 12 passed in 7.87s ===========================================
