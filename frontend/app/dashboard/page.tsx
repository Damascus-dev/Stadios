'use client';

import { useEffect, useState } from 'react';

/* ─── Mock Data ─── */
const crowdZones = [
  { name: 'North Stand', density: 92, color: 'bg-rose-500' },
  { name: 'South Stand', density: 78, color: 'bg-amber-500' },
  { name: 'East Wing Food Court', density: 95, color: 'bg-rose-500' },
  { name: 'West Concourse', density: 54, color: 'bg-emerald-500' },
  { name: 'VIP Lounge', density: 38, color: 'bg-cyan-500' },
  { name: 'Main Concourse', density: 71, color: 'bg-amber-400' },
  { name: 'Gate A Entry', density: 63, color: 'bg-amber-400' },
  { name: 'Gate D Entry', density: 45, color: 'bg-emerald-500' },
];

const alerts = [
  { severity: 'critical', message: 'Medical emergency reported — Section 112, Row H', zone: 'North Stand', time: '2 min ago' },
  { severity: 'high', message: 'Overcrowding threshold exceeded at East Wing Food Court', zone: 'East Wing', time: '8 min ago' },
  { severity: 'medium', message: 'Elevator 3B out of service — accessibility reroute active', zone: 'West Concourse', time: '15 min ago' },
  { severity: 'low', message: 'Volunteer shift change in progress — Zone C', zone: 'South Stand', time: '22 min ago' },
  { severity: 'low', message: 'Parking Lot D reaching 85% capacity', zone: 'Exterior', time: '31 min ago' },
];

const aiRecommendations = [
  {
    agent: 'Navigation',
    priority: 'high',
    action: 'Reroute pedestrian flow from East Wing via South Corridor to reduce congestion by ~30%',
    confidence: 94,
    agentColor: 'text-cyan-400 bg-cyan-400/10 border-cyan-400/20',
  },
  {
    agent: 'Operations',
    priority: 'medium',
    action: 'Deploy 5 additional volunteers to Gate A for expected 2nd-half crowd surge',
    confidence: 87,
    agentColor: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
  },
  {
    agent: 'Accessibility',
    priority: 'high',
    action: 'Activate backup wheelchair ramp at Section 300 — primary ramp queue exceeds 8 min',
    confidence: 91,
    agentColor: 'text-amber-400 bg-amber-400/10 border-amber-400/20',
  },
];

const volunteerZones = [
  { zone: 'Gate A', count: 8, total: 10 },
  { zone: 'North Stand', count: 12, total: 15 },
  { zone: 'Food Court', count: 10, total: 12 },
  { zone: 'VIP Area', count: 6, total: 8 },
  { zone: 'South Stand', count: 9, total: 15 },
];

const severityConfig: Record<string, { badge: string; dot: string }> = {
  critical: { badge: 'badge-critical', dot: 'bg-rose-500' },
  high: { badge: 'badge-high', dot: 'bg-orange-500' },
  medium: { badge: 'badge-medium', dot: 'bg-amber-500' },
  low: { badge: 'badge-low', dot: 'bg-cyan-500' },
};

/* ─── Helper Components ─── */
function LiveClock() {
  const [time, setTime] = useState('');
  useEffect(() => {
    const update = () => {
      const now = new Date();
      setTime(now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }));
    };
    update();
    const id = setInterval(update, 1000);
    return () => clearInterval(id);
  }, []);
  return <span className="font-mono text-sm text-gray-400 tabular-nums">{time}</span>;
}

function ProgressRing({ pct, size = 120, stroke = 8, color = '#06b6d4' }: { pct: number; size?: number; stroke?: number; color?: string }) {
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (pct / 100) * circ;
  return (
    <svg width={size} height={size} className="transform -rotate-90">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" className="progress-ring-bg" strokeWidth={stroke} />
      <circle
        cx={size / 2} cy={size / 2} r={r} fill="none"
        stroke={color}
        strokeWidth={stroke}
        strokeDasharray={circ}
        strokeDashoffset={offset}
        className="progress-ring-fill"
        style={{ filter: `drop-shadow(0 0 6px ${color}55)` }}
      />
    </svg>
  );
}

function MiniBar({ pct, color = 'bg-cyan-500', label, value }: { pct: number; color?: string; label: string; value: string }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-gray-400">{label}</span>
        <span className="text-white font-medium">{value}</span>
      </div>
      <div className="h-1.5 rounded-full bg-white/[0.06] overflow-hidden">
        <div className={`h-full rounded-full ${color} transition-all duration-1000`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

/* ─── Dashboard Page ─── */
export default function DashboardPage() {
  return (
    <div className="ml-[68px] min-h-screen bg-gradient-mesh bg-grid-pattern">
      {/* Top Header */}
      <header className="sticky top-0 z-40 glass-panel border-b border-white/[0.06] px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div>
            <h1 className="text-lg font-bold tracking-tight">
              <span className="text-white">StadiumOS</span>{' '}
              <span className="text-cyan-400">AI</span>
            </h1>
            <p className="text-xs text-gray-500">MetLife Stadium — FIFA World Cup 2026</p>
          </div>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse-slow" />
            <span className="text-xs text-emerald-400 font-medium">All Systems Operational</span>
          </div>
          <div className="h-4 w-px bg-white/10" />
          <LiveClock />
        </div>
      </header>

      {/* Grid Layout */}
      <div className="p-6 grid grid-cols-12 gap-5 auto-rows-min">

        {/* ─ 1. Stadium Health ─ */}
        <div className="col-span-12 lg:col-span-4 glass-card p-6 animate-slide-in delay-1 glow-emerald">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Stadium Health</h2>
            <span className="badge badge-success">Operational</span>
          </div>
          <div className="flex items-center gap-6">
            <div className="relative">
              <ProgressRing pct={94} size={110} stroke={8} color="#10b981" />
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-bold text-white">94</span>
                <span className="text-[10px] text-gray-400 -mt-1">HEALTH</span>
              </div>
            </div>
            <div className="flex-1 space-y-3">
              <MiniBar pct={78} label="Capacity" value="62,400 / 80,000" color="bg-cyan-500" />
              <MiniBar pct={94} label="Systems" value="94%" color="bg-emerald-500" />
              <MiniBar pct={88} label="Safety" value="88%" color="bg-emerald-400" />
            </div>
          </div>
        </div>

        {/* ─ 2. Crowd Heatmap ─ */}
        <div className="col-span-12 lg:col-span-8 glass-card p-6 animate-slide-in delay-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Crowd Density Heatmap</h2>
            <span className="text-xs text-gray-500">Live • 62,400 fans</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {crowdZones.map((zone) => (
              <div
                key={zone.name}
                className={`relative p-3 rounded-xl border transition-all duration-300 ${
                  zone.density >= 90
                    ? 'bg-rose-500/10 border-rose-500/30'
                    : zone.density >= 70
                    ? 'bg-amber-500/10 border-amber-500/20'
                    : zone.density >= 50
                    ? 'bg-amber-400/5 border-white/[0.06]'
                    : 'bg-emerald-500/5 border-white/[0.06]'
                }`}
              >
                {zone.density >= 90 && (
                  <div className="absolute top-2 right-2 w-2 h-2 rounded-full bg-rose-400 animate-pulse-slow" />
                )}
                <p className="text-xs text-gray-400 mb-1 truncate">{zone.name}</p>
                <div className="flex items-end gap-1">
                  <span className={`text-xl font-bold ${
                    zone.density >= 90 ? 'text-rose-400' : zone.density >= 70 ? 'text-amber-400' : 'text-emerald-400'
                  }`}>
                    {zone.density}%
                  </span>
                </div>
                <div className="mt-2 h-1 rounded-full bg-white/[0.06] overflow-hidden">
                  <div
                    className={`h-full rounded-full ${zone.color} transition-all duration-1000`}
                    style={{ width: `${zone.density}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ─ 3. Volunteer Deployment ─ */}
        <div className="col-span-12 sm:col-span-6 lg:col-span-3 glass-card p-6 animate-slide-in delay-3">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Volunteer Deployment</h2>
          <div className="flex items-center gap-4 mb-4">
            <div className="relative">
              <ProgressRing pct={75} size={80} stroke={6} color="#06b6d4" />
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-lg font-bold text-white">45</span>
                <span className="text-[9px] text-gray-500">/60</span>
              </div>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">75%</p>
              <p className="text-xs text-gray-500">Deployed</p>
            </div>
          </div>
          <div className="space-y-2">
            {volunteerZones.map((v) => (
              <div key={v.zone} className="flex items-center justify-between text-xs">
                <span className="text-gray-400">{v.zone}</span>
                <span className="text-white font-medium">{v.count}/{v.total}</span>
              </div>
            ))}
          </div>
        </div>

        {/* ─ 4. Incident Counter ─ */}
        <div className="col-span-12 sm:col-span-6 lg:col-span-3 glass-card p-6 animate-slide-in delay-4">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Incidents</h2>
          <div className="flex gap-4 mb-5">
            <div className="flex-1 text-center p-3 rounded-xl bg-rose-500/10 border border-rose-500/20">
              <p className="text-3xl font-bold text-rose-400">2</p>
              <p className="text-[10px] text-gray-400 mt-1 uppercase">Active</p>
            </div>
            <div className="flex-1 text-center p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
              <p className="text-3xl font-bold text-emerald-400">7</p>
              <p className="text-[10px] text-gray-400 mt-1 uppercase">Resolved</p>
            </div>
          </div>
          <div className="space-y-2">
            {[
              { label: 'Critical', color: 'bg-rose-500', count: 1 },
              { label: 'High', color: 'bg-orange-500', count: 1 },
              { label: 'Medium', color: 'bg-amber-500', count: 3 },
              { label: 'Low', color: 'bg-cyan-500', count: 4 },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${item.color}`} />
                  <span className="text-gray-400">{item.label}</span>
                </div>
                <span className="text-white font-medium">{item.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* ─ 5. Active Alerts ─ */}
        <div className="col-span-12 lg:col-span-6 glass-card p-6 animate-slide-in delay-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Active Alerts</h2>
            <span className="text-xs text-gray-500">{alerts.length} alerts</span>
          </div>
          <div className="space-y-3 max-h-[260px] overflow-y-auto pr-1">
            {alerts.map((alert, i) => {
              const cfg = severityConfig[alert.severity];
              return (
                <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-white/[0.02] border border-white/[0.04] hover:bg-white/[0.04] transition-colors">
                  <div className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 ${cfg.dot}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`badge ${cfg.badge}`}>{alert.severity}</span>
                      <span className="text-[10px] text-gray-600">{alert.zone}</span>
                    </div>
                    <p className="text-sm text-gray-300 leading-snug">{alert.message}</p>
                  </div>
                  <span className="text-[10px] text-gray-600 whitespace-nowrap flex-shrink-0">{alert.time}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* ─ 6. AI Recommendations ─ */}
        <div className="col-span-12 lg:col-span-6 glass-card p-6 animate-slide-in delay-6 glow-cyan">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">AI Recommendations</h2>
            <span className="text-xs text-cyan-400 animate-pulse-slow">● AI Active</span>
          </div>
          <div className="space-y-4">
            {aiRecommendations.map((rec, i) => (
              <div key={i} className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.05] hover:border-cyan-500/20 transition-colors">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${rec.agentColor}`}>
                    {rec.agent}
                  </span>
                  <span className={`badge ${rec.priority === 'high' ? 'badge-high' : 'badge-medium'}`}>{rec.priority}</span>
                </div>
                <p className="text-sm text-gray-300 mb-3 leading-relaxed">{rec.action}</p>
                <div className="flex items-center gap-3">
                  <div className="flex-1 h-1.5 rounded-full bg-white/[0.06] overflow-hidden">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-cyan-400 transition-all duration-1000"
                      style={{ width: `${rec.confidence}%` }}
                    />
                  </div>
                  <span className="text-xs text-cyan-400 font-semibold tabular-nums">{rec.confidence}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ─ 7. Transportation ─ */}
        <div className="col-span-12 sm:col-span-6 lg:col-span-4 glass-card p-6 animate-slide-in delay-7">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Transportation</h2>
          <div className="space-y-4">
            <MiniBar pct={72} label="Shuttle Load" value="72%" color="bg-amber-500" />
            <MiniBar pct={45} label="Parking Capacity" value="45%" color="bg-cyan-500" />
            <MiniBar pct={63} label="Gate A Congestion" value="63%" color="bg-amber-400" />
            <MiniBar pct={28} label="Gate B Congestion" value="28%" color="bg-emerald-500" />
            <MiniBar pct={81} label="Gate C Congestion" value="81%" color="bg-rose-500" />
          </div>
          <div className="mt-4 p-3 rounded-lg bg-cyan-500/5 border border-cyan-500/10">
            <p className="text-xs text-cyan-300">
              <span className="font-semibold">AI Prediction:</span> Peak shuttle demand expected at T+85min. Pre-positioning 4 additional buses.
            </p>
          </div>
        </div>

        {/* ─ 8. Sustainability ─ */}
        <div className="col-span-12 sm:col-span-6 lg:col-span-4 glass-card p-6 animate-slide-in delay-8">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Sustainability</h2>
          <div className="space-y-4">
            {[
              { label: 'Energy', value: '2,450 kWh', trend: '↓ 12%', trendColor: 'text-emerald-400', icon: '⚡' },
              { label: 'Waste', value: '890 kg', trend: '↑ 5%', trendColor: 'text-amber-400', icon: '♻' },
              { label: 'Water', value: '12,400 L', trend: '↓ 8%', trendColor: 'text-emerald-400', icon: '💧' },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/[0.04]">
                <div className="flex items-center gap-3">
                  <span className="text-lg">{item.icon}</span>
                  <div>
                    <p className="text-xs text-gray-500">{item.label}</p>
                    <p className="text-sm font-semibold text-white">{item.value}</p>
                  </div>
                </div>
                <span className={`text-xs font-medium ${item.trendColor}`}>{item.trend}</span>
              </div>
            ))}
          </div>
          <div className="mt-4 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            <span className="text-[10px] text-emerald-400 font-medium">Crowd-correlated optimization active</span>
          </div>
        </div>

        {/* ─ Quick Stats Footer ─ */}
        <div className="col-span-12 lg:col-span-4 glass-card p-6 animate-slide-in delay-8 flex flex-col justify-center">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Match Status</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Match</span>
              <span className="text-sm font-semibold text-white">USA vs Brazil</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Time</span>
              <span className="text-sm font-semibold text-amber-400">67:23 — 2nd Half</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Score</span>
              <span className="text-sm font-bold text-white">2 — 1</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Weather</span>
              <span className="text-sm text-gray-300">☀ 28°C • Clear</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Next Event</span>
              <span className="text-sm text-gray-300">Halftime Show @ 90+</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
