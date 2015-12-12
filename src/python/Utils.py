import Constants
import networkx as nx





def convertNetToGefx(input_file):
    G = None
    if input_file.endswith(Constants.GEXF_FORMAT):
        G = nx.read_gexf(input_file, None, True)
        nx.write_gexf(G, input_file)
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