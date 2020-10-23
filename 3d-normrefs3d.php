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

 A 3D visualization (non-VR) of the PDF 2.0 Normative References graph
 See https://github.com/vasturiano/3d-force-graph/ and https://github.com/vasturiano/three-spritetext

 Author: Peter Wyatt
-->
<head>
  <title>PDF 2.0 Normative References 3D visualization</title>
  <meta charset="UTF-8">
  <style>
      body { margin: 0; }
  </style>
  <script src="//unpkg.com/three"></script>
  <script src="//unpkg.com/three-spritetext"></script>
  <script src="//unpkg.com/3d-force-graph"></script>
</head>

<script>
function highlight() {
	// Find the node
	let { nodes, links } = Graph.graphData();
	let node = nodes.find(o => o.name == document.getElementById('norm-refs').value);

	// Aim at node from outside it
	const distance = 60;
	const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);
	Graph.cameraPosition(
		{ x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // new position
		node, // lookAt ({ x, y, z })
		3000  // ms transition duration
    );
}

function populate() {
	// Populate drop-down list with Normative Reference titles from Graph nodes (but sorted alphabetically)
	// Need to wait for 3d-force-graph JS to process JSON so do on first click. Only needs to be done once.
	var sel  = document.getElementById('norm-refs');
	var frag = document.createDocumentFragment();
	let { nodes, links } = Graph.graphData();
	nodes.sort((a, b) => a.name.localeCompare(b.name));

	nodes.forEach(function(node, index) {
		var opt = document.createElement('option');
		opt.innerHTML = node.name;
		opt.value = node.name;
		frag.appendChild(opt);
	});
	sel.appendChild(frag);
	sel.removeEventListener("onClick", populate);
}
</script>

<body>
  <div id="3d-graph"></div>
  <p style="position: absolute; top: 10px; left: 10px; font-family: Arial, Helvetica, sans-serif; font-size: 18px">PDF 2.0 Normative References 3D visualization</p>
  <p id="selected-nodes" style="position: absolute; top: 40px; left: 10px; font-family: Arial, Helvetica, sans-serif;">Selected references:</p>

  <div id="find-object" style="position: absolute; top: 80px; left: 10px; font-family: Arial, Helvetica, sans-serif;">
  	<form id="norm-refs-list">
	    <select id="norm-refs" style="width:95%" name="norm-refs" onClick="populate()" onChange="highlight()">
			<option value="">Select Normative Reference to highlight...</option>
		</select>
	</form>
  </div>

  <script>
    function bkg_colorize(n) { // Background color of nodes according to SDOs
		if (n.id == 0)
			return 'LightPink';
		else if (n.group == 'ISO')
			return 'LightBlue';
		else if (n.group == 'W3C')
			return 'PaleGreen';
		else if (n.group == 'Adobe')
			return 'MistyRose';
		else if (n.group == 'Unicode')
			return 'PeachPuff';
		else
			return 'white';
	}

    function colorize(n) { // Colorize nodes according to SDOs
		if (n.id == 0)
			return 'Red';
		else if (n.group == 'ISO')
			return 'Blue';
		else if (n.group == 'W3C')
			return 'Green';
		else if (n.group == 'Adobe')
			return 'Pink';
		else if (n.group == 'Unicode')
			return 'Olive';
		else
			return 'DarkGrey';
	}

    let selectedNodes = new Set();

    const Graph = ForceGraph3D({ controlType: 'orbit' })
      (document.getElementById('3d-graph'))
  	    .jsonUrl('pdf20-norm-refs.json')
  	    .showNavInfo(true)
		.enableNodeDrag(true)
        .enableNavigationControls(true)
        .backgroundColor('white')
        .onNodeDragEnd(node => { node.fx = node.x; node.fy = node.y; node.fz = node.z; }) // stop node floating back
        .nodeColor(node => {
            if (selectedNodes.has(node))
            	return 'yellow';
           	else
				return colorize(node);
        })
		.onNodeClick((node, event) => {
			let s = document.getElementById('selected-nodes').innerHTML;
			if (event.ctrlKey || event.shiftKey || event.altKey) { // multi-selection
				if (selectedNodes.has(node)) {
					selectedNodes.delete(node);
					s = s.replace(' "'+node.name+'"', '');
				} else {
					selectedNodes.add(node);
					s = s + ' "' + node.name + '"';
				}
		  	} else { // single-selection
				const untoggle = selectedNodes.has(node) && selectedNodes.size === 1;
				selectedNodes.clear();
				if (!untoggle) {
					selectedNodes.add(node);
					s = 'Selected references: "' + node.name + '"';
				} else {
					s = 'Selected references:';
				}
		  	}
			document.getElementById('selected-nodes').innerHTML = s;
		  	Graph.nodeColor(Graph.nodeColor()); // update color of selected nodes
        })
  		.linkAutoColorBy('group')
        .linkDirectionalArrowLength(3)
        .linkDirectionalArrowRelPos(1)
        .linkDirectionalParticles(3)
        .linkDirectionalParticleSpeed(0.01)
        .linkWidth(0.75)
        .nodeLabel(node => `<span style="color:${colorize(node)};font-size:10px;background-color:white">${node.name}</span>`)
        .nodeRelSize(1)
        .nodeThreeObject(node => {
			// use a sphere as a drag handle
			const obj = new THREE.Mesh(
				new THREE.SphereGeometry(10),
				new THREE.MeshBasicMaterial({ depthWrite: false, transparent: true, opacity: 0 }));

			// add text sprite as child
			const sprite = new SpriteText(node.short);
			sprite.color = colorize(node);
			sprite.backgroundColor = bkg_colorize(node);
			sprite.borderWidth = 1;
			sprite.borderColor = colorize(node);
			if (node.id == 0)
				sprite.textHeight = 18;
			else
				sprite.textHeight = 8;
			obj.add(sprite);
			return obj;
        })
        .nodeAutoColorBy('group');

	// Spread nodes a little wider
    Graph.d3Force('charge').strength(-120);
</script>
</body>
</html>
