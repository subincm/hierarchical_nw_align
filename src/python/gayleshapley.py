#!/usr/bin/python2.7
from __future__ import division
from collections import defaultdict

import networkx as nx
import pprint as pp
import Constants
import os
import itertools

# For more info, see https://en.wikipedia.org/wiki/Stable_marriage_problem
def stablemarriage(Kings, Queens, pref):
  kingsmatch = defaultdict(lambda: [])
  queensmatch = defaultdict(lambda: [])
  proposals = defaultdict(lambda: [])
  
  freekings = list(Kings)
  while len(kingsmatch.keys()) < len(Kings) and len(queensmatch.keys()) < len(Queens):  
    freeking = freekings[0]
  
    queen = max(pref[freeking], key = lambda x: -pref[freeking].index(x) if x not in proposals[freeking] else float('-inf'))    
  
    proposals[freeking].append(queen)
    if queen not in queensmatch:
      kingsmatch[freeking] = queen
      queensmatch[queen] = freeking
      freekings.remove(freeking)
    else:
      if freeking in pref[queen] and pref[queen].index(queensmatch[queen]) > pref[queen].index(freeking):
	freekings.append(queensmatch[queen])
	del kingsmatch[queensmatch[queen]]
	del queensmatch[queen]
      
	kingsmatch[freeking] = queen
	queensmatch[queen] = freeking
	freekings.remove(freeking)	
	
  if len(Kings) < len(Queens):
    for king in Kings:
      yield (king, kingsmatch.get(king, None))
  else:
    for queen in Queens:
      yield (queensmatch.get(queen, None), queen)

def getDistanceBetweenGraphs(G, H, _cache_ = {}):
  
  if G not in _cache_:
    if type(G) is str and G.endswith(Constants.GEXF_FORMAT):
      graph = nx.read_gexf(G)
      _cache_[G] = {}
      _cache_[G]['clustercoeff'] = nx.clustering(graph)
      _cache_[G]['nodes'] = graph.nodes()
    else:      
      graph = G
      _cache_[G] = {}
      _cache_[G]['clustercoeff'] = nx.clustering(graph)
      _cache_[G]['nodes'] = graph.nodes()
  
  if H not in _cache_:
    if type(H) is str and H.endswith(Constants.GEXF_FORMAT):
      graph = nx.read_gexf(H)
      _cache_[H] = {}
      _cache_[H]['clustercoeff'] = nx.clustering(graph)
      _cache_[H]['nodes'] = graph.nodes()
    else:      
      graph = H
      _cache_[H] = {}
      _cache_[H]['clustercoeff'] = nx.clustering(graph)
      _cache_[H]['nodes'] = graph.nodes()
      
  gc = _cache_[G]['clustercoeff']
  hc = _cache_[H]['clustercoeff']
  
  Kings = map(lambda x: 'G{0}'.format(str(x)), _cache_[G]['nodes'])
  Queens = map(lambda x: 'H{0}'.format(str(x)), _cache_[H]['nodes'])
  pref = defaultdict(lambda: [])
  
  for g in gc:
    for h in hc:
      dist = abs(gc[g] - hc[h])      
      pref['H{0}'.format(str(h))].append(('G{0}'.format(str(g)), dist))
      pref['G{0}'.format(str(g))].append(('H{0}'.format(str(h)), dist))
  
  for p in pref:
    pref[p].sort(key=lambda x: x[1])
    pref[p] = map(lambda x: x[0], pref[p])
    
  typecast = int if type(gc.keys()[0]) is int else str
  sm = 0
  for p in stablemarriage(Kings, Queens, pref):
    sm = sm + abs(gc[typecast(p[0][1:])] - hc[typecast(p[1][1:])])
  return sm

def getDistanceAndPairsFromSDF(sdf):
  A, B, prefs, nprefs = [], [], defaultdict(lambda: []), defaultdict(lambda: [])
  for line in open(sdf):
    a, b, d = line.split()
    if a not in A:
      A.append(a)
    if b not in B:
      B.append(b)
    prefs[a].append((b, float(d)))
    prefs[b].append((a, float(d)))
    
  for k in prefs.keys():    
    prefs[k].sort(key=lambda x: x[1])
    nprefs[k] = [x[0] for x in prefs[k]]   
    
  sm = 0
  pairs_to_return, pairs_to_sum = itertools.tee(stablemarriage(A, B, nprefs))   
  for pair in pairs_to_sum:
    for b_dist in prefs[pair[0]]:
      if pair[1] == b_dist[0]:
	sm = sm + b_dist[1]
	break
  return sm, pairs_to_return
    
def createClusterSDF(indir, ret = '/tmp/cluster.sdf'):  
  with open (ret, 'w') as f:
    for c in os.listdir(indir):
      if c == ".DS_Store":
          continue
      G, H = c.split('.')[0].split('_vs_')    
      d, pairs = getDistanceAndPairsFromSDF(os.path.join(indir, c))
      f.write('\t'.join(map(str, [G, H, d])) + '\n')
  return ret

if __name__ == '__main__':
  # Test for Gayle Shapely
  Kings = [('K1', 5), ('K2', 2), ('K3', 3)]
  Queens = [('Q1', 5), ('Q2', 1)]

  Kings.sort(key = lambda x: -x[1])
  Queens.sort(key = lambda x: -x[1])
  Kings = [k[0] for k in Kings]
  Queens = [q[0] for q in Queens]

  pref = {king: Queens for king in Kings}
  pref.update({queen: Kings for queen in Queens})
  for pair in stablemarriage(Kings, Queens, pref):
    print pair
    
  # Graph test for Gayle Shapely  
  G = nx.fast_gnp_random_graph(30, 0.4)
  H = nx.fast_gnp_random_graph(40, 0.2)  
  
  print getDistanceBetweenGraphs(G, H)