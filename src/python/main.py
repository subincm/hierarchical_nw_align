
import Constants
import Utils
import mcl_cluster
import kmeans_cluster
import dbscan_cluster
#import hungarian
import compute_cluster_param

SDF_PATH="../../Data/GHOSTData.fixed/"


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
    dbscan_cluster.dbscan_cluster(G1, Constants.INPUT_FILE_1_NAME)
    dbscan_cluster.dbscan_cluster(G2, Constants.INPUT_FILE_1_NAME)

    #Compute cluster parameters
    filelist=compute_cluster_param.listfiles(SDF_PATH)
    for f in filelist:
         print(f)
         print("avg:",compute_cluster_param.compute_average(f))

if __name__ == '__main__':
    letsStartAlgorithm()
