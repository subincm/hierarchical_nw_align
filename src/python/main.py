#!/usr/bin/python2.7
import os
import Constants
import Utils
import mcl_cluster
import kmeans_cluster
import spectral_clustering
import generate_alignment
#import hungarian
#import compute_cluster_param
from collections import defaultdict
from gayleshapley import *
import subprocess
import hungarian
import compute_cluster_param


SDF_PATH="../../Data/GHOSTData.fixed/"
DATASETS_TYPE =["CG_SET","DMC_SET","DMR_SET"]
WAYS_TYPE = ["5-way","8-way"]
FAMILY_TYPE = ["Family_1", "Family_2", "Family_3", "Family_4","Family_5"]
def getMapOfGraphClusters():
  ret = defaultdict(lambda: [])
  for fgraph in os.walk(Constants.KMEANS_PATH):
    for fcluster in os.listdir(fgraph[0]):
      if fcluster.endswith(Constants.GEXF_FORMAT):
          ret[os.path.basename(fgraph[0])].append(os.path.join(os.path.dirname(fgraph[0]), os.path.basename(fgraph[0]),fcluster))
  return ret

def letsStartSpectralAlgorithm():
    #hungarian.Hungarian_algo()
    #Form networkx representation of both graphs
    subprocess.call("rm -rf ../../Data/SpectralC", shell=True)
    G1 = Utils.convertNetToGefx(Constants.INPUT_FILE_1 + Constants.NET_FORMAT)
    G2 = Utils.convertNetToGefx(Constants.INPUT_FILE_2 + Constants.NET_FORMAT)
    
    #Run one of the first clustering algorithm
#     mcl_cluster.mcl_cluster(G1)
#     mcl_cluster.mcl_cluster(G2)

    #print("**************Run kmeans*****************")
    #Run kmeans
    num_clusters1 = spectral_clustering.spectral_clustering(G1, Constants.INPUT_FILE_1_NAME)
    num_clusters2 = spectral_clustering.spectral_clustering(G2, Constants.INPUT_FILE_2_NAME)
    SDF_PATH = Utils.ComputeSpectralDistance(Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME, "SpectralC")

    #Find best Matching for our bipartite graph
    #Compute cluster parameters
    cluster_edge_weight_matrix = compute_cluster_param.find_cluster_edges_SDF(SDF_PATH, num_clusters1, num_clusters2)
    best_cluster_pairs = hungarian.Hungarian_algo(cluster_edge_weight_matrix)
    
    #Generate alignment score of our graphs
    generate_alignment.generate_alignment_score(best_cluster_pairs, "SpectralC", "SDF", Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME)

def letsStartKMeans(ways_type,dataset_type, family_type):
    #hungarian.Hungarian_algo()
    #Form networkx representation of both graphs
    subprocess.call("rm -rf ../../Data/KMeans", shell=True)
    INPUT_FILE_1 = os.path.join(Constants.NAPA_PATH, ways_type, dataset_type,family_type, Constants.INPUT_FILE_1_NAME )
    INPUT_FILE_2 = os.path.join(Constants.NAPA_PATH, ways_type, dataset_type,family_type, Constants.INPUT_FILE_2_NAME )
    G1 = Utils.convertNetToGefx(INPUT_FILE_1 + Constants.NET_FORMAT)
    G2 = Utils.convertNetToGefx(INPUT_FILE_2 + Constants.NET_FORMAT)

    #print("**************Run kmeans*****************")
    #Run kmeans
    for num_clusters in [8,20]:
        kmeans_cluster.kmeans_cluster(G1, Constants.INPUT_FILE_1_NAME, num_clusters)
        kmeans_cluster.kmeans_cluster(G2, Constants.INPUT_FILE_2_NAME, num_clusters)
        SDF_PATH = Utils.ComputeSpectralDistance(Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME, "Kmeans")
    
        #Find best Matching for our bipartite graph
        #Compute cluster parameters
        cluster_edge_weight_matrix = compute_cluster_param.find_cluster_edges_SDF(SDF_PATH, num_clusters, num_clusters)
        best_cluster_pairs = hungarian.Hungarian_algo(cluster_edge_weight_matrix)
        
        #Generate alignment score of our graphs
        generate_alignment.generate_alignment_score(best_cluster_pairs, "Kmeans", "SDF", INPUT_FILE_1,INPUT_FILE_2, Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME,
                                                    ways_type,dataset_type, family_type, num_clusters)

def letsStartMcl(ways_type,dataset_type, family_type):
  subprocess.call("rm -rf ../../Data/MCL", shell=True)
  INPUT_FILE_1 = os.path.join(Constants.NAPA_PATH, ways_type, dataset_type,family_type, Constants.INPUT_FILE_1_NAME )
  INPUT_FILE_2 = os.path.join(Constants.NAPA_PATH, ways_type, dataset_type,family_type, Constants.INPUT_FILE_2_NAME )
  for mcl_param in [1.35,1.40,1.45,1.50]:
      A_sg_dir = mcl_cluster.getMCLFromFile(INPUT_FILE_1+Constants.NET_FORMAT, '../../Data', mcl_param)
      B_sg_dir = mcl_cluster.getMCLFromFile(INPUT_FILE_2+Constants.NET_FORMAT, '../../Data', mcl_param)
      print Utils.ComputeSpectralDistance(A_sg_dir.split('/')[-1], B_sg_dir.split('/')[-1], "MCL")
      
      clustersdf = createClusterSDF('../../Data/MCL/SDF/A_B', '../../Data/MCL/SDF/A_B_cluster.sdf')
      d, best_cluster_pairs = getDistanceAndPairsFromSDF(clustersdf)
        
      best_cluster_pairs = [(pair[0][1:], pair[1][1:]) for pair in best_cluster_pairs]
      print best_cluster_pairs
      
      final_out = generate_alignment.generate_alignment_score(best_cluster_pairs, "MCL", "SDF", INPUT_FILE_1,INPUT_FILE_2, Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME,
                                                    ways_type,dataset_type, family_type, mcl_param)
                                                              
  


if __name__ == '__main__':
  for ways_type in WAYS_TYPE:
      for dataset_type in DATASETS_TYPE:
          for family_type in FAMILY_TYPE:
              print "ways =" + ways_type + " dataset_type =" + dataset_type + "family_type =" + family_type
              #letsStartKMeans(ways_type,dataset_type, family_type )
              letsStartMcl(ways_type,dataset_type, family_type)
              #letsStartSpectralAlgorithm()
#   #print Utils.getEdgeCorrectness('/home/rami/workspace/hierarchical_nw_align/Data/NAPAbench/8-way/CG_set/Family_1/A.net',
#                  '/home/rami/workspace/hierarchical_nw_align/Data/NAPAbench/8-way/CG_set/Family_1/B.net',
#                  '/home/rami/workspace/hierarchical_nw_align/Data/MCL/Score_Dir/SDF/A_B/Final_result/result.score.af')
  #print Utils.filter(out, Constants.EC_ICS_REGEX)