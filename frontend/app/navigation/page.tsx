'use client';

import { useState } from 'react';

const zones = [
  'Gate A Entrance',
  'Gate B Entrance',
  'Gate C Entrance',
  'Gate D Entrance',
  'Section 114, Row A',
  'Section 214, Row F',
  'Section 312, Row K',
  'VIP Lounge - Level 3',
  'East Wing Food Court',
  'West Concourse Restrooms',
  'First Aid Station 1',
  'Accessible Seating Area',
  'Family Zone',
  'Media Center',
];

const routeSteps = [
  { step: 1, instruction: 'Exit Gate A Entrance and proceed straight', distance: '120m', eta: '2 min', congestion: 'low' },
  { step: 2, instruction: 'Turn left at Main Concourse — follow blue signage', distance: '200m', eta: '3 min', congestion: 'medium' },
  { step: 3, instruction: 'Take Elevator 2A to Level 2 (accessible)', distance: '—', eta: '1 min', congestion: 'low' },
  { step: 4, instruction: 'Follow corridor past Food Court East entrance', distance: '150m', eta: '2 min', congestion: 'high' },
  { step: 5, instruction: 'Arrive at Section 214, Row F — Seat 12', distance: '30m', eta: '1 min', congestion: 'low' },
];

const congestionColors: Record<string, string> = {
  low: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
  medium: 'text-amber-400 bg-amber-400/10 border-amber-400/20',
  high: 'text-rose-400 bg-rose-400/10 border-rose-400/20',
};

export default function NavigationPage() {
  const [from, setFrom] = useState('Gate A Entrance');
  const [to, setTo] = useState('Section 214, Row F');
  const [accessibility, setAccessibility] = useState({ wheelchair: true, vision: false, hearing: false });

  return (
    <div className="ml-[68px] min-h-screen bg-gradient-mesh bg-grid-pattern">
      {/* Header */}
      <header className="sticky top-0 z-40 glass-panel border-b border-white/[0.06] px-6 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-white">Navigation</h1>
          <p className="text-xs text-gray-500">AI-powered wayfinding • Accessibility-first routing</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="badge badge-success">Route Active</span>
        </div>
      </header>

      <div className="p-6 grid grid-cols-12 gap-5">
        {/* Left Panel — Controls */}
        <div className="col-span-12 lg:col-span-3 space-y-5 animate-slide-in delay-1">
          {/* Route Selection */}
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
                    <option key={z} value={z} className="bg-[#1a1f36] text-white">{z}</option>
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
                    <option key={z} value={z} className="bg-[#1a1f36] text-white">{z}</option>
                  ))}
                </select>
              </div>
            </div>

            <button className="w-full mt-4 py-2.5 px-4 bg-gradient-to-r from-cyan-500 to-cyan-600 text-white text-sm font-semibold rounded-xl shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/30 transition-all hover:scale-[1.02] active:scale-[0.98]">
              Calculate Route
            </button>
          </div>

          {/* Accessibility Options */}
          <div className="glass-card p-5">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Accessibility</h2>
            <div className="space-y-3">
              {[
                { key: 'wheelchair', label: 'Wheelchair Access', icon: '♿' },
                { key: 'vision', label: 'Vision Assistance', icon: '👁' },
                { key: 'hearing', label: 'Hearing Support', icon: '👂' },
              ].map((opt) => (
                <label key={opt.key} className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-white/[0.03] transition-colors cursor-pointer">
                  <div
                    className={`w-5 h-5 rounded-md border-2 flex items-center justify-center transition-all ${
                      accessibility[opt.key as keyof typeof accessibility]
                        ? 'bg-cyan-500 border-cyan-500'
                        : 'border-gray-600'
                    }`}
                    onClick={() => setAccessibility(prev => ({ ...prev, [opt.key]: !prev[opt.key as keyof typeof prev] }))}
                  >
                    {accessibility[opt.key as keyof typeof accessibility] && (
                      <span className="text-white text-xs">✓</span>
                    )}
                  </div>
                  <span className="text-sm">{opt.icon}</span>
                  <span className="text-sm text-gray-300">{opt.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Language */}
          <div className="glass-card p-5">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3">Language</h2>
            <select className="w-full glass-input px-3 py-2.5 text-sm rounded-xl">
              <option className="bg-[#1a1f36]">English</option>
              <option className="bg-[#1a1f36]">Español</option>
              <option className="bg-[#1a1f36]">Português</option>
              <option className="bg-[#1a1f36]">Français</option>
              <option className="bg-[#1a1f36]">العربية</option>
            </select>
          </div>
        </div>

        {/* Map Area */}
        <div className="col-span-12 lg:col-span-9 space-y-5">
          <div className="glass-card p-1 animate-slide-in delay-2 overflow-hidden" style={{ minHeight: '400px' }}>
            <div className="relative w-full h-[400px] rounded-2xl bg-[#0d1220] border border-white/[0.04] flex items-center justify-center overflow-hidden">
              {/* Grid overlay effect */}
              <div className="absolute inset-0 bg-grid-pattern opacity-30" />
              {/* Fake map gradient */}
              <div className="absolute inset-0">
                <div className="absolute top-1/3 left-1/4 w-40 h-24 bg-cyan-500/10 rounded-2xl border border-cyan-500/20 animate-pulse-slow" />
                <div className="absolute top-1/2 left-1/2 w-32 h-20 bg-amber-500/10 rounded-2xl border border-amber-500/20" />
                <div className="absolute bottom-1/4 right-1/4 w-36 h-28 bg-emerald-500/10 rounded-2xl border border-emerald-500/20" />
                {/* Route line mock */}
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
              </div>
              {/* Center label */}
              <div className="relative z-10 text-center">
                <div className="animate-pulse-slow">
                  <div className="w-16 h-16 mx-auto rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mb-3">
                    <span className="text-2xl">🗺</span>
                  </div>
                  <p className="text-sm text-gray-400 font-medium">Interactive Map</p>
                  <p className="text-xs text-gray-600 mt-1">Leaflet integration ready</p>
                </div>
              </div>
            </div>
          </div>

          {/* Route Details */}
          <div className="glass-card p-6 animate-slide-in delay-3">
            <div className="flex items-center justify-between mb-5">
              <div>
                <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Route Details</h2>
                <p className="text-xs text-gray-500 mt-1">{from} → {to}</p>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className="text-xs text-gray-500">Total Distance</p>
                  <p className="text-sm font-semibold text-white">500m</p>
                </div>
                <div className="h-8 w-px bg-white/10" />
                <div className="text-right">
                  <p className="text-xs text-gray-500">Est. Time</p>
                  <p className="text-sm font-semibold text-cyan-400">~9 min</p>
                </div>
              </div>
            </div>

            <div className="space-y-0">
              {routeSteps.map((step, i) => (
                <div key={step.step} className="flex gap-4">
                  {/* Timeline */}
                  <div className="flex flex-col items-center">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${
                      i === 0 ? 'bg-emerald-500 text-white' : i === routeSteps.length - 1 ? 'bg-rose-500 text-white' : 'bg-white/[0.08] text-gray-400 border border-white/[0.1]'
                    }`}>
                      {step.step}
                    </div>
                    {i < routeSteps.length - 1 && (
                      <div className="w-px h-10 bg-white/[0.08]" />
                    )}
                  </div>
                  {/* Content */}
                  <div className="pb-4 flex-1">
                    <p className="text-sm text-gray-200 font-medium">{step.instruction}</p>
                    <div className="flex items-center gap-3 mt-1.5">
                      {step.distance !== '—' && (
                        <span className="text-xs text-gray-500">{step.distance}</span>
                      )}
                      <span className="text-xs text-gray-500">~{step.eta}</span>
                      <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${congestionColors[step.congestion]}`}>
                        {step.congestion}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-4 p-3 rounded-xl bg-cyan-500/5 border border-cyan-500/10">
              <p className="text-xs text-cyan-300">
                <span className="font-semibold">♿ Accessible Route:</span> This route uses elevators and wide corridors. No stairs. Estimated wheelchair time: ~11 min.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
