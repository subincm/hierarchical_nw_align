#!/usr/bin/python2.7
import os
import Constants
import Utils
import mcl_cluster
import kmeans_cluster
import dbscan_cluster
import generate_alignment
#import hungarian
#import compute_cluster_param
from collections import defaultdict
from gayleshapley import *
import subprocess
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
    subprocess.call("rm -rf ../../Data/KMeans", shell=True)
    G1 = Utils.convertNetToGefx(Constants.INPUT_FILE_1 + Constants.NET_FORMAT)
    G2 = Utils.convertNetToGefx(Constants.INPUT_FILE_2 + Constants.NET_FORMAT)
    
    #Run one of the first clustering algorithm
#     mcl_cluster.mcl_cluster(G1)
#     mcl_cluster.mcl_cluster(G2)

    #print("**************Run kmeans*****************")
    #Run kmeans
    num_clusters1 = kmeans_cluster.kmeans_cluster(G1, Constants.INPUT_FILE_1_NAME)
    num_clusters2 = kmeans_cluster.kmeans_cluster(G2, Constants.INPUT_FILE_2_NAME)
    SDF_PATH = Utils.ComputeSpectralDistance(Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME, "Kmeans")

    #Find best Matching for our bipartite graph
    #Compute cluster parameters
    cluster_edge_weight_matrix = compute_cluster_param.find_cluster_edges_SDF(SDF_PATH, num_clusters1, num_clusters2)
    best_cluster_pairs = hungarian.Hungarian_algo(cluster_edge_weight_matrix)
    
    #Generate alignment score of our graphs
    generate_alignment.generate_alignment_score(best_cluster_pairs, "Kmeans", "SDF", Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME)

def letsStartAnotherAlgorithm():
  subprocess.call("rm -rf ../../Data/MCL", shell=True)
  A_sg_dir = mcl_cluster.getMCLFromFile(Constants.INPUT_FILE_1+Constants.NET_FORMAT, '../../Data')
  B_sg_dir = mcl_cluster.getMCLFromFile(Constants.INPUT_FILE_2+Constants.NET_FORMAT, '../../Data')
  print Utils.ComputeSpectralDistance(A_sg_dir.split('/')[-1], B_sg_dir.split('/')[-1], "MCL")
  
  clustersdf = createClusterSDF('../../Data/MCL/SDF/A_B', '../../Data/MCL/SDF/A_B_cluster.sdf')
  d, best_cluster_pairs = getDistanceAndPairsFromSDF(clustersdf)
    
  best_cluster_pairs = [(pair[0][1:], pair[1][1:]) for pair in best_cluster_pairs]
  print best_cluster_pairs
  
  final_out = generate_alignment.generate_alignment_score(best_cluster_pairs, "MCL", "SDF", Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME)
  


if __name__ == '__main__':
  letsStartAlgorithm()
  #letsStartAnotherAlgorithm()
#   #print Utils.getEdgeCorrectness('/home/rami/workspace/hierarchical_nw_align/Data/NAPAbench/8-way/CG_set/Family_1/A.net',
#                  '/home/rami/workspace/hierarchical_nw_align/Data/NAPAbench/8-way/CG_set/Family_1/B.net',
#                  '/home/rami/workspace/hierarchical_nw_align/Data/MCL/Score_Dir/SDF/A_B/Final_result/result.score.af')
  #print Utils.filter(out, Constants.EC_ICS_REGEX)