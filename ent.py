#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: R.F. Smith <rsmith@xs4all.nl>
# $Date$
#
# To the extent possible under law, Roland Smith has waived all
# copyright and related or neighboring rights to the original works in
# chisquare.py. This work is published from the Netherlands. See
# http://creativecommons.org/publicdomain/zero/1.0/

import math
from os.path import getsize
import sys

def readdata(name):
    """Read the data from a file and count how often each byte value
    occurs.

    Arguments:
    name -- name of the file to read the data from
    """
    with open(name, 'rb') as f:
        ba = bytearray(getsize(name))
        f.readinto(ba)
    counts = [0]*256
    for b in ba:
        counts[b] += 1
    return ba, counts

def pearsonchisquare(d, counts=None):
    '''Calculate Pearson's χ² (chi square) test for an array of bytes. 
    See [http://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
    #Discrete_uniform_distribution]

    Arguments:
    d      -- data that is or can be converted to an array of bytes.
    counts -- list of counts for all byte values.
    '''
    if not isinstance(d, bytearray):
        d = bytearray(d)
    np = len(d)/256.0
    if not counts:
        counts = [0]*256
        for b in d:
            counts[b] += 1
    return sum([(counts[b] - np)**2/np for b in range(256)])

def entropy(counts):
    """Calculate the entropy of the data represented by the counts
    list. Returns the entropy in bits per byte.

    Arguments:
    counts -- list of counts for all byte values.
    """
    ent = 0.0
    sz = sum(counts)
    for b in counts:
        if b == 0:
            continue
        p = float(b)/sz
        ent -= p*math.log(p, 256)
    return ent*8

# _poz() and pochisq() are ported from chisq.c from random.zip;
# http://www.fourmilab.ch/random/ (also in the public domain)

def _poz(z):
    '''Probability of normal z value. Returns cumulative probability
    from -∞ to z. Adapted from a polynomial approximation in:
    "Ibbetson D, Algorithm 209, Collected Algorithms of the CACM 1963
    p. 616" Note: This routine has six digit accuracy, so it is only
    useful for absolute z values < 6.  For z values >= to 6.0, poz()
    returns 0.0.

    Arguments:
    z -- normal z value
    '''
    Z_MAX = 6.0
    if z == 0.0:
        x = 0.0
    else:
        y = 0.5 * math.fabs(z)
        if y >= Z_MAX * 0.5:
            x = 1.0
        elif y < 1.0:
            w = y * y
            x = ((((((((0.000124818987 * w
                        -0.001075204047) * w +0.005198775019) * w
                      -0.019198292004) * w +0.059054035642) * w
                    -0.151968751364) * w +0.319152932694) * w
                  -0.531923007300) * w +0.797884560593) * y * 2.0
        else:
            y -= 2.0
            x = (((((((((((((-0.000045255659 * y
                              +0.000152529290) * y -0.000019538132) * y
                           -0.000676904986) * y +0.001390604284) * y
                         -0.000794620820) * y -0.002034254874) * y
                       +0.006549791214) * y -0.010557625006) * y
                     +0.011630447319) * y -0.009279453341) * y
                   +0.005353579108) * y -0.002141268741) * y
                 +0.000535310849) * y +0.999936657524
    if z > 0:
        return (x + 1.0) * 0.5
    return (1.0 - x) * 0.5

def pochisq(x, df=255):
    '''Compute probability of χ² test value. Adapted from: Hill,
    I. D. and Pike, M. C.  Algorithm 299 Collected Algorithms for the
    CACM 1967 p. 243 Updated for rounding errors based on remark in
    ACM TOMS June 1985, page 185.

    According to http://www.fourmilab.ch/random/:

      We interpret the percentage (return value*100) as the degree to
      which the sequence tested is suspected of being non-random. If
      the percentage is greater than 99% or less than 1%, the sequence
      is almost certainly not random. If the percentage is between 99%
      and 95% or between 1% and 5%, the sequence is
      suspect. Percentages between 90% and 95% and 5% and 10% indicate
      the sequence is “almost suspect”.

    Arguments:
    x -- obtained chi-square value
    df -- degrees of freedom, defaults to 255 for random bytes.
    '''
    # Check arguments first
    if not isinstance(df, int):
        raise ValueError('df must be an integer')
    if x <= 0.0 or df < 1:
        return 1.0
    # Constants
    LOG_SQRT_PI = 0.5723649429247000870717135 # log(√π)
    I_SQRT_PI = 0.5641895835477562869480795 # 1/√π
    BIGX = 20.0
    a = 0.5 * x
    ev = 2 * (df / 2) == df
    # Helper functions.
    def even(t, f, w=ev):
        if w:
            return t
        return f
    def ex(x):
        if x < -BIGX:
            return 0.0
        return math.exp(x)
    if df > 1:
        y = ex(-a)
    s = even(y, 2.0 * _poz(-math.sqrt(x)))
    if df > 2:
        x = 0.5 * (df - 1.0)
        z = even(1.0, 0.5)
        if a > BIGX:
            e = even(0, LOG_SQRT_PI)
            c = math.log(a)
            while z <= x:
                e += math.log(z)
                s += ex(c * z - a - e)
                z += 1.0
            return s
        else:
            e = even(1.0, I_SQRT_PI / math.sqrt(a))
            c = 0.0
            while z <= x:
                e *= (a / z)
                c += e
                z += 1.0
            return c * y + s
    else:
        return s

def main(args=None):
    '''Calculates and prints figures about the randomness of the input
    files. Use test data if no arguments given

    Arguments:
    args -- list of input files
    '''
    if not args:
        args = ['test/random.dat']
    for fname in args:
        data, cnts = readdata(fname)
        print 'File "{}"'.format(fname)
        e = entropy(cnts)
        print '- Entropy is {:.6f} bits per byte.'.format(e)
        avg = sum(data)/float(len(data))
        outs = '- Arithmetic mean value of data bytes is {:.4f}'
        print outs.format(avg), '(random = 127.5).'
        c = pearsonchisquare(data, cnts)
        p = pochisq(c)
        outs = '- χ² distribution for {} samples is {:.2f}, and randomly'
        print outs.format(len(data), c)
        outs = '  would exceed this value {:.2f} percent of the times.'
        print outs.format(p*100)
        d = math.fabs(p*100-50)
        print "- According to the χ² test, this sequence",
        if d > 49:
            print "is almost certainly not random"
        elif d > 45:
            print "is suspected of being not random."
        elif d > 40:
            print "is close to random, but not perfect."
        else:
            print "looks random."

if __name__ == '__main__':
    main(sys.argv[1:])
