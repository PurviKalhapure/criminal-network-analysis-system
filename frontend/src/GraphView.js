import React, { useEffect, useState } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import axios from 'axios';

function GraphView({ personId }) {
  const [elements, setElements] = useState([]);

  useEffect(() => {
    if (!personId) return;
    axios.get(`http://127.0.0.1:8000/network/${personId}`)
      .then(res => {
        const nodes = res.data.nodes.map(n => ({
          data: { id: n.id, label: n.id, risk_flag: String(n.risk_flag) }
        }));
        const edges = res.data.edges.map((e, i) => ({
          data: { id: `e${i}`, source: e.source, target: e.target }
        }));
        setElements([...nodes, ...edges]);
      })
      .catch(err => console.log(err));
  }, [personId]);

  const stylesheet = [
    { selector: 'node', style: { 'label': 'data(label)', 'background-color': '#00e5ff', 'color': '#fff', 'font-size': 10, 'width': 25, 'height': 25 } },
    { selector: 'node[risk_flag = "true"]', style: { 'background-color': '#ff3b3b' } },
    { selector: 'edge', style: { 'width': 2, 'line-color': '#95a5a6', 'target-arrow-shape': 'triangle', 'curve-style': 'bezier' } }
  ];

  return (
    <CytoscapeComponent
      key={personId}
      elements={elements}
      style={{ width: '100%', height: '600px', background: '#0a0e17' }}
      stylesheet={stylesheet}
      layout={{ name: 'cose', animate: false }}
    />
  );
}

export default GraphView;