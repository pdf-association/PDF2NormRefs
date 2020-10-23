<html lang="en">
<!--
 Copyright 2020 PDF Association, Inc. https://www.pdfa.org

 This material is based upon work supported by the Defense Advanced
 Research Projects Agency (DARPA) under Contract No. HR001119C0079.
 Any opinions, findings and conclusions or recommendations expressed
 in this material are those of the author(s) and do not necessarily
 reflect the views of the Defense Advanced Research Projects Agency
 (DARPA). Approved for public release.

 SPDX-License-Identifier: Apache-2.0

 A 3D VR visualization of the PDF 2.0 Normative References graph
 See https://github.com/vasturiano/3d-force-graph-vr/

 Author: Peter Wyatt
-->
<head>
  <title>PDF 2.0 Normative References VR visualization</title>
  <meta charset="UTF-8">
  <style>
      body { margin: 0; }
  </style>
  <script src="//unpkg.com/3d-force-graph-vr"></script>
</head>

<body>
  <div id="3d-graph"></div>
  <p style="position: absolute; top: 10px; left: 10px; font-size: 18px">PDF 2.0 Normative References VR visualization</p>

  <script>
    const Graph = ForceGraphVR()
      (document.getElementById('3d-graph'))
        .jsonUrl('pdf20-norm-refs.json')
        .showNavInfo(true)
        .nodeColor(node => {
			if (node.id == 0)
				return 'red';
			else if (node.group == 'ISO')
				return 'blue';
			else if (node.group == 'W3C')
				return 'green';
			else if (node.group == 'Adobe')
				return 'pink';
			else if (node.group == 'Unicode')
				return 'gold';
			else
				return 'silver';
        })
        .linkAutoColorBy('group')
        .linkDirectionalArrowLength(3)
        .linkDirectionalArrowRelPos(1)
        .linkDirectionalParticles(3)
        .linkDirectionalParticleSpeed(0.01)
        .linkWidth(0.75)
        .linkHoverPrecision(0.3)
        .nodeLabel('name')
        .nodeRelSize(1)
        .nodeAutoColorBy('group');

	// Spread nodes a little wider
    Graph.d3Force('charge').strength(-120);
  </script>
</body>
</html>
