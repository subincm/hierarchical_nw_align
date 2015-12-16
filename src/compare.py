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
def filter_fn(x):
 for y in x:
  if math.isnan(y):
    return False
  elif 0 == y:
    return False
 return True

for path in sys.argv[1:]:
  if os.path.isfile(path):
    lst = getdict(path).values()
    list_of_lists.append(lst)

comparison_list = zip(*list_of_lists)
print zip(*filter(filter_fn, comparison_list))