#!/usr/bin/env python

"""
Takes a data set and each task renders a unique graph


Run this using
$ mpirun -np 4 python ./analyze_data.py
"""
import os
import sys
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

#General arrays of options that can be used when creating
#graphs such as type of points and lines as well as color
colors = ['r','b','g','c','m','y','k']
colorsCycle = cycle(colors)
lines = ['-','--',':','-.']
linesCycle = cycle(lines)
markers = ['+','.','o','*','p','s','x','D','h','^']
markersCycle = cycle(markers)

for d in csv.DictReader(open('./sleepstudy.csv'), delimiter=','):
	#print d['Reaction']
	reaction.append(float(d['Reaction']))
	days.append(int(d['Days']))
	subject.append(int(d['Subject']))

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

set_days = []
for day in days:
	if day in set_days:
		continue
	else:
		set_days.append(day)

hashmap = []
compiled_reaction_by_day = []
for day_t in set_days:
	selected_day = day_t
	temp_list = []
	i = 0
	for day in days:
		if day == selected_day:
			temp_list.append(reaction[i])
		i+=1
	compiled_reaction_by_day.append(temp_list)

reaction_average_list = []
for n in compiled_reaction_by_day:
	reaction_average_list.append(sum(n)/len(n))

#print reaction_average_list	

compiled_reaction_by_subject = []
for subject_s in subjects:
	selected_subject = subject_s
	temp_list = []
	i = 0
	for sub in subject:
		if sub == selected_subject:
			temp_list.append(reaction[i])
		i+=1
	compiled_reaction_by_subject.append(temp_list)

reaction_average_by_subject = []
for n in compiled_reaction_by_subject:
	reaction_average_by_subject.append(sum(n)/len(n))
	

#print compiled_list

os.environ['DISPLAY'] = ':0.0'
if comm.rank == 0:
	os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
	#print set_days
	#print subjects
	mpl.figure()
	i = 0
	while i < len(subjects):
		mpl.plot(set_days,compiled_list[i])
		i+=1
	mpl.ylabel('Reaction times')
	mpl.xlabel('Number of sleep deprived days')
	mpl.show()

if comm.rank == 1:
	#plot of reaction time over days
	os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
	mpl.plot(days,reaction,'ro')
	mpl.ylabel('Reaction times')
	mpl.xlabel('Number of sleep deprived days')
	mpl.show()

if comm.rank == 2:
	os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
	mpl.plot(set_days,reaction_average_list,'c^')
	for xy in zip(set_days,reaction_average_list):
		mpl.annotate('(%s, %s)' %xy, xy=xy)
	mpl.grid()
	mpl.ylabel('Average reaction times of all subjects')
	mpl.xlabel('Number of sleep deprived days')
	mpl.show()

if comm.rank == 3:
	os.environ['SDL_VIDEO_WINDOW_POS'] = "200,100"
	mpl.plot(subjects,reaction_average_by_subject,'ro')
	for xy in zip(subjects,reaction_average_by_subject):
		mpl.annotate('(%s, %s)' %xy, xy=xy)
	mpl.grid()
	mpl.ylabel('Average reaction time per subject')
	mpl.xlabel('Sleep deprived subject number')
	mpl.show()


#print "Reaction= ", reaction
#print "Days= ", days
#print "Subject= ", subject
