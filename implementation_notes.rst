Implementation notes for ent
############################

:date: 2015-05-31
:author: Roland Smith

.. Last modified: 2022-01-30T20:21:43+0100

Reading the data
================

With numpy
++++++++++

The fastest way to read bytes with numpy is to use ``fromfile``;

.. code-block:: python

    import numpy as np
    data = np.fromfile(name, np.ubyte)

Next we use ``bincounts`` to get the occurrence of every byte value.

.. code-block:: python

    counts = np.bincount(data)

An example (with random data);

.. code-block:: python

    In [1]: import numpy as np

    In [2]: import os

    In [3]: import math

    In [4]: data = np.array([i for i in os.urandom(100)], np.ubyte)
    Out[4]: 
    array([204, 248, 187,  20, 188, 252, 108,  29,  28,  53, 171, 203,  67,
        189,  73,  42, 158,  16, 175, 117,  19,   1,  19,  86, 226,  24,
            47,  24,  19, 246,  38, 148, 185, 146, 117, 154,  53,  78, 203,
            59, 235,  98, 139, 231,  81, 102, 202, 150, 206, 158, 241,  29,
            2, 123, 232, 245,  37, 125, 189, 116,   7, 226, 210,  12,  56,
            56, 168, 126,  65, 212, 233, 212,  95, 164,  51, 251, 109,  79,
            40,  53, 106,  32,  18, 154,  66,  92, 172, 239, 143, 177, 178,
            71, 214,  51, 130, 248,  25,  56, 249,  46], dtype=uint8)

    In [5]: counts = np.bincount(data)
    Out[5]: 
    array([0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 3, 1, 0,
        0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0,
        0, 0, 1, 1, 0, 0, 0, 2, 0, 3, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 1,
        1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1,
        0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0,
        2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1,
        0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 2, 1, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1,
        0, 0, 0, 1, 1, 0, 2, 1, 0, 1, 1])

Without numpy
+++++++++++++

We read the file in binary mode and use ``collections.Counter``.

.. code-block:: python

    def readdata(name):
        """
        Read the data from a file and count byte occurences.

        Arguments:
            name: Path of the file to read

        Returns:
            data: file contents as bytes.
            cnts: list containing the occurance count of each byte value 0−255.
        """
        with open(name, "rb") as inf:
            data = inf.read()
        cnts = collections.Counter(data).values()
        return data, cnts


Entropy calculation
===================

We want to calculate the entropy of a stream of unsigned bytes. Every byte can
have 256 different values. The definition of entropy in this context is;

Η = - Σ P(i)·log₂₅₆(P(i))

where i is every possible byte value.

If the log₂₅₆ cannot be calculated directly, we can use log(P(i))/log(256)
instead. Since we cannot take the logarithm of 0, we remove all 0 counts, and
we convert counts to relative frequencies.


With numpy
++++++++++

.. code-block:: python

    counts = np.trim_zeros(np.sort(counts))
    sz = sum(counts)
    p = counts/sz

An example;

.. code-block:: python

    In [5]: counts = np.bincount(data)
    Out[5]: 
    array([0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 3, 1, 0,
        0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0,
        0, 0, 1, 1, 0, 0, 0, 2, 0, 3, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 1,
        1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1,
        0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0,
        2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1,
        0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 2, 1, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1,
        0, 0, 0, 1, 1, 0, 2, 1, 0, 1, 1])

    In [6]: counts = np.trim_zeros(np.sort(counts))
    Out[6]: 
    array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3])

    In [7]: sz = sum(counts)
    Out[7]: 100

    In [8]: p = counts/sz
    Out[8]: 
    array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
        0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
        0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
        0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
        0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
        0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
        0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
        0.02, 0.02, 0.02, 0.03, 0.03, 0.03])

With numpy, calculating the sum is easy because operators work element-wise on
arrays. The result is multiplied by 8 because we want to express entropy as
bits per byte.

.. code-block:: python

    In [9]: ent = -sum(p * np.log(p)/math.log(256))*8
    Out[9]: 6.281209564709828


Without numpy
+++++++++++++

We use a list comprehension and a generator expressions instead.

.. code-block:: python

    def entropy(counts):
        """
        Calculate the entropy of the data represented by the counts array.

        Arguments:
            counts: list containing the occurance of each byte value 0−255.

        Returns:
            Entropy in bits per byte.
        """
        sz = sum(counts)
        p = [n / sz for n in counts]
        c = math.log(256)
        ent = -sum(n * math.log(n) / c for n in p)
        return ent * 8



Calculating the χ² value
========================

The calculation given on the `wikipedia page`_ can be easily converted into
Python.

.. _wikipedia page: http://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test#Calculating_the_test-statistic

With numpy
++++++++++

.. code-block:: python

    def pearsonchisquare(counts):
        np = sum(counts)/256
        return sum((counts - np)**2/np)

Without numpy
+++++++++++++

.. code-block:: python

    def pearsonchisquare(counts):
        """
        Calculate Pearson's χ² (chi square) test for an array of bytes.

        See [http://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
        #Discrete_uniform_distribution]

        Arguments:
            counts: list containing the occurance of each byte value 0−255.

        Returns:
            χ² value
        """
        np = sum(counts) / 256
        return sum((c - np) ** 2 / np for c in counts)


Calculating the serial correlation coefficient
==============================================

With numpy
++++++++++

The code for this calculation was written after tracing the execution of the
calculation in the original C code from the file ``randtest.c``.  The
calculation in that file uses the following variables ``sccfirst``, ``scc``,
``sccun``, ``sccu0``, ``scclast``, ``scct1``, ``scct2`` and ``scct3``.

The variable ``sccfirst`` is only used to detect the first iteration, so we
will not follow it. But for the other variables we will trace the values of
the variables when dealing with a four-byte input 2 ,17, 5, 9.

In the following table, ‘-’ indicates that no value is set. Every line is the
content of the variables at the *end* of a cycle.

The variable ``sccu0`` contains the first byte: 2, while ``totalc`` contains
the amount of bytes processed which is 4, at the end of this sequence.

=====   =====================   =============   =================   =======
sccun   scct1                   scct2           scct3               scclast
=====   =====================   =============   =================   =======
-       0                       0               0                   -
2       0                       2               2*2                 2
17      2*17                    2+17            2*2+17*17           17
5       2*17+17*5               2+17+5          2*2+17*17+5*5       5
9       2*17+17*5+5*9           2+17+5+9        2*2+17*17+5*5+9*9   9
-       2*17+17*5+5*9+9*2       (2+17+5+9)**2   2*2+17*17+5*5+9*9   9
-----   ---------------------   -------------   -----------------   -------
res.    182                     1089            399                 -
=====   =====================   =============   =================   =======

From the standpoint of implementing this in Python (with numpy arrays) we see
that ``scct1`` is the sum of the product of two arrays where the second array
is a copy of the first one rolled left by one.

.. code-block:: python

    In [1]: import numpy as np

    In [2]: data = np.array([2 ,17, 5, 9], np.ubyte);

    In [3]: a = np.array(data, np.float64)
    Out[3]: array([ 2., 17.,  5.,  9.])

    In [4]: b = np.roll(a, -1)
    Out[4]: array([17.,  5.,  9.,  2.])

    In [5]: a*b
    Out[5]: array([34., 85., 45., 18.])

    In [6]: sum(a*b)
    Out[6]: 182.0


The calculation for ``scct2`` is easier, just sum the elements and square the
sum;

.. code-block:: python

    In [10]: np.sum(a)**2
    Out[10]: 1089

And ``scct3`` is simply the sum of the squares;

.. code-block:: python

    In [11]: np.sum(a*a)
    Out[11]: 399

We now calculate ``scc``::

    scc = totalc * scct3 - scct2
    scc = 4 * 399 - 1089 = 507

Since this value is not zero, we continue::

    scc = (totalc * scct1 - scct2) / scc
    scc = (4 * 182 - 1089) / 507 = -0.712

Without numpy
+++++++++++++

The code is basically a simple translation of the C code.


Implementation of poz()
=======================

Originally I used the algorithm from ``chisq.c``. After reading the wikipedia
page for the `normal distribution`_ I implemented the integration by parts of
the cumulative distribution function.

.. _normal distribution: http://en.wikipedia.org/wiki/Normal_distribution#Cumulative_distribution_function

The calculation for a given value ``z`` goes like this;

.. code-block:: python

    In [1]: import numpy as np

    In [2]: z = 1.3;

    In [3]: cnt = 40;

    In [4]: exp = np.array([2*i+1 for i in range(0, cnt+1)])
    Out[4]: 
    array([ 1,  3,  5,  7,  9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33,
        35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67,
        69, 71, 73, 75, 77, 79, 81])

    In [5]: za = np.ones(cnt+1)*z
    Out[5]: 
    array([1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3,
        1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3,
        1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3,
        1.3, 1.3])

    In [6]: num = np.power(za, exp)
    Out[6]: 
    array([1.30000000e+00, 2.19700000e+00, 3.71293000e+00, 6.27485170e+00,
        1.06044994e+01, 1.79216039e+01, 3.02875107e+01, 5.11858930e+01,
        8.65041592e+01, 1.46192029e+02, 2.47064529e+02, 4.17539054e+02,
        7.05641001e+02, 1.19253329e+03, 2.01538126e+03, 3.40599434e+03,
        5.75613043e+03, 9.72786043e+03, 1.64400841e+04, 2.77837422e+04,
        4.69545243e+04, 7.93531460e+04, 1.34106817e+05, 2.26640520e+05,
        3.83022479e+05, 6.47307990e+05, 1.09395050e+06, 1.84877635e+06,
        3.12443203e+06, 5.28029013e+06, 8.92369032e+06, 1.50810366e+07,
        2.54869519e+07, 4.30729488e+07, 7.27932834e+07, 1.23020649e+08,
        2.07904897e+08, 3.51359276e+08, 5.93797176e+08, 1.00351723e+09,
        1.69594411e+09])

    In [7]: denum = np.cumprod(exp)
    Out[7]: 
    array([                1,                    3,                   15,
                         105,                  945,                10395,
                      135135,              2027025,             34459425,
                   654729075,          13749310575,         316234143225,
               7905853580625,      213458046676875,     6190283353629375,
          191898783962510625,  6332659870762850625,   282166592185152483,
        -8006580162858909745,  1338022901564897417,  -481293256967860751,
        -2248865975908460677, -8965248547332972385,  2908431970669985073,
        -5060786026847144351,   154329662729360723,  8179472124656118319,
         7149109087057268761,  1670848340654183825,  6346331730049087595,
         -255390014906240641,  2357173134616391233,  5642301160389017217,
         9099296271873121219,   662144253120609167, -8327990249565403991,
          799266214140711985,  4604733839424744027,  4076368235223809375,
         8438441329618563153,   984216971850205601])

    In [8]: import math

    In [9]: 0.5+(np.sum(num/denum)/math.sqrt(2*math.pi))*math.exp(-(z*z)/2)
    Out[9]: 0.9031995158269118

Looking in the relevant table_, this is the correct answer.

.. _table: http://en.wikipedia.org/wiki/Standard_normal_table#Cumulative

After the Python 3.9 update, I used the ``cdf`` method from
``statistics.NormalDist``.


Calculating the Monte Carlo value for π
=======================================

This calculation creates an x and y coordinate out of three consecutive bytes
each. Suppose that ``d`` is an array of bytes, then the coordinates of the
first point would be calculated as follows by considering the bytes as
unsigned 8-bit integers.

.. code-block:: python

    montex = d[0]*256**2 + d[1]*256 + d[2]
    montey = d[3]*256**2 + d[4]*256 + d[5]
    dist2 = montex*montex + montey*montey

The square of the radius of the circle is given by:

.. code-block:: python

    incirc = (256**3 - 1)**2

If ``dist2`` is smaller than ``incirc``, the point is counted as being inside
the circle.

With numpy
++++++++++

.. code-block:: python

    In [1]: import os

    In [2]: import numpy as np

    In [3]: d = np.array(bytearray(os.urandom(24)), dtype=np.float64)
    Out[3]: 
    array([ 15., 240.,  20.,  97.,  97., 180., 231., 109., 160.,  98., 123.,
            37.,  21.,  80., 229., 132., 150., 160., 206.,  30., 138., 173.,
            29., 252.])

Combining three bytes into one number is done like this.

.. code-block:: python

    In [4]: values = np.sum(d.reshape((-1, 3))*np.array([256**2, 256, 1]), axis=1)
    Out[4]: 
    array([ 1044500.,  6382004., 15166880.,  6454053.,  1396965.,  8689312.,
        13508234., 11345404.])

Slicing the X and Y values and calculating the square of distance from the origin.

.. code-block:: python

    In [5]: montex, montey = values[0::2], values[1::2];

    In [6]: dist2 = montex * montex + montey * montey
    Out[6]: array([4.18209553e+13, 2.71689049e+14, 7.74556542e+13, 3.11190578e+14])

Calculate the square of the maximum distance where a point is still in the
circle, and count the number of points that match.

.. code-block:: python

    In [7]: incirc = (256.0**3 - 1)**2
    Out[7]: 281474943156225.0

    In [8]: inmont = np.count_nonzero(dist2 <= incirc)
    Out[8]: 3

This is only a small example with very few points. But for a large amount of
points one would calculate π as follows:

.. code-block:: python

    montepi = 4 * inmont/len(montex)

Without numpy
+++++++++++++

Here we use a slightly different ``values``, which converts the
``bytes`` into an array of ``float`` directly, per 3 bytes, MSB first.

.. code-block:: python

    def monte_carlo(d):
        values = [
            a * 65536.0 + b * 256.0 + c * 1.0 for a, b, c in
            zip(d[0::3], d[1::3], d[2::3])
        ]
        montex = values[0::2]
        montey = values[1::2]
        dist2 = (i * i + j * j for i, j in zip(montex, montey))
        incirc = (256.0 ** 3 - 1) ** 2
        inmont = sum(j <= incirc for j in dist2)
        montepi = 4 * inmont / len(montex)
        return montepi

