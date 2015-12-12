import os
import string as str
from os import path,walk
from os import listdir
from os.path import isfile, join

SDF_PATH="../../Data/GHOSTData.fixed/"
filepath="../../Data/GHOSTData.fixed/cjejuni_vs_ecoli.sdf"

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

