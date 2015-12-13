import Constants
import networkx as nx
import subprocess
import os

def convertNetToGefx(input_file):
    G = None
    if input_file.endswith(Constants.GEXF_FORMAT):
        G = nx.read_gexf(input_file, None, True)
    elif input_file.endswith(Constants.NET_FORMAT):
        G=nx.Graph()
        f = file(input_file, 'r')
        # iterate over the lines in the file
        for line in f:
            # split the line into a list of column values
            columns = line.split('\t')
            # clean any whitespace off the items
            columns = [col.strip() for col in columns]
            if columns:
                G.add_edge(columns[0], columns[1])
        #write to a gexf file, so that GHOST can read it as well
        gexf_path = input_file[:-len(Constants.NET_FORMAT)]+Constants.GEXF_FORMAT
        #add attributes to nodes in gefx file
        for n,d in G.nodes_iter(data=True):
            G.node[n]["id"] = n
            G.node[n]["gname"] = n
        nx.write_gexf(G, gexf_path)
    else:
        print("Unsupported Format")
        exit(0)
    print("For "+input_file+" Number of Nodes =", G.number_of_nodes(), "No of edges = ", G.number_of_edges())

    return G

def ComputeSpectralDistance(graph_name1, graph_name2, algo):
    subgraph1Path = os.path.join("../../Data", algo, graph_name1)
    subgraph2Path = os.path.join("../../Data", algo, graph_name2)
    assert(os.path.exists(subgraph1Path))
    assert(os.path.exists(subgraph2Path))

    SDF_DIRECTORY = os.path.join("../../Data", algo, "SDF")
    if not os.path.exists(SDF_DIRECTORY):
        os.makedirs(SDF_DIRECTORY)

    SDF_A_B_DIRECTORY = os.path.join(SDF_DIRECTORY, graph_name1+"_"+graph_name2)
    if not os.path.exists(SDF_A_B_DIRECTORY):
        os.makedirs(SDF_A_B_DIRECTORY)

    #Compute the spectral signatures first for all the subgraphs of a graph
    for path in [subgraph1Path, subgraph2Path]:
        subgraphFiles = os.listdir(path)
        for f1 in subgraphFiles:
            network1 = os.path.join(path, f1)
            network2 = os.path.join(path, f1)
            cfg_file = generateCfgFile(network1, network2, dumpSignatures=True)
            subprocess.call([Constants.GHOST_PATH, "-c", cfg_file])
        subprocess.call("mv *gz "+path, shell=True)


    subgraph1Files = os.listdir(subgraph1Path)
    subgraph2Files = os.listdir(subgraph2Path)

    for f1 in subgraph1Files:
        if f1.endswith(Constants.GEXF_FORMAT):
            network1 = os.path.join(subgraph1Path, f1)
            sigs1 = os.path.join(subgraph1Path, f1[:-len(Constants.GEXF_FORMAT)]+".sig.gz")
            for f2 in subgraph2Files:
                if f2.endswith(Constants.GEXF_FORMAT):
                    network2 = os.path.join(subgraph2Path, f2)
                    sigs2 = os.path.join(subgraph2Path, f2[:-len(Constants.GEXF_FORMAT)]+".sig.gz")
                    cfg_file = generateCfgFile(network1, network2, dumpDistances=True,sigs1=sigs1, sigs2=sigs2)
                    subprocess.call([Constants.GHOST_PATH, "-c", cfg_file])
    subprocess.call("mv *sdf "+SDF_A_B_DIRECTORY, shell=True)
    return SDF_A_B_DIRECTORY

def generateCfgFile (network1, network2, dumpDistances=False, dumpSignatures=False,
                     sigs1=None, sigs2=None):

    cfg_file = "/tmp/napa.cfg"
    with open (cfg_file, 'w') as f:
        f.write ('[main]\n')
        f.write("network1: "+network1+'\n')
        f.write("network2: "+network2+'\n')
        if not sigs1 is None:
            f.write("sigs1: "+sigs1+'\n')
        if not sigs2 is None:
            f.write("sigs2: "+sigs2+'\n')
        if dumpDistances is True:
            f.write("dumpDistances: true\n")
        elif dumpSignatures is True:
            f.write("dumpSignatures: true\n")

    return cfg_file