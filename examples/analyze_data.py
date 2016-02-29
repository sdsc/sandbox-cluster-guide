#!/usr/bin/env python

import csv
import matplotlib.pyplot as mpl
from itertools import cycle
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

reaction = []
days = []
subject = []

colors = ['r','b','g','c','m','y','k']
colorsCycle = cycle(colors)
lines = ['-','--',':','-.']
linesCycle = cycle(lines)
markers = ['+','.','o','*','p','s','x','D','h','^']
markersCycle = cycle(markers)

for d in csv.DictReader(open('/home/hungmaau2/sandbox-cluster-guide/examples/sleepstudy.csv'), delimiter=','):
	#print d['Reaction']
	reaction.append(float(d['Reaction']))
	days.append(int(d['Days']))
	subject.append(int(d['Subject']))

if comm.rank == 0:
	selected_subject = subject[0]
	subjects = [selected_subject]
	compiled_list = []
	lists = []
	i = 0
	for sub in subject:
		if sub == selected_subject:
			lists.append(reaction[i])
		else:
			compiled_list.append(lists)
			subjects.append(sub)
			selected_subject = sub
			lists = []
			lists.append(reaction[i])
		i+=1	
	compiled_list.append(lists)	
	
	#print compiled_list
	set_days = []
	for day in days:
		if day in set_days:
			continue
		else:
			set_days.append(day)
	#print set_days
	#print subjects
	mpl.figure()
	i = 0
	while i < len(subjects):
		mpl.plot(set_days,compiled_list[i])
		i+=1
	mpl.show()

if comm.rank == 1:
	#plot of reaction time over days
	mpl.plot(days,reaction,'ro')
	mpl.ylabel('Reaction times')
	mpl.xlabel('Number of sleep deprived days')
	mpl.show()


#print "Reaction= ", reaction
#print "Days= ", days
#print "Subject= ", subject
