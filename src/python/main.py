#!/usr/bin/python2.7
import os
import Constants
import Utils
import mcl_cluster
import kmeans_cluster
import dbscan_cluster

#import hungarian
#import compute_cluster_param
from collections import defaultdict
from gayleshapley import *

import hungarian
import compute_cluster_param


SDF_PATH="../../Data/GHOSTData.fixed/"

def getMapOfGraphClusters():
  ret = defaultdict(lambda: [])
  for fgraph in os.walk(Constants.KMEANS_PATH):
    for fcluster in os.listdir(fgraph[0]):
      if fcluster.endswith(Constants.GEXF_FORMAT):
	ret[os.path.basename(fgraph[0])].append(os.path.join(os.path.dirname(fgraph[0]), os.path.basename(fgraph[0]),fcluster))
  return ret

def letsStartAlgorithm():
    #hungarian.Hungarian_algo()
    #Form networkx representation of both graphs
    G1 = Utils.convertNetToGefx(Constants.INPUT_FILE_NET_1)
    G2 = Utils.convertNetToGefx(Constants.INPUT_FILE_NET_2)
    
    #Run one of the first clustering algorithm
#     mcl_cluster.mcl_cluster(G1)
#     mcl_cluster.mcl_cluster(G2)

    #print("**************Run kmeans*****************")
    #Run kmeans
    kmeans_cluster.kmeans_cluster(G1, Constants.INPUT_FILE_1_NAME)
    kmeans_cluster.kmeans_cluster(G2, Constants.INPUT_FILE_2_NAME)
    Utils.ComputeSpectralDistance(Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME, "Kmeans")

    #print("**************Run DBScan*****************")
    #Run dbscan
    #dbscan_cluster.dbscan_cluster(G1, Constants.INPUT_FILE_1_NAME)
    #dbscan_cluster.dbscan_cluster(G2, Constants.INPUT_FILE_1_NAME)

    #Compute cluster parameters
    #filelist=compute_cluster_param.listfiles(SDF_PATH)
    #for f in filelist:
    #     print(f)
    #     print("avg:",compute_cluster_param.compute_average(f))
    
    # Gayle-Shapely algo
    #mp = getMapOfGraphClusters()
    #for g in mp:
    #  for h in mp:
	#if g < h:
	 # for gsg in mp[g]:
	  #  for hsg in mp[h]:
	   #   print gsg, hsg, getDistanceBetweenGraphs(gsg, hsg)
    clustersdf = '../../Data/Kmeans/SDF/cluster.sdf'
    clustersdf = createClusterSDF('../../Data/Kmeans/SDF/A_B', '../../Data/Kmeans/SDF/A_B_cluster.sdf')
    d, pairs = getDistanceAndPairsFromSDF(clustersdf)
    print list(pairs)

if __name__ == '__main__':
    letsStartAlgorithm()
