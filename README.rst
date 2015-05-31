ENT in Python
#############

:date: 2015-05-31
:author: Roland Smith

.. Last modified: 2015-05-31 13:30:52 +0200


Introduction
============

This is a partial Python_ port of the ent_ program by John "Random" Walker.

.. _Python: http://www.python.org
.. _ent: http://www.fourmilab.ch/random/

It started out as a straight translation. But over time I replaced some of the
algorithms by more Pythonic ones. The latest modification was to use numpy_ for
handling the data. The fact that operators on numpy arrays act by element
makes the algorithms simpler.

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
Currently, the script doesn't handle options, so the following are not
implemented;

* handling input as bits,
* printing occurrence counts,
* folding upper/lowercase and
* terse output.

While terse output and occurrence counts might be implemented, the remaining will
not be implemented.
