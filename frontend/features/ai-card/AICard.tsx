"use client";

import { useStadiumStore, RouteAlternative } from "@/stores/stadiumStore";

function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color =
    pct >= 80 ? "bg-green-500" : pct >= 50 ? "bg-yellow-500" : "bg-red-500";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 rounded-full bg-white/[0.06] overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-xs text-white/40 w-8 text-right">{pct}%</span>
    </div>
  );
}

export default function AICard() {
  const routeResult = useStadiumStore((s) => s.route.routeResult);
  const routeLoading = useStadiumStore((s) => s.route.routeLoading);

  if (routeLoading) {
    return (
      <div className="glass-panel rounded-2xl p-4 backdrop-blur-xl bg-white/[0.04] border border-white/[0.06] animate-pulse">
        <div className="h-3 w-24 bg-white/[0.08] rounded mb-3" />
        <div className="h-3 w-full bg-white/[0.06] rounded mb-2" />
        <div className="h-3 w-3/4 bg-white/[0.06] rounded" />
      </div>
    );
  }

  if (!routeResult) return null;

  const hasExplanation =
    routeResult.reason || routeResult.benefit || routeResult.tradeoff;

  return (
    <div className="glass-panel rounded-2xl backdrop-blur-xl bg-white/[0.04] border border-white/[0.06] overflow-hidden">
      {hasExplanation && (
        <div className="p-4 border-b border-white/[0.06]">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">
              AI Reasoning
            </span>
            <span className="text-[10px] text-white/30">{routeResult.route_id}</span>
          </div>

          {routeResult.reason && (
            <p className="text-sm text-white/80 mb-2">
              <span className="text-white/40 text-xs block mb-0.5">Why this route</span>
              {routeResult.reason}
            </p>
          )}

          <div className="grid grid-cols-2 gap-3 mt-3">
            {routeResult.benefit && (
              <div className="p-2.5 rounded-xl bg-green-500/10 border border-green-500/15">
                <span className="text-[10px] text-green-400 uppercase tracking-wider font-semibold">Benefit</span>
                <p className="text-xs text-white/70 mt-1">{routeResult.benefit}</p>
              </div>
            )}
            {routeResult.tradeoff && (
              <div className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/15">
                <span className="text-[10px] text-amber-400 uppercase tracking-wider font-semibold">Tradeoff</span>
                <p className="text-xs text-white/70 mt-1">{routeResult.tradeoff}</p>
              </div>
            )}
          </div>

          {routeResult.confidence > 0 && (
            <div className="mt-3">
              <span className="text-[10px] text-white/40 uppercase tracking-wider">Confidence</span>
              <ConfidenceBar value={routeResult.confidence} />
            </div>
          )}
        </div>
      )}

      {routeResult.alternatives.length > 0 && (
        <div className="p-4">
          <span className="text-[10px] text-white/40 uppercase tracking-wider font-semibold mb-2 block">
            Alternatives ({routeResult.alternatives.length})
          </span>
          <div className="space-y-2">
            {routeResult.alternatives.map((alt, i) => (
              <AlternativeRow key={i} alt={alt} index={i} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function AlternativeRow({ alt, index }: { alt: RouteAlternative; index: number }) {
  return (
    <div className="p-2.5 rounded-xl bg-white/[0.03] border border-white/[0.06]">
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-white/70 font-medium">
          Option {index + 1}: {alt.description}
        </span>
        <span className="text-[10px] text-white/30">{alt.total_distance_m.toFixed(0)}m</span>
      </div>
      <p className="text-[11px] text-white/50">{alt.reason}</p>
      {alt.tradeoff && (
        <p className="text-[11px] text-amber-400/60 mt-0.5">{alt.tradeoff}</p>
      )}
    </div>
  );
}
