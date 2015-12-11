#!/usr/bin/python2.7

from __future__ import division

import os

import networkx as nx
import pylab as py
import pprint as pp
from mcl import mcl_clustering
#from mcl_clustering import networkx_mcl

#INPUT_FILE ="../Data/NAPAbench/5-way/CG_set/Family_10/B.net"
INPUT_FILE = "../Data/GHOSTData.fixed/Data/CJejuni/cjejuni.gexf"
GEXF_FORMAT=".gexf"
NET_FORMAT=".net"

os.environ["PYTHONPATH"]

if INPUT_FILE.endswith(GEXF_FORMAT):
    G = nx.read_gexf(INPUT_FILE, None, True)
elif INPUT_FILE.endswith(NET_FORMAT):
    G=nx.Graph()
    f = file(INPUT_FILE, 'r')
    # iterate over the lines in the file
    for line in f:
        # split the line into a list of column values
        columns = line.split('\t')
        # clean any whitespace off the items
        columns = [col.strip() for col in columns]
        if columns:
            G.add_edge(columns[0], columns[1])
else:
    print("Unsupported Format")
    exit(0)
print("Number of Nodes =", G.number_of_nodes(), "No of edges = ", G.number_of_edges())

#nx.draw_spring(G)
#py.show()

M, clusters = mcl_clustering.networkx_mcl(G)
pp.pprint(M)
pp.pprint("Found {} clusters.".format(len(clusters)))