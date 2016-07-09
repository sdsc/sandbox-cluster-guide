#!/usr/bin/env python

"""
Calculate pi using the integral of a circle.

$ mpirun -np 32 ./cpi.py
"""

from mpi4py import MPI
import numpy

# get number of tasks and my rank
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# 100 elements per task
# each task does its own section
N = 100
h = 1.0/(N*float(size))
s = 0.0
start = rank*1.0/size
for i in range(0, N):
    x = start + h * (i + 0.5)
    s += 4.0 / (1.0 + x**2)
    piseg = numpy.array(s * h, dtype='d')

# sum up the results across tasks
pi = numpy.array(0.0, 'd')
comm.Reduce([piseg, MPI.DOUBLE], [pi, MPI.DOUBLE],
            op=MPI.SUM, root=0)

if rank == 0:
    print "pi = %0.16f, error is %0.16e" % (pi, numpy.fabs(pi - numpy.pi))
