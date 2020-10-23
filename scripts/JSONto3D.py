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
// Generates a 3D/VR visualization JSON file for use with "3D Force-graph"
// from the "referencesGraph.json" file.
//
// See https://github.com/vasturiano/3d-force-graph/ 
//
// Author: Peter Wyatt
"""
import json

jfile    = open("referencesGraph.json")
indata   = json.load(jfile)
normrefs = indata["ISO32000-2-DB"]

nodes = []
for doc in normrefs:
    n = {}
    n["id"]        = doc["id"]
    n["name"]      = doc["title"]
    # n["nOutLinks"] = len(doc["refs"])
    # n["nInLinks"]  = len(doc["referencedBy"])
    # Size of planet node is proportional to the square of the number of out-going references
    n["val"] = len(doc["refs"]) * len(doc["refs"])
    # Short name is everything before a COMMA (normally the ISO document number or simple title)
    #   then trimmed before a COLON (which will strip off ISO years but so be it!) 
    s = doc["title"].split(",")
    s = s[0].split(":")
    n["short"] = s[0]
    # Make PDF 2.0 the large red centre of the 3D universe!
    # otherwise rough grouping (and thus color coding of node) based on title
    if (doc["id"] == 0):
        n["group"] = "PDF2"
    elif ("ISO" in doc["title"]) or ("IEC" in doc["title"]):
        n["group"] = "ISO"
    elif ("W3C" in doc["title"]) or ("RFC" in doc["title"]) or ("IETF" in doc["title"]) or ("World Wide Web" in doc["title"]):
        n["group"] = "W3C"
    elif ("Adobe" in doc["title"]):
        n["group"] = "Adobe"
    elif ("Unicode" in doc["title"]):
        n["group"] = "Unicode"
    else:
        n["group"] = "Other"
    nodes.append(n)
    
links = []
for doc in normrefs:
    refs = []
    refs = doc["refs"]
    for ref in refs:
        lnk = {}
        lnk["source"] = doc["id"]   
        lnk["target"] = ref   
        # Make all 1st order links from PDF 2.0 red
        # otherwise do rough grouping (and thus color coding of link) based on source title
        if (doc["id"] == 0):
            # Make PDF 2.0 the large red centre of the 3D universe
            lnk["group"] = "PDF2"
            lnk["color"] = "red"
        elif ("ISO" in doc["title"]) or ("IEC" in doc["title"]):
            lnk["group"] = "ISO"
        elif ("W3C" in doc["title"]) or ("RFC" in doc["title"]) or ("IETF" in doc["title"]) or ("World Wide Web" in doc["title"]):
            lnk["group"] = "W3C"
        elif ("Adobe" in doc["title"]):
            lnk["group"] = "Adobe"
        elif ("Unicode" in doc["title"]):
            lnk["group"] = "Unicode"
        else:
            lnk["group"] = "Other"
        # 'desc' attribute is what links display below their label (default attribute 'name') but in smaller text
        # This text is too long and makes for too much... need short friendly names for documents!
        # lnk_doc = next(r for r in normrefs if r["id"] == ref)
        # lnk["desc"] = "From " + doc["title"] + " to " + lnk_doc["title"]
        links.append(lnk)

outdata = {}
outdata["nodes"] = nodes
outdata["links"] = links
with open("pdf20-norm-refs.json", 'w') as outfile:
    json.dump(outdata, outfile, indent=4)
