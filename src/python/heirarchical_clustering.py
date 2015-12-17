import subprocess
import spectral_clustering
import Constants
import Utils
import compute_cluster_param
import hungarian
import os
import networkx as nx
import generate_alignment
import kmeans_cluster

def heirarchical_clustering_spec(G1, G2, num_alignment_pairs,SDF_PATH,num_clusters, ways_type,dataset_type, family_type ):
    subprocess.call("rm -rf "+SDF_PATH, shell=True)
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
                num_alignment_pairs = heirarchical_clustering_spec(newG1, newG2, num_alignment_pairs,SDF_PATH,num_clusters,
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
    return num_alignment_pairs

def heirarchical_clustering_kmeans(G1, G2, num_alignment_pairs,SDF_PATH,num_clusters, ways_type,dataset_type, family_type ):
    subprocess.call("rm -rf "+SDF_PATH, shell=True)
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
                num_alignment_pairs = heirarchical_clustering_kmeans(newG1, newG2, num_alignment_pairs,SDF_PATH,num_clusters,
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
    return num_alignment_pairs