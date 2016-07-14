#!/usr/bin/env python

import socket
from mpi4py import MPI

# Communicator object
comm = MPI.COMM_WORLD
# ID of this task
rank = comm.Get_rank()
# Total number of MPI tasks
size = comm.Get_size()
# Name of host this task is on
# Could also use MPI.Get_processor_name()
myhost = socket.gethostname()

for i in range(0, size):
    # Say hello if it's our turn
    if i == rank:
        print "Hello world from task ", rank, " on ", myhost
    # Make sure we stay in order
    comm.Barrier()
