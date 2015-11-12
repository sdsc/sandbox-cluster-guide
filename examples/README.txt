=== Dependencies ===

The program depends on mpi4py and pygame.

The mpi4py documentation and installation instructions 
can be found at:
   http://mpi4py.scipy.org/

The pygame documentation and installation instructions
can be found at:
   http://www.pygame.org/download.shtml

=== How to run on a single (multi-core) host ===

Run it with 

 mpiexec -n 4 python ./some_python_script

where the number after "-np " is the numer of parallel 
MPI processes to be started.
