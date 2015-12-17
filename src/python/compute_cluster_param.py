import os
import string as str
from os import path,walk
from os import listdir
from os.path import isfile, join
import re

SDF_PATH="../../Data/GHOSTData.fixed/"
filepath="../../Data/GHOSTData.fixed/cjejuni_vs_ecoli.sdf"


def find_cluster_edges_SDF(SDF_PATH, num_clusters1, num_clusters2):
	
	#Hard code SDF_PATH for now. Comment this once we are running algorithm normally
	#SDF_PATH = "/Users/neocfc/Documents/workspace/Compbio/project/hierarchical_nw_align/Data/Kmeans/SDF/A_B"
	#Initialize the bipartite graph of clusters edge weight matrix
	cluster_edge_weight_matrix = [[0 for i in range(num_clusters1)] for j in range(num_clusters2)]
	filelist=listfiles(SDF_PATH)
	for f in filelist:
		try:
			filename = f.rsplit("/")[-1]
			splitOn = filename.split("_")
			cluster1Index = int(splitOn[0][1])
			cluster2Index = int(splitOn[2][1])
			avg_similarity = compute_average(f)
			
			cluster_edge_weight_matrix[cluster1Index][cluster2Index] = avg_similarity
		except Exception, ex:
			pass
	return cluster_edge_weight_matrix

def find_cluster_spectraledges_SDF(SDF_PATH, num_clusters1, num_clusters2):
	
	#Hard code SDF_PATH for now. Comment this once we are running algorithm normally
	#SDF_PATH = "/Users/neocfc/Documents/workspace/Compbio/project/hierarchical_nw_align/Data/Kmeans/SDF/A_B"
	#Initialize the bipartite graph of clusters edge weight matrix
	cluster_edge_weight_matrix = [[0 for i in range(num_clusters1)] for j in range(num_clusters2)]
	filelist=listfiles(SDF_PATH)
	for f in filelist:
		try:
			filename = f.rsplit("/")[-1]
			splitOn = filename.split("_")
			cluster1Index = int(splitOn[0][1])
			cluster2Index = int(splitOn[2][1])
			avg_similarity = compute_average(f)
			
			cluster_edge_weight_matrix[cluster1Index][cluster2Index] = avg_similarity
		except Exception, ex:
			pass
	return cluster_edge_weight_matrix
	
def listfiles(path):
	filelist=[]
	for (dirpath, dirnames, filenames) in walk(path):
		for fname in filenames:
			filepath=os.path.join(path,fname)
			if isfile(filepath) and fname.endswith('.sdf'):
				#print(filepath)
				filelist.append(filepath)
	return filelist

def compute_average(filepath):
	sum=0.0
	count=0
	with open(filepath, "r") as f:
		for line in f:
			count+=1
			#print(line)
			sum+=float(line.split()[2])
	avg=sum/count
	#print(avg)
	return avg		

if __name__ == '__main__':
	filelist=listfiles(SDF_PATH)
	for f in filelist:
		print(f)
		print("avg:",compute_average(f))

