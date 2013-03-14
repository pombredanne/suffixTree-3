#!/usr/bin/python

import matplotlib.pyplot as plt
#from subprocess import Popen
import os
import pdb

def line_yielder(file):
  with open(file) as IN:
    while True:
      line = IN.readline()
      if not line.endswith('\n') and line == "":
        break
      yield(line)
  IN.close() 

result = open("result").readlines()
result = [map(float, i.split()) for i in result]

ticks = [i[0] for i in result ] 
values = [i[1] for i in result ] 
times = [i[2] for i in result ] 


fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(ticks,values, 'ro--')
ax1.set_xlabel("length of string")
ax1.set_ylabel("MemSize Cost")
ax2=ax1.twinx()
s2 = times
ax2.plot(ticks, s2, 'bx--')
ax2.set_ylabel("time elapased")
for t2 in ax2.get_yticklabels():
    t2.set_color('b')
plt.title("String size VS Time and Space")
plt.savefig("result.pdf")
