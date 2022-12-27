# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# Created: 2022-11-11T09:20:06+0100
# Last modified: 2022-12-27T18:02:29+0100
.PHONY: all clean

all:: ent-compiled

ent-compiled: ent-compiled.c
	clang -O3 -flto -I /usr/local/include/python3.9/ -L/usr/local/lib/ \
		-o ent-compiled ent-compiled.c -lpython3.9
	strip ent-compiled

ent-compiled.c: ent_without_numpy.py
	cython --embed -3 -o ent-compiled.c ent_without_numpy.py



clean::
	rm -f ent-compiled.c ent-compiled
