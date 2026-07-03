"use client";

import { ReactFlow, Background, Controls, MiniMap } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import type { WarRoomState } from "../lib/types";

export function OntologyGraphPanel({ state }: { state: WarRoomState | null }) {
  const nodes = (state?.graph_nodes ?? []).map((node, index) => ({
    id: node.id,
    position: { x: (index % 5) * 220, y: Math.floor(index / 5) * 110 },
    data: { label: `${node.label}\n${node.type}` }
  }));
  const edges = (state?.graph_edges ?? []).map((edge) => ({
    id: edge.id,
    source: edge.source,
    target: edge.target,
    label: edge.label
  }));
  return (
    <section className="panel graphPanel">
      <h2>Ontology Graph</h2>
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </section>
  );
}

