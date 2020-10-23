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
"""

from pyexcel_ods import get_data
import json
import re

urlRegExp = '(http[s]?|ftp)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
noteColNumber = 8
statusColNumber = 9

class Standard:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.url = None
        self.note = None
        self.refs = []
        self.referencedBy = []
        self.refNotes = {}
        self.status = None
    def extractURL(self):
        url = re.findall(urlRegExp, self.title)
        if len(url):
            pos = self.title.find(url[0])
            self.url = self.title[pos:]
            self.title = self.title[:pos - 2]

class ReferenceGraph:
    name = "ISO32000-2-DB"
    comment = None
    statusCount = {}
    standards = []
    
    def readFromODS(self, filename, sheetname):
        data = get_data(filename)[sheetname]
        self.readData(data)
        
    def readData(self, data) :
        dictionary = {}
        curIndex = -1
        numWithoutId = 0        
        self.comment = data[0][0]        

        for record in data:
            if not record: continue
            if record[0] != '':
                try:
                    id = int(record[0])
                    if record[1] in dictionary:
                        curIndex = dictionary[record[1]]
                        self.standards[curIndex].id = id
                    else:
                        curIndex = len(self.standards)
                        self.standards.append(Standard(id, record[1]))
                        dictionary[record[1]] = curIndex

                    if len(record) > noteColNumber and record[noteColNumber]:
                        self.standards[curIndex].note = record[noteColNumber]
                        
                    if len(record) > statusColNumber and record[statusColNumber]:
                        self.standards[curIndex].status = record[statusColNumber]
                        if record[statusColNumber] in self.statusCount:
                            self.statusCount[record[statusColNumber]] += 1
                        else:
                            self.statusCount[record[statusColNumber]] = 1

                except ValueError:
                    pass
            elif curIndex != -1 and record[1] != '':
                try:
                    float(record[1])
                    value = record[2]
                    if value in dictionary:
                        refIndex = dictionary[value]
                    else:
                        # reference with no id
                        refIndex = len(self.standards)
                        numWithoutId += 1
                        self.standards.append(Standard(-numWithoutId, value))
                        dictionary[value] = refIndex
                    self.standards[curIndex].refs.append(refIndex)
                    self.standards[refIndex].referencedBy.append(curIndex)     
                    
                    if len(record) > noteColNumber and record[noteColNumber]:
                        self.standards[curIndex].refNotes[refIndex] = record[noteColNumber]                    

                except ValueError:
                    pass
        self.extractData()
    
    def extractData(self):
        for standard in self.standards:
            for i, ref in enumerate(standard.refs):
                standard.refs[i] = self.standards[ref].id
            standard.refs.sort()
            for i, ref in enumerate(standard.referencedBy):
                standard.referencedBy[i] = self.standards[ref].id

            tmpNotes = {}
            for k in standard.refNotes:
                tmpNotes[self.standards[k].id] = standard.refNotes[k]
            standard.refNotes = tmpNotes

            standard.extractURL()
    
    def writeToJSON(self, filename):
        data = {}
        if self.comment:
            data["comment"] = self.comment
        data["statusCount"] = self.statusCount
        data[self.name] = []
        for standard in self.standards:
            record = {}
            record["id"] = standard.id
            record["title"] = standard.title
            if standard.url:
                record["url"] = standard.url
            if standard.status:
                record["status"] = standard.status
            record["refs"] = standard.refs
            record["referencedBy"] = standard.referencedBy
            if standard.note:
                record["note"] = standard.note
            if standard.refNotes:
                record["refsComments"] = standard.refNotes
            data[self.name].append(record)
        data[self.name].sort(key = lambda record : record["id"])
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent = 4)

refGraph = ReferenceGraph()
refGraph.readFromODS('Normative references tree for ISO 32000-2_2020.ods', 'Refs Tree')
refGraph.writeToJSON("referencesGraph.json")