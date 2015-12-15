
import Utils
import os
import Constants
import subprocess

def generate_alignment_score(best_cluster_pairs,clusterAlgoName, distAlgoName, networkName1, networkName2):
    
    SCORE_DIR = os.path.join("../../Data", clusterAlgoName, Constants.FINAL_SCORE_DIR, distAlgoName, networkName1+"_"+networkName2)
    if not os.path.exists(SCORE_DIR):
        os.makedirs(SCORE_DIR)
    RESULT_LOG_DIR =  os.path.join("../..", Constants.FINAL_RESULT, clusterAlgoName ,distAlgoName, Constants.DATASET_USED) 
    if not os.path.exists(RESULT_LOG_DIR):
        os.makedirs(RESULT_LOG_DIR)
    for cluster1,cluster2 in best_cluster_pairs:
        RESULT_LOG_FILE = os.path.join(RESULT_LOG_DIR, str(cluster1)+"_"+str(cluster2)+"_"+Constants.RESULT_LOG_FILE)
        subgraph1Path = os.path.join("../../Data", clusterAlgoName, networkName1, networkName1+str(cluster1) + Constants.GEXF_FORMAT)
        subgraph2Path = os.path.join("../../Data", clusterAlgoName, networkName2, networkName2+str(cluster2)  +  Constants.GEXF_FORMAT)
        print subgraph1Path, '-'*10
        print subgraph2Path, '-'*10
        cfg_file = Utils.generateCfgFile (subgraph1Path, subgraph2Path, dumpDistances=False, dumpSignatures=False,
                     sigs1=None, sigs2=None)
        #subprocess.call([Constants.GHOST_PATH, "-c", cfg_file, "|","tee",RESULT_LOG_FILE])
        cmd = Constants.GHOST_PATH + " -c "+ cfg_file + " | tee "+ RESULT_LOG_FILE
        os.system(cmd)
        subprocess.call("mv *sdf "+SCORE_DIR, shell=True)
        subprocess.call("mv *gz "+SCORE_DIR, shell=True)
        subprocess.call("mv *af "+SCORE_DIR, shell=True)
        pass
    
    #Concatenate different cluster mapping into one
    FINAL_SCORE_DIR = os.path.join(SCORE_DIR,Constants.FINAL_RESULT)
    if not os.path.exists(FINAL_SCORE_DIR):
        os.makedirs(FINAL_SCORE_DIR)
    final_text = ""
    for file in os.listdir(SCORE_DIR):
        if file.endswith(".af"):
            read_file = open(os.path.join(SCORE_DIR,file))
            final_text = final_text + read_file.read()
    final_align_file_path = os.path.join(FINAL_SCORE_DIR,Constants.RESULT_FILE)
    write_file = open(final_align_file_path, 'w+')
    write_file.write(final_text)
    
    #Check whether gexf file exists or not
    graph1Path = Constants.INPUT_FILE_1 + Constants.GEXF_FORMAT
    graph2Path = Constants.INPUT_FILE_2 + Constants.GEXF_FORMAT
    if os.path.isfile(graph1Path) is False:
        Utils.convertNetToGefx(Constants.INPUT_FILE_1 + Constants.NET_FORMAT)
    if os.path.isfile(graph2Path) is False:
        Utils.convertNetToGefx(Constants.INPUT_FILE_2 + Constants.NET_FORMAT)
        
    #Generate Prof score
    RESULT_LOG_FILE = os.path.join(RESULT_LOG_DIR, Constants.PROF+"_"+Constants.RESULT_LOG_FILE)
    cfg_file = Utils.generateCfgFile (graph1Path, graph2Path, dumpDistances=False, dumpSignatures=False,
                     sigs1=None, sigs2=None)
    cmd = Constants.GHOST_PATH + " -c "+ cfg_file + " | tee "+ RESULT_LOG_FILE
    os.system(cmd)
    
    #Generate our Final score
    RESULT_LOG_FILE = os.path.join(RESULT_LOG_DIR, Constants.OURS+"_"+Constants.RESULT_LOG_FILE)           
    Utils.getEdgeCorrectness(graph1Path, graph2Path, final_align_file_path, RESULT_LOG_FILE)
