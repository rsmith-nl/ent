ENT in Python
#############

:date: 2015-05-31
:author: Roland Smith

.. Last modified: 2015-05-31 15:38:44 +0200


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

Development is done on Python 3, but this program has been tested to work on
both Python 2.7 and Python 3.4.


Status
======

Implemented are the calculation of:

* entropy.
* arithmetic mean,
* χ² distribution and
* serial correlation coefficient.

Not implemented are the calculation of;

* Monte Carlo value for π and
* optimum compression.

The output format is different and more organized to handle multiple files.

.. code-block:: console

    > python ent.py test/random.dat
    File "test/random.dat"
    - Entropy is 7.999982 bits per byte.
    - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
    - χ² distribution for 10485760 samples is 259.03, and randomly
    would exceed this value 43.53 percent of the times.
    According to the χ² test, this sequence looks random.
    - Serial correlation coefficient is -0.000289 (totally uncorrelated = 0.0).

Next to normal text output, terse output is also implemented.

.. code-block:: console

    > python ent.py -t test/random.dat
    0,File-name,File-bytes,Entropy,Chi-square,Mean,Serial-Correlation
    1,test/random.dat,10485760,7.999982,259.03,127.5116,-0.000289

The following are not implemented;

* handling input as bits,
* printing occurrence counts,
* folding upper/lowercase.

While occurrence counts might be implemented, the remaining will
likely not be implemented.
