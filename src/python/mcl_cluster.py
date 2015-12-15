import networkx as nx
#import pylab as py
import pprint as pp
import os
import Constants
import Utils

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
    
def getMCLFromFile(infile, outdir,  mcl_param, clusterfile = './mcl.DAT'):
  cmd = Constants.MCL.format(infile, clusterfile, mcl_param)
  os.system(cmd)
  
  maingraph = Utils.convertNetToGefx(infile)
  graphname = os.path.basename(infile).split('.')[0]
  outdirname = os.path.join(outdir, 'MCL', graphname)
  if not os.path.exists(outdirname) :
    os.makedirs(outdirname)
  
  clusterindex = 0
  with open(clusterfile) as f:
    for line in f:
      cluster_nodes = line.split()
      cluster_graph = maingraph.subgraph(cluster_nodes)
      pathtoclustergraph = os.path.join(outdirname, graphname + str(clusterindex) + Constants.GEXF_FORMAT)
      nx.write_gexf(cluster_graph, pathtoclustergraph)
      clusterindex = clusterindex + 1
  return outdirname