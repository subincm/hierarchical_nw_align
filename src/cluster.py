#!/usr/bin/python2.7

from __future__ import division

import os

import networkx as nx
import pylab as py
import pprint as pp
from mcl_clustering import networkx_mcl

os.environ["PYTHONPATH"]

G = nx.read_gexf("../Data/CJejuni/cjejuni.gexf", None, True)
#nx.draw_spring(G)
#py.show()

M, clusters = networkx_mcl(G)
pp.pprint(M)
pp.pprint("Found {} clusters.".format(len(clusters)))