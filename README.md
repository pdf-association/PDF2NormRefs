# **ISO/DIS 32000-2 (PDF 2.0) Normative References Tree**

The Normative References if ISO/DIS 32000-2 (PDF 2.0) are structured as an oriented graph (tree), whose vertices are normative documents and (oriented) edges are references from one document to another. Both vertices and edges are annotated by additional comments to describe discovered issues or just to provide additional informative notes. 

This repo contains:

- A human-readable worksheet of normative references in the OpenDocument Spreadsheet format (ODS), readable by [Libre Office](https://www.libreoffice.org/): [NormRefsTreeISO32000-2.ods](NormRefsTreeISO32000-2.ods).
- Machine-readable representation of the normative references in JSON format [referencesGraph.json](data/referencesGraph.json).
- A Python script to calculate some basic metrics for any specific document [countLevels.py](scripts/countLevels.py).
- A Python script to convert the machine-readable JSON to a 3D graph representation [JSONto3D.py](scripts/JSONto3D.py) 

As of November 2020, the references database contains 1172 documents (vertices of the graph). First level references mean the documents are directly referenced from ISO/DIS 32000-2. Their references are called second level references and so on. The database contains:

-	The ISO 32000-2:202x (FDIS) specification, which has id=0 and serves as a root node of the graph.
-	All (78 out of total 79) first level normative references, while one first level reference is available only in Japanese (JIS X.4051, Formatting rules for Japanese documents, 2004, reference id=72).
-	All (210 out of total 210 second level normative references are processed), including those that were found inactive (withdrawn, obsoleted).
-	Additional 1092 references of higher levels up to level 6. 


## **Legend**

The Legend used within the ODS file reflects the processing status of the documents and is visualized on the Refs Tree worksheet using the following colored naming scheme:
-	Not available (red): documents not available in the open access
-	Withdrawn, obsoleted or inactive (orange): standards that are no longer active
-	Processed documents (green): the documents whose normative references were also added to the graph
-	Gray background is used to trace 2nd level references and links to them from 1st level references


## **Machine-readable JSON**

[referencesGraph.json](data/referencesGraph.json) contains the JSON representation of the above data organized as follows. The value of the (root) key ISO32000_2_DB is the array of all normative documents. 

Each document is a record with the following fields:
- **id** - unique id of the document.
- **orgs** - an array of standardization bodies managing this reference. Each element of this array is a pair of properties: **org** (=name of the authority) and **stid** (=the official identification number of the standard for this authority). 
- **title** - title of the document.
-	**label** - commonly used short title or abbreviation for the standard.
- **url** - URL to locate the document (if available).
-	**date**: publication date of the standard
-	**status**: the status of the document, which can be one of the following: **active**, **in development**, **update**, **obsolete**, **withdrawn**, **not available**
- **refs** - the array of all id’s for all normative references of this document.
- **note** - any abnormalities or informative notes for this document.
- **referencedBy** - the array of documents referencing this document.
- **refsComments** - any abnormalities or informative notes for the document references.
-	**__parser** - an additional structure that specifies the role of the given reference document for PDF 2.0 parser implementation. It includes the following fields:
    -	**type** - ascii or binary
    -	**complexity** - low, medium or high
    -	**dialects** (optional) - the dialects for this reference which may affect parser implementation
    -	**comments** - additional comments on this parser


## **Python Scripts**

The Python script [countLevels.py](scripts/getStats.py) calculates and writes basic statistics to a JSON file, by processing a [referencesGraph.json](data/referencesGraph.json) file. In particualar, this includes metrics (the distance or so-called reference levels) from any given point in the graph, as specified by a document’s unique ID number. 
```
Usage: countLevels.py <infilename> <outfilename> <id> <N> <M>
where:
- infilename  is the JSON with the references
- outfilename is the JSON with the count results
- id          is the root document ID for counting docs by the level (0 means ISO 32000-2)
- N           is the number of top N docs with maximal number of refs
- M           is the number of top M referenced docs
```

The Python script [JSONto3D.py](scripts/JSONto3D.py) implements the conversion of the references graph DB (referencesGraph.json) into another JSON format commonly used to represent directed graphs (see https://github.com/vasturiano/3d-force-graph-vr/ ). 

---
Copyright 2020 PDF Association, Inc. https://www.pdfa.org

This material is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) under Contract No. HR001119C0079. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Defense Advanced Research Projects Agency (DARPA). Approved for public release.
