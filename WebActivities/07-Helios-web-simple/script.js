import { Helios, xnet } from "helios-web"

import { rgb as d3rgb } from "d3-color"
import * as d3Chromatic from "d3-scale-chromatic"
import { scaleOrdinal as d3ScaleOrdinal, scaleSequential as d3ScaleSequential} from "d3-scale"

let nodes = {
	"0": {
		label: "Node 0",
	},
	"1": {
		label: "Node 1",
	},
	"2": {
		label: "Node 2",
	},
}

// Edges are arrays of node ids
let edges = [
	{
		source: "0",
		target: "1",
	},
	{
		source: "1",
		target: "2",
	},
	{
		source: "2",
		target: "0",
	}
];

// async function loadNetwork(networkName,resetPositions) {
// 	let network = await xnet.loadXNETFile("../../Networks/"+networkName + ".xnet")

// 	let nodeCount = network.nodesCount;	
// 	let nodes = {};
// 	let edges = [];
// 	if(resetPositions && "Position" in network.verticesProperties){
// 		delete network.verticesProperties["Position"];
// 	}
// 	for (let index = 0; index < nodeCount; index++) {
// 		nodes["" + index] = {
// 			ID: "" + index,
// 		}
// 		if (network.labels) {
// 			nodes["" + index].label = network.labels[index];
// 		}
// 	}
// 	for (const [key, value] of Object.entries(network.verticesProperties)) {
// 		for (let index = 0; index < nodeCount; index++) {
// 			nodes["" + index][key.toLowerCase()] = value[index];
// 		}
// 	}

// 	for (let index = 0; index < network.edges.length; index++) {
// 		let fromIndex, toIndex;

// 		edges.push({
// 			"source": "" + network.edges[index][0],
// 			"target": "" + network.edges[index][1],
// 			// directed?
// 		});
// 	}
// 	return [nodes, edges];
// }

// [nodes, edges] = await loadNetwork("EUPowerGrid",true);

let helios = new Helios({
	elementID: "netviz", // ID of the element to render the network in
	nodes: nodes, // Dictionary of nodes 
	edges: edges, // Array of edges
	use2D: false, // Choose between 2D or 3D layouts
});


helios
.backgroundColor([1.0,1.0,1.0,1.0]) 
// .nodeColor([0.0, 0.0, 0.0]) 
// .nodeSize(1.0)
// .nodeOpacity(1.0)
.nodeOutlineWidth(0.2)
.nodeOutlineColor([1.0,1.0,1.0])
// .edgesOpacity(1.0)
// .edgesWidthScale(1.0)
// .additiveBlending(false)

// Node events
helios.onNodeHoverStart((node, event) => {
	console.log("node hover start: ", node);
})
.onNodeHoverMove((node, event) => {
	console.log("node hover move: ", node);
})
.onNodeHoverEnd((node, event) => {
	console.log("node hover end: ", node);
})
.onNodeClick((node, event) => {
	console.log(`node clicked: ${node.ID}`);
})
.onNodeDoubleClick((node, event) => {
	console.log(`node double clicked: ${node.ID}`);
})

// Edge events
// helios.onEdgeHoverStart((edge, event) => {
// 	console.log("edge hover start: ", edge);
// })
// .onEdgeHoverMove((edge, event) => {
// 	console.log("edge hover move: ", edge);
// })
// .onEdgeHoverEnd((edge, event) => {
// 	console.log("edge hover end: ", edge);
// })
// .onEdgeClick((edge, event) => {
// 	console.log("Edge clicked");
// })

// Layout events
helios.onLayoutStart(()=>{
	console.log("Layout start");
})
.onLayoutStop(()=>{
	console.log("Layout stop");
});

helios.onReady(() => {
	helios.zoomFactor(0.05);
	helios.zoomFactor(30, 8000);
});