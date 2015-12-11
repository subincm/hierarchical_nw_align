import networkx as nx
#import pylab as py
import pprint as pp
from mcl import mcl_clustering

def mcl_cluster(G):
    M, clusters = mcl_clustering.networkx_mcl(G)
    pp.pprint(M)
    pp.pprint("Found {} clusters.".format(len(clusters)))