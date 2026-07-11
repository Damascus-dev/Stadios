"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { useStadiumStore, GraphNode } from "@/stores/stadiumStore";
import DestinationPicker from "@/features/digital-twin/DestinationPicker";
import AICard from "@/features/ai-card/AICard";
import { useAutoReroute } from "@/hooks/useAutoReroute";
import NextIntent from "@/features/navigation/NextIntent";

const StadiumCanvas = dynamic(
  () => import("@/features/digital-twin/StadiumCanvas").then((m) => m.StadiumCanvas),
  { ssr: false, loading: () => <div className="w-full h-full flex items-center justify-center text-white/40">Loading 3D...</div> }
);

export default function StadiumPage() {
  useAutoReroute();
  const totalSeats = useStadiumStore((s) => s.totalSeats);
  const routePoints = useStadiumStore((s) => s.route.routePoints);
  const routeResult = useStadiumStore((s) => s.route.routeResult);
  const [selected, setSelected] = useState<GraphNode | null>(null);
  const [targetPosition, setTargetPosition] = useState<[number, number, number] | null>(null);

  const handleSelect = (node: GraphNode | null) => {
    setSelected(node);
    if (node) {
      setTargetPosition([node.position.x, node.position.y + 5, node.position.z + 15]);
    } else {
      setTargetPosition(null);
    }
  };

  return (
    <div className="relative w-full h-[calc(100vh-70px)] md:h-screen">
      <StadiumCanvas
        selectedId={selected?.id}
        targetPosition={targetPosition}
        onNodeClick={(node) => setSelected(node)}
      />

      <div className="absolute top-4 left-4 right-4 md:left-6 md:right-auto pointer-events-none z-40">
        <h1 className="text-xl md:text-2xl font-bold text-white drop-shadow-lg">
          MetLife Stadium
        </h1>
        <p className="text-sm text-white/60 mt-1 drop-shadow">
          {totalSeats > 0 ? `${totalSeats.toLocaleString()} seats` : "Interactive Digital Twin"}
        </p>
        {routePoints.length > 0 && (
          <p className="text-xs text-cyan-400/70 mt-1 drop-shadow">
            Route shown on map
          </p>
        )}
      </div>

      {routeResult && (
        <div className="absolute top-20 right-4 w-72 max-h-[50vh] overflow-y-auto z-40 hidden md:block pointer-events-auto">
          <AICard />
        </div>
      )}

      {routeResult && (
        <div className="absolute top-72 right-4 w-72 z-40 hidden md:block pointer-events-auto">
          <NextIntent />
        </div>
      )}

      <div className="md:hidden pointer-events-auto">
        {routeResult && <div className="absolute bottom-24 left-4 right-4 z-40"><AICard /></div>}
      </div>

      <DestinationPicker
        selected={selected}
        onSelect={handleSelect}
      />
    </div>
  );
}
