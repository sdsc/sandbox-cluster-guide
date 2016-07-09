# Parallel Programming

How can make these cores, processors, and computers work together? What examples can I look at?

## Running Parallel Programs

```
pi@pinode-0:~ $ cd /sandbox-cluster-guide/examples
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 2 ./hello.py
```

### A Simple Hello

Most languages have a "Hello, world!" example and we'll try that for our Python and MPI tests. First let's look at [hello.py](../examples/hello.py) in the [examples](../examples/) directory. First will run this with 2 tasks using the `mpirun` command and the flag `-np` to specify the number of tasks.

```
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 2 ./hello.py
Hello world from task  0  on  pinode-0
Hello world from task  1  on  pinode-0
pi@pinode-0:~/sandbox-cluster-guide/examples $
```

Because we didn't tell MPI where to run, all the tasks ran on `pinode-0` where we were typing. Let's see what happens when we increase the number of tasks.

```
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 4 ./hello.py
Hello world from task  0  on  pinode-0
Hello world from task  1  on  pinode-0
Hello world from task  2  on  pinode-0
Hello world from task  3  on  pinode-0
pi@pinode-0:~/sandbox-cluster-guide/examples $
```

Not surprising, just more tasks on `pindode-0`. This time we'll add another flag, `-hostfile` and use a file named `two-pis.txt`.

```
pi@pinode-0:~/sandbox-cluster-guide/examples $  cat two-pis.txt 
pinode-0
pinode-1
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 2 -hostfile two-pis.txt ./hello.py
Hello world from task  0  on  pinode-0
Hello world from task  1  on  pinode-1
pi@pinode-0:~/sandbox-cluster-guide/examples $
```

And now we have a change! Task 1 ran on `pinode-1`, the second host specified in the file. Now we have a means to make tasks run on other nodes. What happens if we run with 4 tasks?

```
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 4 -hostfile two-pis.txt ./hello.py
Hello world from task  0  on  pinode-0
Hello world from task  1  on  pinode-1
Hello world from task  2  on  pinode-0
Hello world from task  3  on  pinode-1
pi@pinode-0:~/sandbox-cluster-guide/examples $
```

It looks like the tasks assignment loops back to the top of the file. We can also adjust the file to change the ordering to be ordered by the node numbers (see [four-tasks-0011.txt](../examples/four-tasks-0011.txt).

```
pi@pinode-0:~/sandbox-cluster-guide/examples $ cat four-tasks-0011.txt
pinode-0
pinode-0
pinode-1
pinode-1
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 4 -hostfile four-tasks-0011.txt ./hello.py
Hello world from task  0  on  pinode-0
Hello world from task  1  on  pinode-0
Hello world from task  2  on  pinode-1
Hello world from task  3  on  pinode-1
pi@pinode-0:~/sandbox-cluster-guide/examples $
```

Sure enough, the first two tasks ran on `pinode-0` and the last two on `pinode-1`. And because we can determine which node we're running on we could guide the application's behavior either by its rank (MPI task ID) and, or, the node's name.

### Making it Visual

A big drawback of these command-line examples is that the only feedback you get telling you where the task is running are those hostnames. But if we can launch tasks on another Pi we can also open windows on it. Find out what happens when you run the [images.py](../examples/images.py) script.

```
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 4 ./images.py cat.jpg
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 4 -hostfile two-pis.txt ./images.py cat.jpg
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 4 -hostfile four-tasks-0011.txt ./images.py cat.jpg
```

The [cpi_display.py](../examples/cpi_display.py) is another graphical example, this time showing portions of an integral computing pi. We can run that and observe how the windows controlled by the individual tasks move with their node assignment.

```
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 8  ./cpi_display.py
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 8 -hostfile two-pis.txt ./cpi_display.py
pi@pinode-0:~/sandbox-cluster-guide/examples $ mpirun -np 8 -hostfile four-tasks-0011.txt ./cpi_display.py
```
