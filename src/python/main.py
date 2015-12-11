
import Constants
import Utils
import mcl_cluster







def letsStartAlgorithm():
    #Form networkx representation of both graphs
    G1 = Utils.convertNetToGefx(Constants.INPUT_FILE_NET_1)
    G2 = Utils.convertNetToGefx(Constants.INPUT_FILE_NET_2)
    
    #Run one of the first clustering algorithm
    mcl_cluster.mcl_cluster(G1)
    mcl_cluster.mcl_cluster(G2)





if __name__ == '__main__':
    letsStartAlgorithm()