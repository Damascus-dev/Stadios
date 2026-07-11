'use client';

import { useEffect, useState } from 'react';
import { getAlerts, type AlertItem } from '@/lib/api';

type Severity = 'critical' | 'high' | 'medium' | 'low';

function formatTimestamp(iso: string): string {
  const d = new Date(iso);
  const now = new Date();
  const diff = Math.floor((now.getTime() - d.getTime()) / 1000);
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  return `${Math.floor(diff / 3600)}h ago`;
}

interface Alert {
  id: string;
  severity: Severity;
  title: string;
  description: string;
  zone: string;
  time: string;
  status: 'active' | 'resolved';
  recommendedAction: string;
}

const fallbackAlerts: Alert[] = [
  {
    id: 'INC-001',
    severity: 'critical',
    title: 'Medical Emergency — Section 112',
    description: 'Fan collapsed in Section 112, Row H, Seat 14. Medical team dispatched. AED unit requested from nearest station.',
    zone: 'North Stand',
    time: '2 min ago',
    status: 'active',
    recommendedAction: 'Clear adjacent rows. Medical team ETA: 90 seconds. Notify stadium medical coordinator.',
  },
  {
    id: 'INC-002',
    severity: 'high',
    title: 'Overcrowding — East Wing Food Court',
    description: 'Crowd density at 95% capacity. Bottleneck forming at south entrance of food court area. Risk of crush incident.',
    zone: 'East Wing',
    time: '8 min ago',
    status: 'active',
    recommendedAction: 'Activate crowd flow diversion via South Corridor. Deploy 3 additional stewards. Close south entrance temporarily.',
  },
  {
    id: 'INC-003',
    severity: 'medium',
    title: 'Elevator 3B Out of Service',
    description: 'Elevator 3B in West Concourse has stopped responding. Maintenance team notified. Accessibility rerouting automatically activated.',
    zone: 'West Concourse',
    time: '15 min ago',
    status: 'active',
    recommendedAction: 'Redirect wheelchair users to Elevator 3A or Ramp 4. Post signage. ETA for repair: ~25 minutes.',
  },
  {
    id: 'INC-004',
    severity: 'medium',
    title: 'Power Fluctuation — Lighting Grid B',
    description: 'Intermittent power fluctuation detected in Lighting Grid B covering South Stand sections 200-215. Backup systems on standby.',
    zone: 'South Stand',
    time: '22 min ago',
    status: 'active',
    recommendedAction: 'Engineering team dispatched. Switch to backup power if fluctuation persists beyond 5 min threshold.',
  },
  {
    id: 'INC-005',
    severity: 'low',
    title: 'Parking Lot D — 85% Capacity',
    description: 'Parking Lot D approaching maximum capacity. Lot E still at 40% availability. Updated signage required for incoming vehicles.',
    zone: 'Exterior',
    time: '31 min ago',
    status: 'active',
    recommendedAction: 'Update digital highway signs to redirect to Lot E. Alert shuttle service for increased demand.',
  },
  {
    id: 'INC-006',
    severity: 'low',
    title: 'Water Pressure Drop — Section 300 Restrooms',
    description: 'Minor water pressure reduction in Section 300 restroom facilities. Functional but below optimal pressure.',
    zone: 'West Concourse',
    time: '45 min ago',
    status: 'resolved',
    recommendedAction: 'Facilities team adjusted pressure valves. Monitoring for recurrence.',
  },
  {
    id: 'INC-007',
    severity: 'high',
    title: 'Unauthorized Access Attempt — Media Zone',
    description: 'Security detected unauthorized credential scan at Media Center entrance. Individual detained by security.',
    zone: 'Media Center',
    time: '1 hr ago',
    status: 'resolved',
    recommendedAction: 'Credential verified as expired. Individual escorted to Guest Services for reissue.',
  },
];

const severityConfig: Record<Severity, { badge: string; border: string; dot: string; bg: string }> = {
  critical: { badge: 'badge-critical', border: 'border-l-rose-500', dot: 'bg-rose-500', bg: 'bg-rose-500/5' },
  high: { badge: 'badge-high', border: 'border-l-orange-500', dot: 'bg-orange-500', bg: 'bg-orange-500/5' },
  medium: { badge: 'badge-medium', border: 'border-l-amber-500', dot: 'bg-amber-500', bg: 'bg-amber-500/5' },
  low: { badge: 'badge-low', border: 'border-l-cyan-500', dot: 'bg-cyan-500', bg: 'bg-cyan-500/5' },
};

export default function AlertsPage() {
  const [filter, setFilter] = useState<'all' | 'active' | 'resolved'>('all');
  const [severityFilter, setSeverityFilter] = useState<'all' | Severity>('all');
  const [alerts, setAlerts] = useState<Alert[]>(fallbackAlerts);

  useEffect(() => {
    getAlerts()
      .then((apiAlerts) => {
        if (apiAlerts?.length) {
          setAlerts(apiAlerts.map((a: AlertItem) => ({
            id: a.id,
            severity: a.severity as Severity,
            title: a.title || a.message,
            description: a.message,
            zone: a.zone,
            time: formatTimestamp(a.timestamp),
            status: a.acknowledged === false ? 'active' : 'resolved',
            recommendedAction: a.recommended_action || '',
          })));
        }
      })
      .catch(() => {
        // fallback to mock data
      });
  }, []);

  const filtered = alerts.filter((a) => {
    if (filter !== 'all' && a.status !== filter) return false;
    if (severityFilter !== 'all' && a.severity !== severityFilter) return false;
    return true;
  });

  const activeCount = alerts.filter((a) => a.status === 'active').length;
  const resolvedCount = alerts.filter((a) => a.status === 'resolved').length;

  return (
    <div className="md:ml-[68px] min-h-screen bg-gradient-mesh bg-grid-pattern">
      {/* Header */}
      <header className="sticky top-0 z-40 glass-panel border-b border-white/[0.06] px-6 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-white">Alerts & Incidents</h1>
          <p className="text-xs text-gray-500">Real-time incident monitoring and response</p>
        </div>
      </header>

      <div className="p-6 max-w-5xl mx-auto">
        {/* Stats Row */}
        <div className="grid grid-cols-3 gap-4 mb-6 animate-slide-in delay-1">
          <div className="glass-card p-4 text-center">
            <p className="text-3xl font-bold text-rose-400">{activeCount}</p>
            <p className="text-xs text-gray-500 mt-1 uppercase tracking-wider">Active</p>
          </div>
          <div className="glass-card p-4 text-center">
            <p className="text-3xl font-bold text-emerald-400">{resolvedCount}</p>
            <p className="text-xs text-gray-500 mt-1 uppercase tracking-wider">Resolved</p>
          </div>
          <div className="glass-card p-4 text-center">
            <p className="text-3xl font-bold text-white">{alerts.length}</p>
            <p className="text-xs text-gray-500 mt-1 uppercase tracking-wider">Total</p>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3 mb-6 animate-slide-in delay-2">
          <div className="flex gap-1 p-1 rounded-xl bg-white/[0.03] border border-white/[0.06]">
            {(['all', 'active', 'resolved'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  filter === f
                    ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/20'
                    : 'text-gray-400 hover:text-gray-300 border border-transparent'
                }`}
              >
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>
          <div className="h-6 w-px bg-white/10" />
          <div className="flex gap-1 p-1 rounded-xl bg-white/[0.03] border border-white/[0.06]">
            {(['all', 'critical', 'high', 'medium', 'low'] as const).map((s) => (
              <button
                key={s}
                onClick={() => setSeverityFilter(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
                  severityFilter === s
                    ? 'bg-white/[0.08] text-white border border-white/[0.1]'
                    : 'text-gray-500 hover:text-gray-300 border border-transparent'
                }`}
              >
                {s !== 'all' && <div className={`w-1.5 h-1.5 rounded-full ${severityConfig[s as Severity]?.dot}`} />}
                {s.charAt(0).toUpperCase() + s.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Alert List */}
        <div className="space-y-4">
          {filtered.map((alert, i) => {
            const cfg = severityConfig[alert.severity];
            return (
              <div
                key={alert.id}
                className={`glass-card border-l-[3px] ${cfg.border} ${cfg.bg} p-5 animate-slide-in`}
                style={{ animationDelay: `${0.3 + i * 0.08}s`, opacity: 0 }}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2 flex-wrap">
                      <span className={`badge ${cfg.badge}`}>{alert.severity}</span>
                      <span className={`badge ${alert.status === 'active' ? 'badge-critical' : 'badge-success'}`}>
                        {alert.status}
                      </span>
                      <span className="text-[10px] text-gray-600 font-mono">{alert.id}</span>
                    </div>
                    <h3 className="text-sm font-semibold text-white mb-1.5">{alert.title}</h3>
                    <p className="text-sm text-gray-400 leading-relaxed mb-3">{alert.description}</p>
                    <div className="p-3 rounded-lg bg-white/[0.02] border border-white/[0.04]">
                      <p className="text-xs text-gray-300">
                        <span className="text-cyan-400 font-semibold">Recommended Action: </span>
                        {alert.recommendedAction}
                      </p>
                    </div>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <p className="text-xs text-gray-500">{alert.zone}</p>
                    <p className="text-[10px] text-gray-600 mt-1">{alert.time}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {filtered.length === 0 && (
          <div className="glass-card p-12 text-center animate-fade-in">
            <p className="text-gray-500 text-sm">No alerts match the selected filters.</p>
          </div>
        )}
      </div>
    </div>
  );
}
