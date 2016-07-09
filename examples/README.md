Examples
========

Dependencies
------------

The program depends on mpi4py and pygame.

The mpi4py documentation and installation instructions 
can be found at:
   http://mpi4py.scipy.org/

mpi4py is available from the Raspbian repository as `python-mpi4py`.

The pygame documentation and installation instructions
can be found at: http://www.pygame.org/download.shtml

Note that Pygame is included with Raspbian.

How to run on a single (multi-core) host
----------------------------------------

Run it with 

```
$ mpiexec -n 4 python ./some_python_script
```

where the number after "`-np`" is the numer of parallel 
MPI processes to be started.

`images.py`
-----------

This python script takes an image and displays it across
four different windows or displays. Each window will display 
a distinct fourth of the image.

In order to add your own file, change the following line in 
the script to be the image file you select:

```
   #Where the image file is stored; need to edit the file name before using
   img = pygame.image.load('20140902_200423.jpg')
```

Afterwards, save the python script and follow the instructions above
to run the python script.
