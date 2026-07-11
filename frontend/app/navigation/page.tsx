'use client';

import { useState, useEffect } from 'react';
import { getNavigationRoute, getZones, NavigationResponse, StadiumZone } from '@/lib/api';
import AICard from '@/features/ai-card/AICard';
import NextIntent from '@/features/navigation/NextIntent';
import { useStadiumStore } from '@/stores/stadiumStore';

const congestionColors: Record<string, string> = {
  low: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
  medium: 'text-amber-400 bg-amber-400/10 border-amber-400/20',
  high: 'text-rose-400 bg-rose-400/10 border-rose-400/20',
};

function formatDuration(totalSeconds: number): string {
  const m = Math.floor(totalSeconds / 60);
  const s = Math.round(totalSeconds % 60);
  return s > 0 ? `${m} min ${s}s` : `${m} min`;
}

function formatDistance(meters: number): string {
  return meters >= 1000 ? `${(meters / 1000).toFixed(1)} km` : `${Math.round(meters)}m`;
}

export default function NavigationPage() {
  const [zones, setZones] = useState<StadiumZone[]>([]);
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [routeResult, setRouteResult] = useState<NavigationResponse | null>(null);
  const [accessibility, setAccessibility] = useState({ wheelchair: false, vision: false, hearing: false });

  useEffect(() => {
    getZones()
      .then((data) => {
        setZones(data);
        if (data.length >= 2) {
          setFrom(data[0].zone_id);
          setTo(data[1].zone_id);
        }
      })
      .catch(() => {});
  }, []);

  async function handleCalculate() {
    if (!from || !to) return;
    setLoading(true);
    setError('');
    setRouteResult(null);

    try {
      let pref: string | undefined;
      if (accessibility.wheelchair) pref = 'wheelchair';
      else if (accessibility.vision) pref = 'visual';
      else if (accessibility.hearing) pref = 'hearing';

      const result = await getNavigationRoute(from, to, pref);
      setRouteResult(result);
      useStadiumStore.setState((s) => ({ route: { ...s.route, routeResult: result as any } }));
    } catch (e) {
      setError('Failed to calculate route. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  const zoneName = (zoneId: string) => {
    const z = zones.find((z) => z.zone_id === zoneId);
    return z ? z.name : zoneId;
  };

  return (
    <div className="md:ml-[68px] min-h-screen bg-gradient-mesh bg-grid-pattern">
      <header className="sticky top-0 z-40 glass-panel border-b border-white/[0.06] px-6 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-white">Navigation</h1>
          <p className="text-xs text-gray-500">AI-powered wayfinding • Accessibility-first routing</p>
        </div>
        {routeResult && (
          <span className="badge badge-success">Route Active</span>
        )}
      </header>

      <div className="p-6 grid grid-cols-12 gap-5">
        {/* Left Panel — Controls */}
        <div className="col-span-12 lg:col-span-3 space-y-5 animate-slide-in delay-1">
          <div className="glass-card p-5">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Route Planner</h2>

            <div className="space-y-4">
              <div>
                <label className="text-xs text-gray-500 mb-1.5 block">From</label>
                <select
                  value={from}
                  onChange={(e) => setFrom(e.target.value)}
                  className="w-full glass-input px-3 py-2.5 text-sm rounded-xl"
                >
                  {zones.map((z) => (
                    <option key={z.zone_id} value={z.zone_id} className="bg-[#1a1f36] text-white">{z.name}</option>
                  ))}
                </select>
              </div>

              <div className="flex justify-center">
                <div className="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.06] flex items-center justify-center text-gray-500 text-sm">
                  ↕
                </div>
              </div>

              <div>
                <label className="text-xs text-gray-500 mb-1.5 block">To</label>
                <select
                  value={to}
                  onChange={(e) => setTo(e.target.value)}
                  className="w-full glass-input px-3 py-2.5 text-sm rounded-xl"
                >
                  {zones.map((z) => (
                    <option key={z.zone_id} value={z.zone_id} className="bg-[#1a1f36] text-white">{z.name}</option>
                  ))}
                </select>
              </div>
            </div>

            <button
              onClick={handleCalculate}
              disabled={loading || !from || !to}
              className="w-full mt-4 py-2.5 px-4 bg-gradient-to-r from-cyan-500 to-cyan-600 text-white text-sm font-semibold rounded-xl shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/30 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {loading ? 'Calculating...' : 'Calculate Route'}
            </button>

            {error && (
              <p className="mt-2 text-xs text-rose-400">{error}</p>
            )}
          </div>

          {/* Accessibility Options */}
          <div className="glass-card p-5">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Accessibility</h2>
            <div className="space-y-3">
              {[
                { key: 'wheelchair' as const, label: 'Wheelchair Access', icon: '\u267f' },
                { key: 'vision' as const, label: 'Vision Assistance', icon: '\uD83D\uDC41' },
                { key: 'hearing' as const, label: 'Hearing Support', icon: '\uD83D\uDC42' },
              ].map((opt) => (
                <label key={opt.key} className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-white/[0.03] transition-colors cursor-pointer">
                  <div
                    className={`w-5 h-5 rounded-md border-2 flex items-center justify-center transition-all ${
                      accessibility[opt.key]
                        ? 'bg-cyan-500 border-cyan-500'
                        : 'border-gray-600'
                    }`}
                    onClick={() => setAccessibility((prev) => {
                      const next = { wheelchair: false, vision: false, hearing: false };
                      next[opt.key] = !prev[opt.key];
                      return next;
                    })}
                  >
                    {accessibility[opt.key] && (
                      <span className="text-white text-xs">{'\u2713'}</span>
                    )}
                  </div>
                  <span className="text-sm">{opt.icon}</span>
                  <span className="text-sm text-gray-300">{opt.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Map + Route Details */}
        <div className="col-span-12 lg:col-span-9 space-y-5">
          <div className="glass-card p-1 animate-slide-in delay-2 overflow-hidden" style={{ minHeight: '400px' }}>
            <div className="relative w-full h-[400px] rounded-2xl bg-[#0d1220] border border-white/[0.04] flex items-center justify-center overflow-hidden">
              <div className="absolute inset-0 bg-grid-pattern opacity-30" />
              <div className="absolute inset-0">
                <div className="absolute top-1/3 left-1/4 w-40 h-24 bg-cyan-500/10 rounded-2xl border border-cyan-500/20 animate-pulse-slow" />
                <div className="absolute top-1/2 left-1/2 w-32 h-20 bg-amber-500/10 rounded-2xl border border-amber-500/20" />
                <div className="absolute bottom-1/4 right-1/4 w-36 h-28 bg-emerald-500/10 rounded-2xl border border-emerald-500/20" />
                {routeResult && (
                  <svg className="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M 100 300 Q 200 280 280 220 Q 360 160 450 180 Q 540 200 620 140"
                      fill="none"
                      stroke="#06b6d4"
                      strokeWidth="3"
                      strokeDasharray="8 4"
                      opacity="0.6"
                    />
                    <circle cx="100" cy="300" r="6" fill="#10b981" />
                    <circle cx="620" cy="140" r="6" fill="#f43f5e" />
                  </svg>
                )}
              </div>
              <div className="relative z-10 text-center">
                {!routeResult ? (
                  <div className="animate-pulse-slow">
                    <div className="w-16 h-16 mx-auto rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mb-3">
                      <span className="text-2xl">{'\uD83D\uDDFA'}</span>
                    </div>
                    <p className="text-sm text-gray-400 font-medium">Interactive Map</p>
                    <p className="text-xs text-gray-600 mt-1">Select start and destination, then calculate</p>
                  </div>
                ) : (
                  <div className="text-center">
                    <p className="text-sm text-emerald-400 font-medium">{'\u2713'} Route calculated</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {zoneName(from)} → {zoneName(to)}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Route Details */}
          {routeResult && (
            <div className="glass-card p-6 animate-slide-in delay-3">
              <div className="flex items-center justify-between mb-5">
                <div>
                  <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Route Details</h2>
                  <p className="text-xs text-gray-500 mt-1">
                    {zoneName(from)} → {zoneName(to)}
                    {routeResult.accessibility_adapted && (
                      <span className="ml-2 text-cyan-400">{'\u267F'} Accessible</span>
                    )}
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className="text-xs text-gray-500">Total Distance</p>
                    <p className="text-sm font-semibold text-white">{formatDistance(routeResult.total_distance_m)}</p>
                  </div>
                  <div className="h-8 w-px bg-white/10" />
                  <div className="text-right">
                    <p className="text-xs text-gray-500">Est. Time</p>
                    <p className="text-sm font-semibold text-cyan-400">{formatDuration(routeResult.total_duration_s)}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-0">
                {routeResult.steps.map((step, i) => (
                  <div key={i} className="flex gap-4">
                    <div className="flex flex-col items-center">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${
                        i === 0 ? 'bg-emerald-500 text-white' : i === routeResult.steps.length - 1 ? 'bg-rose-500 text-white' : 'bg-white/[0.08] text-gray-400 border border-white/[0.1]'
                      }`}>
                        {i + 1}
                      </div>
                      {i < routeResult.steps.length - 1 && (
                        <div className="w-px h-10 bg-white/[0.08]" />
                      )}
                    </div>
                    <div className="pb-4 flex-1">
                      <p className="text-sm text-gray-200 font-medium">{step.instruction}</p>
                      <div className="flex items-center gap-3 mt-1.5">
                        <span className="text-xs text-gray-500">{formatDistance(step.distance_m)}</span>
                        <span className="text-xs text-gray-500">{formatDuration(step.duration_s)}</span>
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${congestionColors[step.congestion_level]}`}>
                          {step.congestion_level}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {routeResult.accessibility_adapted && (
                <div className="mt-4 p-3 rounded-xl bg-cyan-500/5 border border-cyan-500/10">
                  <p className="text-xs text-cyan-300">
                    <span className="font-semibold">{'\u267F'} Accessible Route:</span> This route uses accessible paths and elevators. No stairs.
                  </p>
                </div>
              )}
            </div>
          )}

          {routeResult && routeResult.confidence > 0 && (
            <div className="animate-slide-in delay-3 space-y-3">
              <AICard />
              <NextIntent />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
