#!/usr/bin/env python
# file: ent_without_numpy.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2012-08-25T23:37:50+0200
# Last modified: 2022-08-27T10:50:17+0200
"""
Partial implementation of the ‘ent’ program by John "Random" Walker in Python.

This version does not use numpy.

See http://www.fourmilab.ch/random/ for the original.
"""

import argparse
import collections
import math
import statistics as stat
import sys

__version__ = "2022.08.27"
PI = 3.14159265358979323846


def main(argv):
    """
    Calculate and print figures about the randomness of the input files.

    Arguments:
        argv: Program options.
    """
    opts = argparse.ArgumentParser(prog="ent", description=__doc__)
    opts.add_argument(
        "-c", action="store_true", help="print occurrence counts (not implemented yet)"
    )
    opts.add_argument("-t", action="store_true", help="terse output in CSV format")
    opts.add_argument("-v", "--version", action="version", version=__version__)
    opts.add_argument(
        "files", metavar="file", nargs="*", help="one or more files to process"
    )
    args = opts.parse_args(argv)
    for fname in args.files:
        data, cnts = readdata(fname)
        e = entropy(cnts)
        c = pearsonchisquare(cnts)
        p = pochisq(c)
        d = math.fabs(p * 100 - 50)
        m = monte_carlo(data)
        try:
            scc = correlation(data)
            es = f"{scc:.6f}"
        except ValueError:
            es = "undefined"
        if args.t:
            terseout(data, e, c, p, d, es, m)
        else:
            textout(data, e, c, p, d, es, m)


def terseout(data, e, chi2, p, d, scc, mc):
    """
    Print the results in terse CSV.

    Arguments:
        data: file contents
        e: Entropy of the data in bits per byte.
        chi2: Χ² value for the data.
        p: Probability of normal z value.
        d: Percent distance of p from centre.
        scc: Serial correlation coefficient.
        mc: Monte Carlo approximation of π.
    """
    print("0,File-bytes,Entropy,Chi-square,Mean," "Monte-Carlo-Pi,Serial-Correlation")
    n = len(data)
    m = stat.fmean(data)
    print(f"1,{n},{e:.6f},{chi2:.6f},{m:.6f},{mc:.6f},{scc}")


def textout(data, e, chi2, p, d, scc, mc):
    """
    Print the results in plain text.

    Arguments:
        data: file contents
        e: Entropy of the data in bits per byte.
        chi2: Χ² value for the data.
        p: Probability of normal z value.
        d: Percent distance of p from centre.
        scc: Serial correlation coefficient.
        mc: Monte Carlo approximation of π.
    """
    print(f"- Entropy is {e:.6f} bits per byte.")
    print("- Optimum compression would reduce the size")
    red = (100 * (8 - e)) / 8
    n = len(data)
    print(f"  of this {n} byte file by {red:.0f}%.")
    print(f"- χ² distribution for {n} samples is {chi2:.2f}, and randomly")
    pp = 100 * p
    print(f"  would exceed this value {pp:.2f}% of the times.")
    print("  According to the χ² test, this sequence", end=" ")
    if d > 49:
        print("is almost certainly not random")
    elif d > 45:
        print("is suspected of being not random.")
    elif d > 40:
        print("is close to random, but not perfect.")
    else:
        print("looks random.")
    m = stat.fmean(data)
    print(f"- Arithmetic mean value of data bytes is {m:.4f} (random = 127.5).")
    err = 100 * (math.fabs(PI - mc) / PI)
    print(f"- Monte Carlo value for π is {mc:.9f} (error {err:.2f}%).")
    print(f"- Serial correlation coefficient is {scc} (totally uncorrelated = 0.0).")


def readdata(name):
    """
    Read the data from a file and count byte occurences.

    Arguments:
        name: Path of the file to read

    Returns:
        data: file contents as bytes.
        cnts: list containing the occurance of each byte value 0−255.
    """
    with open(name, "rb") as inf:
        data = inf.read()
    cnts = collections.Counter(data).values()
    return data, cnts


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


def correlation(d):
    """
    Calculate the serial correlation coefficient of the data.

    Arguments:
        d: data in the form of bytes.

    Returns:
        Serial correlation coeffiecient.
    """
    totalc = len(d)
    b = d[1:] + bytes(d[0])
    scct1 = sum(i * j for i, j in zip(d, b))
    scct2 = sum(d) ** 2
    scct3 = sum(j * j for j in d)
    scc = totalc * scct3 - scct2
    if scc == 0:
        raise ValueError
    scc = (totalc * scct1 - scct2) / scc
    return scc


def pochisq(x, df=255):
    """
    Compute probability of χ² test value.

    Adapted from: Hill, I. D. and Pike, M. C.  Algorithm 299 Collected
    Algorithms for the CACM 1967 p. 243 Updated for rounding errors based on
    remark in ACM TOMS June 1985, page 185.

    According to http://www.fourmilab.ch/random/:

      We interpret the percentage (return value*100) as the degree to which
      the sequence tested is suspected of being non-random. If the percentage
      is greater than 99% or less than 1%, the sequence is almost certainly
      not random. If the percentage is between 99% and 95% or between 1% and
      5%, the sequence is suspect. Percentages between 90% and 95% and 5% and
      10% indicate the sequence is “almost suspect”.

    Arguments:
        x: Obtained χ² value.
        df: Degrees of freedom, defaults to 255 for random bytes.

    Returns:
        The degree to which the sequence tested is suspected of being
        non-random.
    """
    # Check arguments first
    if not isinstance(df, int):
        raise ValueError("df must be an integer")
    if x <= 0.0 or df < 1:
        return 1.0
    # Constants
    LOG_SQRT_PI = 0.5723649429247000870717135  # log(√π)
    I_SQRT_PI = 0.5641895835477562869480795  # 1/√π
    BIGX = 20.0
    a = 0.5 * x
    even = df % 2 == 0
    if df > 1:
        y = math.exp(-a)
    nd = stat.NormalDist()
    s = y if even else 2.0 * nd.cdf(-math.sqrt(x))
    if df > 2:
        x = 0.5 * (df - 1.0)
        z = 1.0 if even else 0.5
        if a > BIGX:
            e = 0 if even else LOG_SQRT_PI
            c = math.log(a)
            while z <= x:
                e = math.log(z) + e
                s += math.exp(c * z - a - e)
                z += 1.0
            return s
        else:
            e = 1.0 if even else I_SQRT_PI / math.sqrt(a)
            c = 0.0
            while z <= x:
                e = e * a / z
                c = c + e
                z += 1.0
            return c * y + s
    else:
        return s


def monte_carlo(d):
    """
    Calculate Monte Carlo value for π.

    Arguments:
        d:  byte values.

    Returns:
        Approximation of π
    """
    values = [
        a * 65536.0 + b * 256.0 + c * 1.0 for a, b, c in zip(d[0::3], d[1::3], d[2::3])
    ]
    montex = values[0::2]
    montey = values[1::2]
    dist2 = (i * i + j * j for i, j in zip(montex, montey))
    # constant in the next line is (256.0 ** 3 - 1) ** 2
    inmont = sum(k <= 281474943156225.0 for k in dist2)
    montepi = 4 * inmont / len(montex)
    return montepi


if __name__ == "__main__":
    main(sys.argv[1:])
