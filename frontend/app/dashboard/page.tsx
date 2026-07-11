'use client';

import { useEffect, useState } from 'react';
import { getDashboard, DashboardData } from '@/lib/api';

const severityConfig: Record<string, { badge: string; dot: string }> = {
  critical: { badge: 'badge-critical', dot: 'bg-rose-500' },
  high: { badge: 'badge-high', dot: 'bg-orange-500' },
  medium: { badge: 'badge-medium', dot: 'bg-amber-500' },
  low: { badge: 'badge-low', dot: 'bg-cyan-500' },
};

function densityColor(density: number): string {
  if (density >= 90) return 'from-rose-500 to-rose-600 shadow-rose-500/20';
  if (density >= 75) return 'from-orange-500 to-orange-600 shadow-orange-500/20';
  if (density >= 50) return 'from-amber-500 to-amber-600 shadow-amber-500/20';
  return 'from-emerald-500 to-emerald-600 shadow-emerald-500/20';
}

function densityBg(density: number): string {
  if (density >= 90) return 'bg-rose-500/10 border-rose-500/30';
  if (density >= 75) return 'bg-orange-500/10 border-orange-500/20';
  if (density >= 50) return 'bg-amber-500/5 border-white/[0.06]';
  return 'bg-emerald-500/5 border-white/[0.06]';
}

function densityText(density: number): string {
  if (density >= 90) return 'text-rose-400';
  if (density >= 75) return 'text-orange-400';
  if (density >= 50) return 'text-amber-400';
  return 'text-emerald-400';
}

function densityBar(density: number): string {
  if (density >= 90) return 'bg-rose-500';
  if (density >= 75) return 'bg-orange-500';
  if (density >= 50) return 'bg-amber-500';
  return 'bg-emerald-500';
}

function deltaIcon(trend: string): string {
  if (trend === 'rising') return '\u2191';
  if (trend === 'falling') return '\u2193';
  return '\u2192';
}

function deltaColor(trend: string): string {
  if (trend === 'rising') return 'text-rose-400';
  if (trend === 'falling') return 'text-emerald-400';
  return 'text-gray-500';
}

function formatTime(iso: string): string {
  const d = new Date(iso);
  const now = new Date();
  const diff = Math.floor((now.getTime() - d.getTime()) / 1000);
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  return `${Math.floor(diff / 3600)}h ago`;
}

function LiveClock() {
  const [time, setTime] = useState('');
  useEffect(() => {
    const update = () => {
      setTime(new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }));
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

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboard()
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="md:ml-[68px] min-h-screen bg-gradient-mesh bg-grid-pattern flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mx-auto mb-4 animate-pulse">
            <span className="text-xl">{'\u231A'}</span>
          </div>
          <p className="text-sm text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="md:ml-[68px] min-h-screen bg-gradient-mesh bg-grid-pattern flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 rounded-2xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center mx-auto mb-4">
            <span className="text-xl">{'\u26A0'}</span>
          </div>
          <p className="text-sm text-gray-400">Dashboard data unavailable</p>
        </div>
      </div>
    );
  }

  const d = data;
  const zones = d.crowd_heat?.zones || [];
  const alerts = d.active_alerts?.alerts || [];
  const recs = d.ai_recommendations || [];
  const vol = d.volunteer_status;
  const inc = d.incident_count;
  const trans = d.transportation;
  const sustain = d.sustainability;
  const health = d.stadium_health;

  return (
    <div className="md:ml-[68px] min-h-screen bg-gradient-mesh bg-grid-pattern">
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
            <div className={`w-2 h-2 rounded-full animate-pulse-slow ${health.status === 'green' ? 'bg-emerald-400' : health.status === 'yellow' ? 'bg-amber-400' : 'bg-rose-400'}`} />
            <span className={`text-xs font-medium ${health.status === 'green' ? 'text-emerald-400' : health.status === 'yellow' ? 'text-amber-400' : 'text-rose-400'}`}>
              {health.status === 'green' ? 'All Systems Operational' : health.status === 'yellow' ? 'Degraded Performance' : 'Critical Issues'}
            </span>
          </div>
          <div className="h-4 w-px bg-white/10" />
          <LiveClock />
        </div>
      </header>

      <div className="p-6 grid grid-cols-12 gap-5 auto-rows-min">
        {/* 1. Stadium Health */}
        <div className="col-span-12 lg:col-span-4 glass-card p-6 animate-slide-in delay-1 glow-emerald">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Stadium Health</h2>
            <span className={`badge ${health.status === 'green' ? 'badge-success' : health.status === 'yellow' ? 'badge-medium' : 'badge-critical'}`}>
              {health.status === 'green' ? 'Operational' : health.status === 'yellow' ? 'Degraded' : 'Critical'}
            </span>
          </div>
          <div className="flex items-center gap-6">
            <div className="relative">
              <ProgressRing pct={health.overall_score} size={110} stroke={8} color={health.status === 'green' ? '#10b981' : health.status === 'yellow' ? '#f59e0b' : '#f43f5e'} />
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-bold text-white">{Math.round(health.overall_score)}</span>
                <span className="text-[10px] text-gray-400 -mt-1">HEALTH</span>
              </div>
            </div>
            <div className="flex-1 space-y-3">
              <MiniBar pct={health.capacity_pct} label="Capacity" value={`${Math.round(health.capacity_pct)}%`} color="bg-cyan-500" />
              <MiniBar pct={health.overall_score} label="Systems" value={`${Math.round(health.overall_score)}%`} color="bg-emerald-500" />
              <MiniBar pct={Math.min(100, health.active_zones * 7.14)} label="Active Zones" value={`${health.active_zones}/14`} color="bg-emerald-400" />
            </div>
          </div>
        </div>

        {/* 2. Crowd Heatmap */}
        <div className="col-span-12 lg:col-span-8 glass-card p-6 animate-slide-in delay-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Crowd Density Heatmap</h2>
            <span className="text-xs text-gray-500">Live</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {zones.map((zone) => (
              <div key={zone.zone_id} className={`relative p-3 rounded-xl border transition-all duration-300 ${densityBg(zone.density_pct)}`}>
                {zone.risk_level === 'critical' && (
                  <div className="absolute top-2 right-2 w-2 h-2 rounded-full bg-rose-400 animate-pulse-slow" />
                )}
                <p className="text-xs text-gray-400 mb-1 truncate">{zone.name}</p>
                <div className="flex items-end gap-1">
                  <span className={`text-xl font-bold ${densityText(zone.density_pct)}`}>
                    {zone.density_pct}%
                  </span>
                  <span className={`text-xs ${deltaColor(zone.trend)}`}>{deltaIcon(zone.trend)}</span>
                </div>
                <div className="mt-2 h-1 rounded-full bg-white/[0.06] overflow-hidden">
                  <div className={`h-full rounded-full ${densityBar(zone.density_pct)} transition-all duration-1000`} style={{ width: `${zone.density_pct}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 3. Volunteer Deployment */}
        <div className="col-span-12 sm:col-span-6 lg:col-span-3 glass-card p-6 animate-slide-in delay-3">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Volunteer Deployment</h2>
          <div className="flex items-center gap-4 mb-4">
            <div className="relative">
              <ProgressRing pct={vol.total > 0 ? (vol.deployed / vol.total) * 100 : 0} size={80} stroke={6} color="#06b6d4" />
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-lg font-bold text-white">{vol.deployed}</span>
                <span className="text-[9px] text-gray-500">/{vol.total}</span>
              </div>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{vol.total > 0 ? Math.round((vol.deployed / vol.total) * 100) : 0}%</p>
              <p className="text-xs text-gray-500">Deployed</p>
            </div>
          </div>
          <div className="space-y-2">
            {vol.zones.slice(0, 6).map((v) => (
              <div key={v.zone_id} className="flex items-center justify-between text-xs">
                <span className="text-gray-400 truncate mr-2">{v.zone_name}</span>
                <span className="text-white font-medium">{v.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* 4. Incident Counter */}
        <div className="col-span-12 sm:col-span-6 lg:col-span-3 glass-card p-6 animate-slide-in delay-4">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Incidents</h2>
          <div className="flex gap-4 mb-5">
            <div className="flex-1 text-center p-3 rounded-xl bg-rose-500/10 border border-rose-500/20">
              <p className="text-3xl font-bold text-rose-400">{inc.active}</p>
              <p className="text-[10px] text-gray-400 mt-1 uppercase">Active</p>
            </div>
            <div className="flex-1 text-center p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
              <p className="text-3xl font-bold text-emerald-400">{inc.resolved}</p>
              <p className="text-[10px] text-gray-400 mt-1 uppercase">Resolved</p>
            </div>
          </div>
          <div className="space-y-2">
            {[
              { label: 'Critical', key: 'critical' as const, color: 'bg-rose-500' },
              { label: 'High', key: 'high' as const, color: 'bg-orange-500' },
              { label: 'Medium', key: 'medium' as const, color: 'bg-amber-500' },
              { label: 'Low', key: 'low' as const, color: 'bg-cyan-500' },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${item.color}`} />
                  <span className="text-gray-400">{item.label}</span>
                </div>
                <span className="text-white font-medium">{inc.by_severity[item.key]}</span>
              </div>
            ))}
          </div>
        </div>

        {/* 5. Active Alerts */}
        <div className="col-span-12 lg:col-span-6 glass-card p-6 animate-slide-in delay-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Active Alerts</h2>
            <span className="text-xs text-gray-500">{alerts.length} alerts</span>
          </div>
          <div className="space-y-3 max-h-[260px] overflow-y-auto pr-1">
            {alerts.map((alert, i) => {
              const cfg = severityConfig[alert.severity] || severityConfig.low;
              return (
                <div key={alert.id || i} className="flex items-start gap-3 p-3 rounded-xl bg-white/[0.02] border border-white/[0.04] hover:bg-white/[0.04] transition-colors">
                  <div className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 ${cfg.dot}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`badge ${cfg.badge}`}>{alert.severity}</span>
                      <span className="text-[10px] text-gray-600">{alert.zone}</span>
                    </div>
                    <p className="text-sm text-gray-300 leading-snug">{alert.message}</p>
                  </div>
                  <span className="text-[10px] text-gray-600 whitespace-nowrap flex-shrink-0">{formatTime(alert.timestamp)}</span>
                </div>
              );
            })}
            {alerts.length === 0 && (
              <p className="text-sm text-gray-500 text-center py-4">No active alerts — all clear</p>
            )}
          </div>
        </div>

        {/* 6. AI Recommendations */}
        <div className="col-span-12 lg:col-span-6 glass-card p-6 animate-slide-in delay-6 glow-cyan">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">AI Recommendations</h2>
            <span className="text-xs text-cyan-400 animate-pulse-slow">{'\u25CF'} AI Active</span>
          </div>
          <div className="space-y-4">
            {recs.map((rec, i) => {
              const agentColor = rec.agent_source === 'navigation' ? 'text-cyan-400 bg-cyan-400/10 border-cyan-400/20'
                : rec.agent_source === 'operations' ? 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20'
                : 'text-amber-400 bg-amber-400/10 border-amber-400/20';
              return (
                <div key={rec.id || i} className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.05] hover:border-cyan-500/20 transition-colors">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${agentColor}`}>
                      {rec.agent_source}
                    </span>
                    <span className={`badge ${rec.priority === 'critical' ? 'badge-critical' : rec.priority === 'high' ? 'badge-high' : 'badge-medium'}`}>
                      {rec.priority}
                    </span>
                  </div>
                  <p className="text-sm text-gray-300 mb-3 leading-relaxed">{rec.description}</p>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-1.5 rounded-full bg-white/[0.06] overflow-hidden">
                      <div className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-cyan-400 transition-all duration-1000" style={{ width: `${rec.confidence * 100}%` }} />
                    </div>
                    <span className="text-xs text-cyan-400 font-semibold tabular-nums">{Math.round(rec.confidence * 100)}%</span>
                  </div>
                </div>
              );
            })}
            {recs.length === 0 && (
              <p className="text-sm text-gray-500 text-center py-4">No recommendations — all zones stable</p>
            )}
          </div>
        </div>

        {/* 7. Transportation */}
        <div className="col-span-12 sm:col-span-6 lg:col-span-4 glass-card p-6 animate-slide-in delay-7">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Transportation</h2>
          <div className="space-y-4">
            <MiniBar pct={trans.shuttle_load_pct} label="Shuttle Load" value={`${trans.shuttle_load_pct}%`} color="bg-amber-500" />
            <MiniBar pct={trans.parking_capacity_pct} label="Parking Capacity" value={`${trans.parking_capacity_pct}%`} color="bg-cyan-500" />
            {(trans.exit_congestion || []).slice(0, 3).map((exit) => (
              <MiniBar
                key={exit.exit_id}
                pct={exit.congestion_pct}
                label={exit.name}
                value={`${exit.congestion_pct}%`}
                color={exit.congestion_pct >= 80 ? 'bg-rose-500' : exit.congestion_pct >= 60 ? 'bg-amber-500' : 'bg-emerald-500'}
              />
            ))}
          </div>
          <div className="mt-4 p-3 rounded-lg bg-cyan-500/5 border border-cyan-500/10">
            <p className="text-xs text-cyan-300">
              <span className="font-semibold">Prediction:</span> {trans.prediction}
            </p>
          </div>
        </div>

        {/* 8. Sustainability */}
        <div className="col-span-12 sm:col-span-6 lg:col-span-4 glass-card p-6 animate-slide-in delay-8">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Sustainability</h2>
          <div className="space-y-4">
            {[
              { label: 'Energy', value: `${sustain.energy_load_kwh.toLocaleString()} kWh`, icon: '\u26A1', trend: '', trendColor: '' },
              { label: 'Waste', value: `${sustain.waste_generation_kg.toLocaleString()} kg`, icon: '\u267B', trend: '', trendColor: '' },
              { label: 'Water', value: `${sustain.water_usage_liters.toLocaleString()} L`, icon: '\uD83D\uDCA7', trend: '', trendColor: '' },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/[0.04]">
                <div className="flex items-center gap-3">
                  <span className="text-lg">{item.icon}</span>
                  <div>
                    <p className="text-xs text-gray-500">{item.label}</p>
                    <p className="text-sm font-semibold text-white">{item.value}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            <span className="text-[10px] text-emerald-400 font-medium">
              Crowd-correlated: {Math.round(sustain.crowd_correlation_factor * 100)}%
            </span>
          </div>
        </div>

        {/* Match Status */}
        <div className="col-span-12 lg:col-span-4 glass-card p-6 animate-slide-in delay-8 flex flex-col justify-center">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Match Status</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Match</span>
              <span className="text-sm font-semibold text-white">USA vs Brazil</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Attendance</span>
              <span className="text-sm font-semibold text-amber-400">{d.stadium_health.capacity_pct}% capacity</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Score</span>
              <span className="text-sm font-bold text-white">2 — 1</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Weather</span>
              <span className="text-sm text-gray-300">{'\u2600'} {28}°C • Clear</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Next Event</span>
              <span className="text-sm text-gray-300">Halftime Show</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
