# -*- coding: utf-8 -*-
"""
// Copyright 2020 PDF Association, Inc. https://www.pdfa.org
//
// This material is based upon work supported by the Defense Advanced 
// Research Projects Agency (DARPA) under Contract No. HR001119C0079. 
// Any opinions, findings and conclusions or recommendations expressed
// in this material are those of the author(s) and do not necessarily
// reflect the views of the Defense Advanced Research Projects Agency 
// (DARPA). Approved for public release.
//
// SPDX-License-Identifier: Apache-2.0
//
// Collects various statistics of the graph including:
// - The distribution of the references by distance (so called reference level) from the root node
// - The distribution of the references by the status
// - The count of the references by SDOs
// - Top N references with maximal number of referenced documents
// - Top M references with the maximal number of documents referencing them (=incoming edges)
//
// Usage:  <infilename> <outfilename> <id> <N> <M>
//
// where:
//   infilename  is the JSON with the references
//   outfilename is the JSON with the count results
//   id          is the root document ID for counting docs by the level (0 means ISO 32000-2)
//	 N           is the number of top N docs with maximal number of refs
//   M           is the number of top M referenced docs
//
"""

import json
from collections import deque
import sys

def extractGraph(filename):
    with open(filename) as json_file:
        data = json.load(json_file)["ISO32000_2_DB"]
        graph = [{}, {}, {}, {}]
        refGraph = graph[0]
        dualGraph = graph[1]
        orgsCounter = graph[2]
        statusCounter = graph[3]
        noOrgs = []
		
        for standard in data:
            refGraph[standard['id']] = standard['refs']
            dualGraph[standard['id']] = standard['referencedBy']
            
            if 'status' in standard:
                status = standard['status']
                if status in statusCounter:
                    statusCounter[status] += 1
                else:
                    statusCounter[status] = 1
			
            if 'orgs' in standard and standard['orgs']:
                for org in standard['orgs']:
                    orgName = org['org']
                    if orgName in orgsCounter:
                        orgsCounter[orgName] += 1
                    else:
                        orgsCounter[orgName] = 1
            else:
                noOrgs.append(standard['id'])
		
        orgsCounter['noOrgs'] = noOrgs		
        return graph

def findTopRefs(graph, N):
    refCounter = {}
    for item in graph:
        refCounter[item] = len(graph[item])
    topN = {k: v for k, v in sorted(refCounter.items(), key = lambda item: item[1], reverse = True)[:N]}
    return topN

def countDistances(graph, recordId):
    dist = {recordId : 0}
    q = deque()
    q.append(recordId)
    while q:
        cur = q.popleft()
        for nbr in graph[cur]:
            if nbr not in dist:
                dist[nbr] = dist[cur] + 1
                q.append(nbr)
    return dist

def countLevels(graph, dist):
    levels = {}
    for item in dist:
        d = dist[item]
        if d in levels:
            levels[d] += 1
        else:
            levels[d] = 1
    return levels

def getDisconnectedComponent(graph, dist):
    disComponent = []
    for item in graph:
        if item not in dist:
            disComponent.append(item)
    return disComponent

infilename = sys.argv[1]
outfilename = sys.argv[2]
requestId = int(sys.argv[3])
NMaxRef = int(sys.argv[4])
NMaxRefBy = int(sys.argv[5])

graph = extractGraph(infilename)
refGraph = graph[0]
dualGraph = graph[1]
orgsCounter = graph[2]
statusCounter = graph[3]
dist = countDistances(refGraph, requestId)
levels = countLevels(refGraph, dist)
disComponent = getDisconnectedComponent(refGraph, dist)

topRefs = findTopRefs(refGraph, NMaxRef)
topRefsBy = findTopRefs(dualGraph, NMaxRefBy)

data = {}
data['id'] = requestId
data['levelsCount'] = levels
data['disconnectedComponent'] = disComponent
data['statusDistribution'] = statusCounter
data['orgsDistribution'] = orgsCounter
data["topRefsNr"] = topRefs
data["topReferencedBy"] = topRefsBy
with open(outfilename, 'w') as outfile:
    json.dump(data, outfile, indent = 4)
    
    
    