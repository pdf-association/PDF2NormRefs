# **ISO/DIS 32000-2 (PDF 2.0) Normative References Tree**

The Normative References if ISO/DIS 32000-2 (PDF 2.) are structured as an oriented graph (tree), whose vertices are normative documents and (oriented) edges are references from one document to another. Both vertices and edges are annotated by additional comments to describe discovered issues or just to provide additional informative notes. 

This repo contains:

- A human-readable worksheet of normative references in the OpenDocument Spreadsheet format (ODS): [Normative references tree for ISO 32000-2_2020.ods](Normative references tree for ISO 32000-2_2020.ods).
- Machine-readable representation of the normative references in JSON format [referencesGraph.json](referencesGraph.json).
- A Python script to convert from the human-readable representation (ODS) to the machine-readable JSON equivalent [ODStoJSON.py](ODStoJSON.py) 
- A Python script to calculate some basic metrics [countLevels.py](countLevels.py).

As of May 2020, the references database contains 605 documents (vertices of the graph) in total and 1220 references between them (edges of the graph). First level references mean the documents are directly referenced from ISO/DIS 32000-2. Their references are called second level references and so on:

- 84 out of total 89 (94.4%) first level normative references are processed (i.e. all their normative references are added to the database).
- 265 out total 336 (78.9%) second level normative references are processed, including those that were found inactive (withdrawn, obsoleted), while 6 more documents were not available.

## **Legend**

The Legend used within the ODS file reflects the processing status of the documents and is visualized on the Refs Tree worksheet using colored naming scheme:
- Processed documents: the documents that were added to the database, their normative references are inspected and added to the database as well.
- Documents to be inspected: normative references are not yet inspected. Some of them might not be present in the database yet.
- Not available: documents not available in the open access.
- Withdrawn, obsoleted or inactive: standards that are no longer active.

## **Machine-readable JSON**

[referencesGraph.json](referencesGraph.json) contains the JSON representation of the above data organized as follows. The value of the (root) key ISO32000-2-DB is the array of all normative documents. 
Each document is a record with the following fields:
- id - unique id of the document.
- title - title of the document.
- url - URL to locate the document (if available).
- refs - the array of all id’s for all normative references of this document.
- note - any abnormalities or informative notes for this document.
- referencedBy - the array of documents referencing this document.
- refsComments - any abnormalities or informative notes for the document references.
- status – the current processing status of the document see above.

## **Python Scripts**

The Python script [ODStoJSON.py](ODStoJSON.py) converts the human-readable representation of the references graph (the LibreOffice Calc ODS file) to a machine-readable JSON equivalent. It takes no CLI arguments, reads the file "Normative references tree for ISO 32000-2_2020.ods" from the local folder and creates the file “referencesGraph.json” next to it.

The Python script [countLevels.py](countLevels.py) calculates and writes basic metrics to a JSON file, by processing a referencesGraph.json file. These metrics can be from any given point in the graph, as specified by a document’s unique ID number. 
```
Usage: countLevels.py <infilename> <outfilename> <id>
where:
infilename	JSON with the references (usually “referencesGraph.json”)
outfilename	JSON file to write the metrics results
id		is the root document ID for counting (ID 0 means ISO/DIS 32000-2)
```

## **ToDo** :pushpin:

- Complete processing of all 1st and 2nd level references. Process 3rd level references for all cases that are relevant to PDF parsing. It is expected that about 200 extra references will be added to the database.
- Parse the title strings of the documents to convert them into more granular record (standardization body, author, short title, version, publication date)
- Introduce short and meaningful names as  keys for ease of graph navigation (such as PDF20, XML11, X.509, JPEG, etc.)

