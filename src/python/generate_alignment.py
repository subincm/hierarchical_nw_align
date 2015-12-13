
import Utils
import os
import Constants
import subprocess

def generate_alignment_score(best_cluster_pairs,clusterAlgoName, distAlgoName, networkName1, networkName2):
    
    SCORE_DIR = os.path.join("../../Data", clusterAlgoName, Constants.FINAL_SCORE_DIR, distAlgoName, networkName1+"_"+networkName2)
    if not os.path.exists(SCORE_DIR):
        os.makedirs(SCORE_DIR)
    for cluster1,cluster2 in best_cluster_pairs:
        subgraph1Path = os.path.join("../../Data", clusterAlgoName, networkName1, networkName1+str(cluster1) + Constants.GEXF_FORMAT)
        subgraph2Path = os.path.join("../../Data", clusterAlgoName, networkName2, networkName2+str(cluster2)  +  Constants.GEXF_FORMAT)
        cfg_file = Utils.generateCfgFile (subgraph1Path, subgraph2Path, dumpDistances=False, dumpSignatures=False,
                     sigs1=None, sigs2=None)
        subprocess.call([Constants.GHOST_PATH, "-c", cfg_file])
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
    
    write_file = open(os.path.join(FINAL_SCORE_DIR,Constants.RESULT_FILE),'w+')
    write_file.write(final_text)
    
                
        