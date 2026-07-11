"use client";

import { useState, useEffect } from "react";
import { API_BASE } from "@/lib/api";
import { useStadiumStore } from "@/stores/stadiumStore";

interface IntentSuggestion {
  type: string;
  reason: string;
}

interface NextIntentResponse {
  suggestions: IntentSuggestion[];
  match_phase: string;
  match_minute: number;
}

const typeLabels: Record<string, string> = {
  gate: "Gate",
  concourse: "Concourse",
  seat: "Seat",
  food: "Food Court",
  restroom: "Restroom",
  merchandise: "Merchandise",
  exit: "Exit",
  parking: "Parking",
};

const typeIcons: Record<string, string> = {
  gate: "\u{1F6AA}",
  concourse: "\u{1F3E0}",
  seat: "\u{1F4BA}",
  food: "\u{1F372}",
  restroom: "\u{1F6BD}",
  merchandise: "\u{1F3EA}",
  exit: "\u{2197}\uFE0F",
  parking: "\u{1F17F}",
};

export default function NextIntent() {
  const routeResult = useStadiumStore((s) => s.route.routeResult);
  const navigateTo = useStadiumStore((s) => s.route.navigateTo);
  const graphNodes = useStadiumStore((s) => s.graphNodes);
  const routeLoading = useStadiumStore((s) => s.route.routeLoading);
  const [suggestions, setSuggestions] = useState<IntentSuggestion[]>([]);

  useEffect(() => {
    if (!routeResult || routeResult.steps.length === 0) {
      setSuggestions([]);
      return;
    }

    const lastStep = routeResult.steps[routeResult.steps.length - 1];
    const locType = lastStep.instruction.includes("Concourse") ? "concourse"
      : lastStep.instruction.includes("Gate") ? "gate"
      : lastStep.instruction.includes("Seat") || lastStep.instruction.includes("seat") ? "seat"
      : lastStep.instruction.includes("Food") ? "food"
      : lastStep.instruction.includes("Restroom") ? "restroom"
      : lastStep.instruction.includes("Exit") || lastStep.instruction.includes("exit") ? "exit"
      : lastStep.instruction.includes("Parking") || lastStep.instruction.includes("parking") ? "parking"
      : "concourse";

    fetch(`${API_BASE}/api/navigation/next-intent`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        current_location: routeResult.path[routeResult.path.length - 1] || "",
        current_location_type: locType,
      }),
    })
      .then((r) => r.json())
      .then((data: NextIntentResponse) => {
        setSuggestions(data.suggestions || []);
      })
      .catch(() => setSuggestions([]));
  }, [routeResult]);

  if (suggestions.length === 0) return null;

  const handleNavigate = (type: string) => {
    const target = graphNodes.find(
      (n) => n.type.toLowerCase() === type.toLowerCase()
    );
    if (target) {
      navigateTo("concourse_l0", target.id);
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-4 backdrop-blur-xl bg-white/[0.04] border border-white/[0.06]">
      <span className="text-[10px] text-white/40 uppercase tracking-wider font-semibold mb-3 block">
        Next Destination
      </span>
      <div className="flex flex-wrap gap-2">
        {suggestions.map((s, i) => (
          <button
            key={i}
            onClick={() => handleNavigate(s.type)}
            disabled={routeLoading}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 transition-colors border border-cyan-500/20 text-xs text-cyan-400 disabled:opacity-50"
          >
            <span>{typeIcons[s.type] || "\u{1F4CD}"}</span>
            <span>{typeLabels[s.type] || s.type}</span>
          </button>
        ))}
      </div>
      {suggestions.length > 0 && (
        <p className="text-[10px] text-white/30 mt-2">{suggestions[0].reason}</p>
      )}
    </div>
  );
}
