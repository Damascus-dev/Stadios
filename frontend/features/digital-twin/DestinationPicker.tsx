"use client";

import { useStadiumStore, GraphNode } from "@/stores/stadiumStore";

interface Props {
  selected: GraphNode | null;
  onSelect: (node: GraphNode | null) => void;
}

const typeLabels: Record<string, string> = {
  food: "Food Court",
  restroom: "Restroom",
  medical: "Medical Station",
  charging: "Charging Station",
  prayer: "Prayer Room",
  merchandise: "Merchandise",
  volunteer: "Volunteer Desk",
  concourse: "Concourse",
  gate: "Gate",
  parking: "Parking",
  exit: "Exit",
};

const typeIcons: Record<string, string> = {
  food: "\u{1F372}",
  restroom: "\u{1F6BD}",
  medical: "\u{1F3E5}",
  charging: "\u{26A1}",
  prayer: "\u{1F54A}",
  merchandise: "\u{1F3EA}",
  volunteer: "\u{1F9D1}",
  concourse: "\u{1F3E0}",
  gate: "\u{1F6AA}",
  parking: "\u{1F17F}",
  exit: "\u{1F6AA}",
};

export default function DestinationPicker({ selected, onSelect }: Props) {
  const graphNodes = useStadiumStore((s) => s.graphNodes);
  const routeLoading = useStadiumStore((s) => s.route.routeLoading);
  const routeResult = useStadiumStore((s) => s.route.routeResult);
  const routeError = useStadiumStore((s) => s.route.routeError);
  const navigateTo = useStadiumStore((s) => s.route.navigateTo);
  const clearRoute = useStadiumStore((s) => s.route.clearRoute);

  const facilities = graphNodes.filter((n) =>
    ["food", "restroom", "medical", "charging", "prayer", "merchandise", "volunteer"].includes(n.type)
  );

  if (selected) {
    return (
      <div className="fixed bottom-4 left-4 right-4 md:bottom-6 md:left-1/2 md:-translate-x-1/2 md:max-w-md z-50">
        <div className="glass-panel rounded-2xl p-4 backdrop-blur-xl bg-white/[0.06] border border-white/[0.08]">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-xl">{typeIcons[selected.type] || "\u{1F4CD}"}</span>
              <div>
                <p className="text-sm font-semibold text-white">
                  {typeLabels[selected.type] || selected.type}
                </p>
                <p className="text-xs text-white/40">
                  Level {selected.level} &middot; {selected.quadrant}
                </p>
              </div>
            </div>
            <button
              onClick={() => { onSelect(null); clearRoute(); }}
              className="text-white/40 hover:text-white/80 transition-colors text-lg leading-none"
            >
              &times;
            </button>
          </div>

          {routeError && (
            <p className="text-xs text-red-400 mb-2">{routeError}</p>
          )}

          {routeResult && (
            <div className="mb-3 p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
              <p className="text-xs text-cyan-400 font-semibold">Route found</p>
              <p className="text-xs text-white/50">
                {routeResult.total_distance_m.toFixed(0)}m &middot; {routeResult.total_duration_s.toFixed(0)}s
              </p>
            </div>
          )}

          <div className="flex gap-2">
            <button
              onClick={() => {
                clearRoute();
                navigateTo("concourse_l0", selected.id);
              }}
              disabled={routeLoading}
              className="flex-1 px-4 py-2.5 rounded-xl bg-cyan-500/20 text-cyan-400 text-sm font-semibold hover:bg-cyan-500/30 transition-colors border border-cyan-500/20 disabled:opacity-50"
            >
              {routeLoading ? "Finding route..." : routeResult ? "Re-route" : "Navigate Here"}
            </button>
            <button
              onClick={() => { onSelect(null); clearRoute(); }}
              className="px-4 py-2.5 rounded-xl bg-white/[0.04] text-white/60 text-sm hover:bg-white/[0.08] transition-colors border border-white/[0.06]"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 md:bottom-6 md:left-1/2 md:-translate-x-1/2 md:max-w-2xl z-50">
      <div className="glass-panel rounded-2xl p-3 backdrop-blur-xl bg-white/[0.04] border border-white/[0.06]">
        <p className="text-xs text-white/40 mb-2 px-1">
          Tap a destination to navigate
        </p>
        <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
          {facilities.slice(0, 12).map((f) => (
            <button
              key={f.id}
              onClick={() => onSelect(f)}
              className="flex-shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] transition-colors border border-white/[0.06] text-xs text-white/70 hover:text-white"
            >
              <span>{typeIcons[f.type] || "\u{1F4CD}"}</span>
              <span>{typeLabels[f.type] || f.type}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
