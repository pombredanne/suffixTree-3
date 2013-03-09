#!/usr/bin/python

import matplotlib.pyplot as plt

ticks = [10, 100,1000, 10000, 100000]
values = [623, 1593, 12941, 135341, 225341]
a = Series(values, index=ticks)
plt.plot(ticks, values, marker='o', linestyle='--', color='r')
plt.show()
plt.plot(ticks, values, marker='o', linestyle='--', color='r')
plt.xlabel("length of string")
plt.ylabel("MemSize Cost")
plt.title("Linear Time Suffix Implementation")
plt.savefig("result.pdf")
