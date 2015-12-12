import networkx as nx
#import pylab as py
import pprint as pp
from mcl import mcl_clustering

def get_clusters(A):
    clusters = []
    for i, r in enumerate((A>0).tolist()):
        if r[i]:
            clusters.append(A[i,:]>0)

    clust_map  ={}
    for cn , c in enumerate(clusters):
        for x in  [ i for i, x in enumerate(c) if x ]:
            clust_map[cn] = clust_map.get(cn, [])  + [x]
    return clust_map

def mcl_cluster(G):
    M, clusters = mcl_clustering.networkx_mcl(G)
    get_clusters(M)
    pp.pprint(M)
    pp.pprint("Found {} clusters.".format(len(clusters)))