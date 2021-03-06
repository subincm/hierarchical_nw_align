import networkx as nx
import os
from sklearn.cluster import SpectralClustering
import Constants

def spectral_clustering(G, graph_name, num_clusters):
    #Find a way to figure out clusters number automatically
    subgraphs = []
    write_directory = os.path.join(Constants.SPECTRAL_PATH,graph_name)
    if not os.path.exists(write_directory):
        os.makedirs(write_directory)
    nodeList = G.nodes()
    matrix_data = nx.to_numpy_matrix(G, nodelist = nodeList)
    spectral = SpectralClustering(n_clusters=2,
                                          eigen_solver='arpack',
                                          affinity="rbf")   
    spectral.fit(matrix_data)
    label = spectral.labels_
    clusters = {}
    
    for nodeIndex, nodeLabel in enumerate(label):
        if nodeLabel not in clusters:
            clusters[nodeLabel] = []
        clusters[nodeLabel].append(nodeList[nodeIndex])
        
    #countNodes is used to test whether we have all the nodes in the clusters 
   
    for clusterIndex, subGraphNodes in enumerate(clusters.keys()):
        subgraph = G.subgraph(clusters[subGraphNodes])
        subgraphs.append(subgraph)
        nx.write_gexf(subgraph, os.path.join(write_directory,graph_name+str(clusterIndex)+"_I"+Constants.GEXF_FORMAT))
        #countNodes = countNodes + len(clusters[subGraphNodes])
    return subgraphs
    
