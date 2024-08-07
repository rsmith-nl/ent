Profiling ``ent``
#################

:modified: 2023-12-26
:date: 2022-01-21 11:28:35
:tags: profiling, python3
:author: Roland Smith

.. Last modified: 2024-07-14T12:05:08+0200
.. vim:spelllang=en

The program ``ent_without_numpy.py`` is a lot slower than the version that
uses ``numpy``.
In this article the program will be profiled.

.. PELICAN_END_SUMMARY

The profiling is done as follows::

    > python -m cProfile -s tottime ent_without_numpy.py test/random.dat|less
    - Entropy is 7.999982 bits per byte.
    - Optimum compression would reduce the size
      of this 10485760 byte file by 0%.
    - χ² distribution for 10485760 samples is 259.03, and randomly
      would exceed this value 41.80% of the times.
      According to the χ² test, this sequence looks random.
    - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
    - Monte Carlo value for π is 3.139877754 (error 0.05%).
    - Serial correlation coefficient is -0.000296 (totally uncorrelated = 0.0).

         69915993 function calls (69915730 primitive calls) in 21.497 seconds

      Ordered by: internal time

      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
           1    3.931    3.931    7.373    7.373 statistics.py:123(_sum)
     3495261    2.891    0.000    5.944    0.000 {built-in method builtins.sum}
    10485761    2.703    0.000    2.703    0.000 statistics.py:219(_exact_ratio)
    10485757    2.437    0.000    4.271    0.000 ent_without_numpy.py:269(<genexpr>)
    10485757    1.833    0.000    1.833    0.000 ent_without_numpy.py:268(<genexpr>)
           1    1.672    1.672    6.589    6.589 ent_without_numpy.py:271(<listcomp>)
    10485761    1.305    0.000    1.305    0.000 ent_without_numpy.py:183(<genexpr>)
           1    1.301    1.301    1.301    1.301 ent_without_numpy.py:181(<listcomp>)
    10485761    1.069    0.000    1.069    0.000 ent_without_numpy.py:185(<genexpr>)
    10485876    0.740    0.000    0.740    0.000 {method 'get' of 'dict' objects}
           1    0.555    0.555    0.555    0.555 {built-in method _collections._count_elements}
     1747627    0.369    0.000    0.680    0.000 ent_without_numpy.py:275(<genexpr>)
     1747627    0.311    0.000    0.311    0.000 ent_without_numpy.py:274(<genexpr>)
           1    0.194    0.194   21.491   21.491 ent_without_numpy.py:28(main)
           1    0.146    0.146    5.892    5.892 ent_without_numpy.py:170(correlation)
           1    0.027    0.027    7.468    7.468 ent_without_numpy.py:256(monte_carlo)

The items with a tottime of <0.01 s are not shown.

According to ``time(1)``, the program uses around 11.1 s of real time and
10.8 s of user time::

  > /usr/bin/time python ent_without_numpy.py test/random.dat
  - Entropy is 7.999982 bits per byte.
  - Optimum compression would reduce the size
    of this 10485760 byte file by 0%.
  - χ² distribution for 10485760 samples is 259.03, and randomly
    would exceed this value 41.80% of the times.
    According to the χ² test, this sequence looks random.
  - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
  - Monte Carlo value for π is 3.139877754 (error 0.05%).
  - Serial correlation coefficient is -0.000296 (totally uncorrelated = 0.0).
        11.16 real        10.82 user         0.33 sys

For comparison, version that uses numpy runs in about 0.4 s on the same
machine on the same dataset::

  > /usr/bin/time python ent.py test/random.dat
  - Entropy is 7.999982 bits per byte.
  - Optimum compression would reduce the size
    of this 10485760 byte file by 0%.
  - χ² distribution for 10485760 samples is 259.03, and randomly
    would exceed this value 41.80% of the times.
    According to the χ² test, this sequence looks random.
  - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
  - Monte Carlo value for π is 3.139877754 (error 0.05%).
  - Serial correlation coefficient is -0.000296 (totally uncorrelated = 0.0).
          0.41 real         0.29 user         0.11 sys


Improvements
------------

Looking at the source for statistics.py, ``statistics.mean()`` is responsible for
the first three lines in the profile.
This function is actually pretty complex because it has to deal with different
types of data.

So let's replace it with ``statistics.fmean()``, a fast floating point
arithmetic mean.

.. code-block:: diff

  diff --git a/ent_without_numpy.py b/ent_without_numpy.py
  index 90cb219..46e4c9d 100644
  --- a/ent_without_numpy.py
  +++ b/ent_without_numpy.py
  @@ -5,7 +5,7 @@
  # Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
  # SPDX-License-Identifier: MIT
  # Created: 2012-08-25T23:37:50+0200
  -# Last modified: 2021-05-29T00:11:17+0200
  +# Last modified: 2022-01-21T11:55:53+0100
  """
  Partial implementation of the ‘ent’ program by John "Random" Walker in Python.
  
  @@ -75,7 +75,7 @@ def terseout(data, e, chi2, p, d, scc, mc):
      """
      print("0,File-bytes,Entropy,Chi-square,Mean," "Monte-Carlo-Pi,Serial-Correlation")
      n = len(data)
  -    m = stat.mean(data)
  +    m = stat.fmean(data)
      print(f"1,{n},{e:.6f},{chi2:.6f},{m:.6f},{mc:.6f},{scc}")
  
  
  @@ -109,7 +109,7 @@ def textout(data, e, chi2, p, d, scc, mc):
          print("is close to random, but not perfect.")
      else:
          print("looks random.")
  -    m = stat.mean(data)
  +    m = stat.fmean(data)
      print(f"- Arithmetic mean value of data bytes is {m:.4f} (random = 127.5).")
      err = 100 * (math.fabs(PI - mc) / PI)
      print(f"- Monte Carlo value for π is {mc:.9f} (error {err:.2f}%).")

And profile again::

    > python -m cProfile -s tottime ent_without_numpy.py test/random.dat|less
    - Entropy is 7.999982 bits per byte.
    - Optimum compression would reduce the size
      of this 10485760 byte file by 0%.
    - χ² distribution for 10485760 samples is 259.03, and randomly
      would exceed this value 41.80% of the times.
      According to the χ² test, this sequence looks random.
    - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
    - Monte Carlo value for π is 3.139877754 (error 0.05%).
    - Serial correlation coefficient is -0.000296 (totally uncorrelated = 0.0).
            48944433 function calls (48944172 primitive calls) in 13.888 seconds

      Ordered by: internal time

      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     3495260    2.843    0.000    5.816    0.000 {built-in method builtins.sum}
    10485757    2.410    0.000    4.143    0.000 ent_without_numpy.py:269(<genexpr>)
    10485757    1.734    0.000    1.734    0.000 ent_without_numpy.py:268(<genexpr>)
           1    1.634    1.634    6.410    6.410 ent_without_numpy.py:271(<listcomp>)
    10485761    1.257    0.000    1.257    0.000 ent_without_numpy.py:183(<genexpr>)
           1    1.238    1.238    1.238    1.238 ent_without_numpy.py:181(<listcomp>)
    10485761    1.052    0.000    1.052    0.000 ent_without_numpy.py:185(<genexpr>)
           1    0.537    0.537    0.537    0.537 {built-in method _collections._count_elements}
     1747627    0.363    0.000    0.663    0.000 ent_without_numpy.py:275(<genexpr>)
     1747627    0.300    0.000    0.300    0.000 ent_without_numpy.py:274(<genexpr>)
           1    0.188    0.188   13.881   13.881 ent_without_numpy.py:28(main)
           1    0.159    0.159    0.159    0.159 {built-in method math.fsum}
           1    0.132    0.132    5.724    5.724 ent_without_numpy.py:170(correlation)
           1    0.027    0.027    7.266    7.266 ent_without_numpy.py:256(monte_carlo)

The run time according to ``time(1)`` is 6.8 s of real time and 6.5 s of user
time.
This two-line change has reduced the run time by a third!

The built-in ``sum`` function now takes the most time.
Built-ins are outside the scope of this article, so the following three items
are now looked at.

Line 268 is a simple float conversion of the data (``MONTEN`` is a constant).

.. code-block:: python

  d = (float(j) for j in d[: len(d) // MONTEN * MONTEN])

And line 269 uses that to calculate an intermediate.

.. code-block:: python

  intermediate = (i * j for i, j in zip(d, it.cycle([256 ** 2, 256, 1])))

Since ``d`` is not used anywhere else, we can combine the to lines.

.. code-block:: diff

  diff --git a/ent_without_numpy.py b/ent_without_numpy.py
  index 46e4c9d..053c0e0 100644
  --- a/ent_without_numpy.py
  +++ b/ent_without_numpy.py
  @@ -5,7 +5,7 @@
  # Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
  # SPDX-License-Identifier: MIT
  # Created: 2012-08-25T23:37:50+0200
  -# Last modified: 2022-01-21T11:55:53+0100
  +# Last modified: 2022-01-21T12:46:44+0100
  """
  Partial implementation of the ‘ent’ program by John "Random" Walker in Python.

  @@ -265,8 +265,12 @@ def monte_carlo(d):
      """
      MONTEN = 6
      incirc = (256.0 ** (MONTEN // 2) - 1) ** 2
  -    d = (float(j) for j in d[: len(d) // MONTEN * MONTEN])
  -    intermediate = (i * j for i, j in zip(d, it.cycle([256 ** 2, 256, 1])))
  +    intermediate = (
  +        float(i) * j
  +        for i, j in zip(
  +            d[: len(d) // MONTEN * MONTEN], it.cycle((256.0 ** 2, 256.0, 1.0))
  +        )
  +    )
      args = [intermediate] * 3
      values = [sum(j) for j in it.zip_longest(*args)]
      montex = values[0::2]


After this change, we profile again::

    > python -m cProfile -s tottime ent_without_numpy.py test/random.dat|less
    - Entropy is 7.999982 bits per byte.
    - Optimum compression would reduce the size
      of this 10485760 byte file by 0%.
    - χ² distribution for 10485760 samples is 259.03, and randomly
      would exceed this value 41.80% of the times.
      According to the χ² test, this sequence looks random.
    - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
    - Monte Carlo value for π is 3.139877754 (error 0.05%).
    - Serial correlation coefficient is -0.000296 (totally uncorrelated = 0.0).
            38458676 function calls (38458415 primitive calls) in 11.774 seconds

      Ordered by: internal time
   
      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     3495260    2.794    0.000    5.795    0.000 {built-in method builtins.sum}
    10485757    2.018    0.000    2.018    0.000 ent_without_numpy.py:268(<genexpr>)
           1    1.593    1.593    4.190    4.190 ent_without_numpy.py:275(<listcomp>)
           1    1.311    1.311    1.311    1.311 ent_without_numpy.py:181(<listcomp>)
    10485761    1.272    0.000    1.272    0.000 ent_without_numpy.py:183(<genexpr>)
    10485761    1.068    0.000    1.068    0.000 ent_without_numpy.py:185(<genexpr>)
           1    0.537    0.537    0.537    0.537 {built-in method _collections._count_elements}
     1747627    0.361    0.000    0.662    0.000 ent_without_numpy.py:279(<genexpr>)
     1747627    0.300    0.000    0.300    0.000 ent_without_numpy.py:278(<genexpr>)
           1    0.188    0.188   11.768   11.768 ent_without_numpy.py:28(main)
           1    0.159    0.159    0.159    0.159 {built-in method math.fsum}
           1    0.132    0.132    5.831    5.831 ent_without_numpy.py:170(correlation)
           1    0.027    0.027    5.045    5.045 ent_without_numpy.py:256(monte_carlo)

The run time according to ``time(1)`` is now 6.3 s real time and 6.0 user time.

Looking at the lines 181--185, these are in the function ``correlation``.
In the calculations for the ``scct`` values, I replaced the ``bytes d`` with
the list of floats ``a``.

.. code-block:: diff

  diff --git a/ent_without_numpy.py b/ent_without_numpy.py
  index 5e11675..729c5ec 100644
  --- a/ent_without_numpy.py
  +++ b/ent_without_numpy.py
  @@ -5,7 +5,7 @@
  # Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
  # SPDX-License-Identifier: MIT
  # Created: 2012-08-25T23:37:50+0200
  -# Last modified: 2022-01-21T13:09:06+0100
  +# Last modified: 2022-01-21T13:13:46+0100
  """
  Partial implementation of the ‘ent’ program by John "Random" Walker in Python.
  
  @@ -180,9 +180,9 @@ def correlation(d):
      totalc = len(d)
      a = [float(j) for j in d]
      b = a[1:] + [a[0]]
  -    scct1 = sum(i * j for i, j in zip(d, b))
  -    scct2 = sum(d) ** 2
  -    scct3 = sum(j * j for j in d)
  +    scct1 = sum(i * j for i, j in zip(a, b))
  +    scct2 = sum(a) ** 2
  +    scct3 = sum(j * j for j in a)
      scc = totalc * scct3 - scct2
      if scc == 0:
          raise ValueError

This shortened the real run-time to 5.9 s and the user time to 5.5 s.

At this point I don't see any obvious improvements anymore.

Different Python versions
-------------------------

The default Python on my platform is 3.9. However, the most recent available
Python, 3.11 has significant speed improvements, so let's try that as well.

Python 3.9 timing::

   > time python3.9 ent_without_numpy.py test/random.dat
   - Entropy is 7.999982 bits per byte.
  - Optimum compression would reduce the size
    of this 10485760 byte file by 0%.
  - χ² distribution for 10485760 samples is 259.03, and randomly
    would exceed this value 41.80% of the times.
    According to the χ² test, this sequence looks random.
  - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
  - Monte Carlo value for π is 3.139875958 (error 0.05%).
  - Serial correlation coefficient is -0.000296 (totally uncorrelated = 0.0).
  3.184u 0.062s 0:03.24 100.0%    5+167k 0+0io 0pf+0w

Python 3.11 run::

  > time python3.11 ent_without_numpy.py test/random.dat
  - Entropy is 7.999982 bits per byte.
  - Optimum compression would reduce the size
    of this 10485760 byte file by 0%.
  - χ² distribution for 10485760 samples is 259.03, and randomly
    would exceed this value 41.80% of the times.
    According to the χ² test, this sequence looks random.
  - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
  - Monte Carlo value for π is 3.139875958 (error 0.05%).
  - Serial correlation coefficient is -0.000296 (totally uncorrelated = 0.0).
  2.272u 0.110s 0:02.38 100.0%    5+167k 0+0io 0pf+0w

Using Python 3.11 is a significant improvement compared to 3.9.

Using pyinstrument
------------------

Version 2022.08.27 of ``ent_without_numpy.py`` was profiled using
pyinstrument::

  > python -m pyinstrument ent_without_numpy.py test/random.dat
  - Entropy is 7.999982 bits per byte.
  - Optimum compression would reduce the size
    of this 10485760 byte file by 0%.
  - χ² distribution for 10485760 samples is 259.03, and randomly
    would exceed this value 41.80% of the times.
    According to the χ² test, this sequence looks random.
  - Arithmetic mean value of data bytes is 127.5116 (random = 127.5).
  - Monte Carlo value for π is 3.139875958 (error 0.05%).
  - Serial correlation coefficient is -0.000296 (totally uncorrelated = 0.0).

    _     ._   __/__   _ _  _  _ _/_   Recorded: 20:12:47  Samples:  4728
  /_//_/// /_\ / //_// / //_'/ //     Duration: 6.241     CPU time: 6.241
  /   _/                      v4.6.1

  Program: /usr/local/lib/python3.9/site-packages/pyinstrument-4.6.1-py3.9-freebsd-14.0-RELEASE-p3-amd64.egg/pyinstrument/__main__.py ent_without_numpy.py test/random.dat

  6.239 <module>  ent_without_numpy.py:9
  └─ 6.235 main  ent_without_numpy.py:27
    ├─ 4.129 correlation  ent_without_numpy.py:169
    │  ├─ 1.700 [self]  ent_without_numpy.py
    │  ├─ 1.253 <genexpr>  ent_without_numpy.py:181
    │  ├─ 1.066 <genexpr>  ent_without_numpy.py:183
    │  └─ 0.110 sum  <built-in>
    ├─ 1.429 monte_carlo  ent_without_numpy.py:254
    │  ├─ 0.658 <listcomp>  ent_without_numpy.py:264
    │  ├─ 0.566 <genexpr>  ent_without_numpy.py:271
    │  │  ├─ 0.302 [self]  ent_without_numpy.py
    │  │  └─ 0.264 <genexpr>  ent_without_numpy.py:269
    │  └─ 0.205 [self]  ent_without_numpy.py
    ├─ 0.493 readdata  ent_without_numpy.py:118
    │  └─ 0.489 Counter.__init__  collections/__init__.py:581
    │        [3 frames hidden]  collections, <built-in>
    └─ 0.141 textout  ent_without_numpy.py:81
        └─ 0.141 fmean  statistics.py:321
              [2 frames hidden]  statistics, <built-in>

  To view this report with different options, run:
      pyinstrument --load-prev 2024-01-19T20-12-47 [options]

Line 181 is:

.. code-block:: python

  scct1 = sum(i * j for i, j in zip(d, b))

And line 183:

.. code-block:: python

  scct3 = sum(j * j for j in d)

These are generator expressions operating on ``bytes`` objects.
Apart from using ``numpy``, I'm not sure what I should do to make them faster.

Converting ``d`` and ``b`` into ``array.array('B')`` shaved ≈0.08 second
off the runtime of ``correlation``.
The diff of the code is below.

.. code-block:: diff

  > git diff ent_without_numpy.py
  diff --git a/ent_without_numpy.py b/ent_without_numpy.py
  index de05a42..c1bf7e6 100644
  --- a/ent_without_numpy.py
  +++ b/ent_without_numpy.py
  @@ -5,7 +5,7 @@
  # Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
  # SPDX-License-Identifier: MIT
  # Created: 2012-08-25T23:37:50+0200
  -# Last modified: 2022-08-27T10:50:17+0200
  +# Last modified: 2024-01-19T20:38:00+0100
  """
  Partial implementation of the ‘ent’ program by John "Random" Walker in Python.
  
  @@ -14,13 +14,14 @@ This version does not use numpy.
  See http://www.fourmilab.ch/random/ for the original.
  """
  
  +import array
  import argparse
  import collections
  import math
  import statistics as stat
  import sys
  
  -__version__ = "2022.08.27"
  +__version__ = "2024.01.19"
  PI = 3.14159265358979323846
  
  
  @@ -176,11 +177,13 @@ def correlation(d):
      Returns:
          Serial correlation coeffiecient.
      """
  -    totalc = len(d)
  -    b = d[1:] + bytes(d[0])
  -    scct1 = sum(i * j for i, j in zip(d, b))
  -    scct2 = sum(d) ** 2
  -    scct3 = sum(j * j for j in d)
  +    da = array.array('B', d)
  +    totalc = len(da)
  +    ba = array.array('B', da[1:])
  +    ba.append(da[0])
  +    scct1 = sum(i * j for i, j in zip(da, ba))
  +    scct2 = sum(da) ** 2
  +    scct3 = sum(j * j for j in da)
      scc = totalc * scct3 - scct2
      if scc == 0:
          raise ValueError

However, when Python 3.11 became the default python version on FreeBSD, the
previous version using ``bytes`` was faster again. so the change to arrays was
reverted.
