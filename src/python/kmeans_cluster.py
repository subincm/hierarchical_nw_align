import networkx as nx
import os
from sklearn.cluster import KMeans
import Constants

def kmeans_cluster(G, graph_name):
    #Find a way to figure out clusters number automatically
    num_clusters = 8
    write_directory = os.path.join(Constants.KMEANS_PATH,graph_name)
    if not os.path.exists(write_directory):
        os.makedirs(write_directory)
    nodeList = G.nodes()
    matrix_data = nx.to_numpy_matrix(G, nodelist = nodeList)
    kmeans = KMeans(init='k-means++', n_clusters=num_clusters, n_init=10)   
    kmeans.fit(matrix_data)
    label = kmeans.labels_
    clusters = {}
    
    for nodeIndex, nodeLabel in enumerate(label):
        if nodeLabel not in clusters:
            clusters[nodeLabel] = []
        clusters[nodeLabel].append(nodeList[nodeIndex])
        
    #countNodes is used to test whether we have all the nodes in the clusters 
    countNodes = 0    
    for clusterIndex, subGraphNodes in enumerate(clusters.keys()):
        subgraph = G.subgraph(clusters[subGraphNodes])
        nx.write_gexf(subgraph, os.path.join(write_directory,graph_name+str(clusterIndex)+Constants.GEXF_FORMAT))
        #countNodes = countNodes + len(clusters[subGraphNodes])
        pass
    return num_clusters
