#!/usr/bin/python2.7

import os
import sys
import math

def getdict(path):
  d = {}
  with open(path) as f:
    for line in f:
      k, v = line.split()
      d[k] = float(v.strip('%'))
    return d

# ---------------MAIN---------------
list_of_lists = []
for path in sys.argv[1:]:
  if os.path.isfile(path):
    list_of_lists.append(getdict(path).values())

for xy in [x for x in zip(*list_of_lists) if not reduce(lambda x, y: x or y, [math.isnan(y) for y in x]) ]:
  print xy[0], xy[1]