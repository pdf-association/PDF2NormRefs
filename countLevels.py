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
// Counts reference levels relative to any document (not necessarily ISO 32000-2). 
//
// Usage:  <infilename> <outfilename> <id>
//
// where:
//   infilename  is the JSON with the references
//   outfilename is the JSON with the count results
//   id          is the root document ID for counting (0 means ISO 32000-2)
//
"""

import json
from collections import deque
import sys

def extractGraph(filename):
    with open(filename) as json_file:
        data = json.load(json_file)["ISO32000-2-DB"]
        graph = {}
        for standard in data:
            graph[standard['id']] = standard['refs']
        return graph
    
def countLevels(graph, recordId):
    dist = {recordId : 0}
    q = deque()
    q.append(recordId)
    while q:
        cur = q.popleft()
        for nbr in graph[cur]:
            if nbr not in dist:
                dist[nbr] = dist[cur] + 1
                q.append(nbr)
    levels = {}
    for item in dist:
        d = dist[item]
        if d in levels:
            levels[d] += 1
        else:
            levels[d] = 1
    return levels

infilename = sys.argv[1]
outfilename = sys.argv[2]
requestId = int(sys.argv[3])

graph = extractGraph(infilename)
levels = countLevels(graph, requestId)
data = {}
data['id'] = requestId
data['levelsCount'] = levels
with open(outfilename, 'w') as outfile:
    json.dump(data, outfile, indent = 4)
    
    
    