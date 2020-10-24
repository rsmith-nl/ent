ENT in Python
#############

:date: 2017-02-18
:author: Roland Smith

.. Last modified: 2020-10-24T11:37:11+0200


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

The following are not implemented;

* handling input as bits,
* printing occurrence counts,
* folding upper/lowercase.

While occurrence counts might be implemented, the remaining will
likely not be implemented.


Testing
=======

This program comes with a test suite, which requires py.test.
To run the tests, use the command::

    py.test -v test/

Example output::

    ========================================== test session starts ==========================================
    platform freebsd12 -- Python 3.9.0, pytest-4.5.0, py-1.9.0, pluggy-0.13.1 -- /usr/local/bin/python3.9
    cachedir: .pytest_cache
    rootdir: /home/rsmith/src/progs/ent
    plugins: pylama-7.7.1
    collected 6 items

    test/test_routines.py::test_size PASSED                                                           [ 16%]
    test/test_routines.py::test_mean PASSED                                                           [ 33%]
    test/test_routines.py::test_entropy PASSED                                                        [ 50%]
    test/test_routines.py::test_chisquare PASSED                                                      [ 66%]
    test/test_routines.py::test_correlation PASSED                                                    [ 83%]
    test/test_routines.py::test_mc PASSED                                                             [100%]

    ======================================= 6 passed in 0.29 seconds ========================================
