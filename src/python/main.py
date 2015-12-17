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
import heirarchical_clustering

SDF_PATH="../../Data/GHOSTData.fixed/"
DATASETS_TYPE =["CG_set"]
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
    INPUT_FILE_1 = os.path.join(Constants.NAPA_PATH, ways_type, dataset_type,family_type, Constants.INPUT_FILE_1_NAME )
    INPUT_FILE_2 = os.path.join(Constants.NAPA_PATH, ways_type, dataset_type,family_type, Constants.INPUT_FILE_2_NAME )
    G1 = Utils.convertNetToGefx(INPUT_FILE_1 + Constants.NET_FORMAT)
    G2 = Utils.convertNetToGefx(INPUT_FILE_2 + Constants.NET_FORMAT)
    num_alignment_pairs = 0
    #Run Spectral
    num_clusters = 4
    
    #Do initial clustering
    subgraphs1 = spectral_clustering.spectral_clustering(G1, Constants.INPUT_FILE_1_NAME, num_clusters)
    subgraphs2 = spectral_clustering.spectral_clustering(G2, Constants.INPUT_FILE_2_NAME, num_clusters)
         
    #Does SDF on those clusters. Does not need to do it on all clusters because some might already be fixed
    SDF_PATH = Utils.ComputeSpectralDistance(Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME, "SpectralC")
        
    #Find best Matching for our bipartite graph
    #Compute cluster parameters
    cluster_edge_weight_matrix = compute_cluster_param.find_cluster_spectraledges_SDF(SDF_PATH, num_clusters, num_clusters)
    best_cluster_pairs = hungarian.Hungarian_algo(cluster_edge_weight_matrix)
    for cluster1,cluster2 in best_cluster_pairs:
            newG1 = subgraphs1[cluster1]
            newG2 = subgraphs2[cluster2]
            if len(newG1.nodes()) >= 900 and  len(newG2.nodes()) >= 900:
                #Write these two graphs gefx files
                #nx.write_gexf(newG1, "../../Data/SpectralC/HC/A.gexf")
                #nx.write_gexf(newG2, "../../Data/SpectralC/HC/B.gexf")
                #Cluster these further
                num_alignment_pairs = heirarchical_clustering.heirarchical_clustering_spec(newG1, newG2, num_alignment_pairs,SDF_PATH,num_clusters,
                                                                                      ways_type,dataset_type, family_type )    
            else:
                #Simply generate alignment file for graph
                #Generate alignment score of our cluster graphs
                
                heirarchical_dir = "../../Data/SpectralC/IntermC"
                if os.path.exists(heirarchical_dir):
                    subprocess.call("rm -rf "+heirarchical_dir, shell=True)
                os.makedirs(heirarchical_dir)
                
                subgraphpath1 = os.path.join(heirarchical_dir,"A_"+str(num_alignment_pairs)+".gexf")
                subgraphpath2 = os.path.join(heirarchical_dir,"B_"+str(num_alignment_pairs)+".gexf")
                nx.write_gexf(newG1, subgraphpath1)
                nx.write_gexf(newG2, subgraphpath2)
                generate_alignment.generate_spectralcluster_alignment_score(subgraphpath1, subgraphpath2, "SpectralC", "SDF",
                             ways_type,dataset_type, family_type, num_clusters, num_alignment_pairs)
                num_alignment_pairs = num_alignment_pairs + 1
    #Give final output
    generate_alignment.generateSpectralFinalScore(INPUT_FILE_1, INPUT_FILE_2,ways_type,dataset_type, family_type, num_clusters )

def letsStartHeiKmeans(ways_type,dataset_type, family_type):
    
    INPUT_FILE_1 = os.path.join(Constants.NAPA_PATH, ways_type, dataset_type,family_type, Constants.INPUT_FILE_1_NAME )
    INPUT_FILE_2 = os.path.join(Constants.NAPA_PATH, ways_type, dataset_type,family_type, Constants.INPUT_FILE_2_NAME )
    G1 = Utils.convertNetToGefx(INPUT_FILE_1 + Constants.NET_FORMAT)
    G2 = Utils.convertNetToGefx(INPUT_FILE_2 + Constants.NET_FORMAT)
    
    #Run Kmeans
    for num_clusters in [2,4,6,8]:
        num_alignment_pairs = 0
        subprocess.call("rm -rf ../../Data/KmeansH", shell=True)
        subgraphs1 = kmeans_cluster.kmeansh_cluster(G1, Constants.INPUT_FILE_1_NAME, num_clusters)
        subgraphs2 = kmeans_cluster.kmeansh_cluster(G2, Constants.INPUT_FILE_2_NAME, num_clusters)
             
        #Does SDF on those clusters. Does not need to do it on all clusters because some might already be fixed
        SDF_PATH = Utils.ComputeSpectralDistance(Constants.INPUT_FILE_1_NAME, Constants.INPUT_FILE_2_NAME, "KmeansH")
            
        #Find best Matching for our bipartite graph
        #Compute cluster parameters
        cluster_edge_weight_matrix = compute_cluster_param.find_cluster_spectraledges_SDF(SDF_PATH, num_clusters, num_clusters)
        best_cluster_pairs = hungarian.Hungarian_algo(cluster_edge_weight_matrix)
        for cluster1,cluster2 in best_cluster_pairs:
                newG1 = subgraphs1[cluster1]
                newG2 = subgraphs2[cluster2]
                if len(newG1.nodes()) >= 50 and  len(newG2.nodes()) >= 50:
                    #Write these two graphs gefx files
                    #nx.write_gexf(newG1, "../../Data/SpectralC/HC/A.gexf")
                    #nx.write_gexf(newG2, "../../Data/SpectralC/HC/B.gexf")
                    #Cluster these further
                    num_alignment_pairs = heirarchical_clustering.heirarchical_clustering_kmeans(newG1, newG2, num_alignment_pairs,SDF_PATH,num_clusters,
                                                                                          ways_type,dataset_type, family_type )    
                else:
                    #Simply generate alignment file for graph
                    #Generate alignment score of our cluster graphs
                    
                    heirarchical_dir = "../../Data/KmeansH/IntermC"
                    if os.path.exists(heirarchical_dir):
                        subprocess.call("rm -rf "+heirarchical_dir, shell=True)
                    os.makedirs(heirarchical_dir)
                    
                    subgraphpath1 = os.path.join(heirarchical_dir,"A_"+str(num_alignment_pairs)+".gexf")
                    subgraphpath2 = os.path.join(heirarchical_dir,"B_"+str(num_alignment_pairs)+".gexf")
                    nx.write_gexf(newG1, subgraphpath1)
                    nx.write_gexf(newG2, subgraphpath2)
                    generate_alignment.generate_kmeanscluster_alignment_score(subgraphpath1, subgraphpath2, "KmeansH", "SDF",
                                 ways_type,dataset_type, family_type, num_clusters, num_alignment_pairs)
                    num_alignment_pairs = num_alignment_pairs + 1
        #Give final output
        generate_alignment.generatekmeansFinalScore(INPUT_FILE_1, INPUT_FILE_2,ways_type,dataset_type, family_type, num_clusters )
    
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
              #letsStartMcl(ways_type,dataset_type, family_type)
              #letsStartSpectralAlgorithm()
              letsStartHeiKmeans(ways_type,dataset_type, family_type)
#   #print Utils.getEdgeCorrectness('/home/rami/workspace/hierarchical_nw_align/Data/NAPAbench/8-way/CG_set/Family_1/A.net',
#                  '/home/rami/workspace/hierarchical_nw_align/Data/NAPAbench/8-way/CG_set/Family_1/B.net',
#                  '/home/rami/workspace/hierarchical_nw_align/Data/MCL/Score_Dir/SDF/A_B/Final_result/result.score.af')
  #print Utils.filter(out, Constants.EC_ICS_REGEX)