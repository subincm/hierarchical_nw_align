
import Constants
import Utils
import mcl_cluster
import kmeans_cluster
import dbscan_cluster





def letsStartAlgorithm():
    #Form networkx representation of both graphs
    G1 = Utils.convertNetToGefx(Constants.INPUT_FILE_NET_1)
    G2 = Utils.convertNetToGefx(Constants.INPUT_FILE_NET_2)
    
    #Run one of the first clustering algorithm
#     mcl_cluster.mcl_cluster(G1)
#     mcl_cluster.mcl_cluster(G2)

    #print("**************Run kmeans*****************")
    #Run kmeans
    kmeans_cluster.kmeans_cluster(G1, Constants.INPUT_FILE_1_NAME)
    #kmeans_cluster.kmeans_cluster(G2, Constants.INPUT_FILE_2_NAME)

    print("**************DBScan kmeans*****************")
    #Run dbscan
    dbscan_cluster.dbscan_cluster(G1, Constants.INPUT_FILE_1_NAME)
    #dbscan_cluster.dbscan_cluster(G2, Constants.INPUT_FILE_1_NAME)



if __name__ == '__main__':
    letsStartAlgorithm()
