
import networkx as nx
import os
from sklearn.cluster import DBSCAN
import Constants

DBSCAN_PATH = "../../Data/DBScan"

def dbscan_cluster(G, graph_name):
    write_directory = os.path.join(DBSCAN_PATH,graph_name)
    if not os.path.exists(write_directory):
        os.makedirs(write_directory)
    nodeList = G.nodes()
    matrix_data = nx.to_numpy_matrix(G, nodelist = nodeList)
    #kmeans = KMeans(init='k-means++', n_clusters=8, n_init=10)
    #kmeans.fit(matrix_data)
    #label = kmeans.labels_
    #print(matrix_data)

    # Compute DBSCAN
    db = DBSCAN(eps=1, min_samples=2).fit(matrix_data)
    #core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    #core_samples_mask[db.core_sample_indices_] = True
    label = db.labels_
    clusters = {}

    for nodeIndex, nodeLabel in enumerate(label):
        if nodeLabel not in clusters:
            clusters[nodeLabel] = []
        clusters[nodeLabel].append(nodeList[nodeIndex])
    
    #print(label)
    #print("clusters",clusters)    

    #countNodes is used to test whether we have all the nodes in the clusters
    countNodes = 0
    for clusterIndex, subGraphNodes in enumerate(clusters.keys()):
        subgraph = G.subgraph(clusters[subGraphNodes])
        nx.write_gexf(subgraph, os.path.join(write_directory,graph_name+str(clusterIndex)+Constants.GEXF_FORMAT))
        #countNodes = countNodes + len(clusters[subGraphNodes])
        pass
    pass
