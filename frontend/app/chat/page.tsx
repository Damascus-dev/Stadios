'use client';

import { useState } from 'react';

type Agent = 'Navigation' | 'Operations' | 'Accessibility';

interface Message {
  id: number;
  role: 'user' | 'agent';
  agent?: Agent;
  text: string;
  time: string;
}

const agentConfig: Record<Agent, { color: string; bg: string; border: string; icon: string }> = {
  Navigation: { color: 'text-cyan-400', bg: 'bg-cyan-400/10', border: 'border-cyan-400/20', icon: '◎' },
  Operations: { color: 'text-emerald-400', bg: 'bg-emerald-400/10', border: 'border-emerald-400/20', icon: '◫' },
  Accessibility: { color: 'text-amber-400', bg: 'bg-amber-400/10', border: 'border-amber-400/20', icon: '♿' },
};

const initialMessages: Record<Agent, Message[]> = {
  Navigation: [
    { id: 1, role: 'user', text: 'I need to get from Gate A to Section 214. What\'s the fastest route?', time: '14:32' },
    { id: 2, role: 'agent', agent: 'Navigation', text: 'I\'ve calculated the optimal route for you. From Gate A, head straight through the Main Concourse, then take Elevator 2A to Level 2. Follow the corridor past the East Food Court to Section 214.\n\n📍 Total distance: 500m\n⏱ Estimated time: ~9 minutes\n🚦 Current congestion: Medium\n\nI\'ve also enabled accessibility mode since Elevator 2A is the best option for this route.', time: '14:32' },
    { id: 3, role: 'user', text: 'Is there a less crowded alternative?', time: '14:33' },
    { id: 4, role: 'agent', agent: 'Navigation', text: 'Yes! I can reroute you via the South Corridor. It\'s 50m longer but congestion is currently LOW. This route avoids the East Wing Food Court which is at 95% density right now.\n\n🔄 Alternative route: Gate A → South Corridor → Ramp 3B → Level 2 → Section 214\n⏱ Estimated time: ~11 minutes\n🚦 Congestion: Low\n\nWould you like me to switch to this route?', time: '14:33' },
  ],
  Operations: [
    { id: 1, role: 'user', text: 'What\'s the current volunteer status?', time: '14:20' },
    { id: 2, role: 'agent', agent: 'Operations', text: 'Here\'s the volunteer deployment overview:\n\n👥 45 of 60 volunteers currently deployed (75%)\n\n📊 Zone Breakdown:\n• Gate A: 8/10 ✅\n• North Stand: 12/15 ⚠️\n• Food Court: 10/12 ✅\n• VIP Area: 6/8 ✅\n• South Stand: 9/15 ⚠️\n\nI\'m recommending 5 additional volunteers for the South Stand and Gate A areas ahead of the expected 2nd-half crowd surge.', time: '14:20' },
  ],
  Accessibility: [
    { id: 1, role: 'user', text: 'Are there any accessibility issues right now?', time: '14:15' },
    { id: 2, role: 'agent', agent: 'Accessibility', text: 'I\'m tracking one active accessibility concern:\n\n⚠️ Elevator 3B (West Concourse) is currently out of service. I\'ve automatically activated rerouting for all accessibility-tagged navigation requests in that area.\n\n✅ All other accessible facilities are operational:\n• 12/12 wheelchair ramps: Active\n• 8/8 accessible restrooms: Open\n• Sensory room (Level 1): Available\n• Audio description service: Broadcasting\n\nI also recommend activating the backup wheelchair ramp at Section 300 — primary ramp queue is exceeding 8 minutes.', time: '14:15' },
  ],
};

export default function ChatPage() {
  const [activeAgent, setActiveAgent] = useState<Agent>('Navigation');
  const [inputValue, setInputValue] = useState('');
  const messages = initialMessages[activeAgent];

  return (
    <div className="ml-[68px] min-h-screen bg-gradient-mesh flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-40 glass-panel border-b border-white/[0.06] px-6 py-3">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-lg font-bold text-white">AI Chat</h1>
            <p className="text-xs text-gray-500">Talk to stadium AI agents in real-time</p>
          </div>
        </div>
      </header>

      {/* Agent Tabs */}
      <div className="px-6 pt-4">
        <div className="flex gap-2 animate-slide-in">
          {(Object.keys(agentConfig) as Agent[]).map((agent) => {
            const cfg = agentConfig[agent];
            const isActive = activeAgent === agent;
            return (
              <button
                key={agent}
                onClick={() => setActiveAgent(agent)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? `${cfg.bg} ${cfg.color} border ${cfg.border}`
                    : 'text-gray-400 hover:text-gray-300 hover:bg-white/[0.03] border border-transparent'
                }`}
              >
                <span>{cfg.icon}</span>
                <span>{agent}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 px-6 py-4 overflow-y-auto">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.map((msg, i) => {
            if (msg.role === 'user') {
              return (
                <div key={msg.id} className="flex justify-end animate-slide-in" style={{ animationDelay: `${i * 0.1}s` }}>
                  <div className="max-w-[75%]">
                    <div className="bg-gradient-to-br from-cyan-500/20 to-cyan-600/10 border border-cyan-500/20 rounded-2xl rounded-tr-md px-4 py-3">
                      <p className="text-sm text-gray-200 leading-relaxed">{msg.text}</p>
                    </div>
                    <p className="text-[10px] text-gray-600 mt-1 text-right">{msg.time}</p>
                  </div>
                </div>
              );
            }

            const cfg = msg.agent ? agentConfig[msg.agent] : agentConfig.Navigation;
            return (
              <div key={msg.id} className="flex justify-start animate-slide-in" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="max-w-[80%]">
                  <div className="flex items-center gap-2 mb-1.5">
                    <div className={`w-6 h-6 rounded-lg ${cfg.bg} border ${cfg.border} flex items-center justify-center text-xs`}>
                      {cfg.icon}
                    </div>
                    <span className={`text-xs font-semibold ${cfg.color}`}>{msg.agent}</span>
                  </div>
                  <div className="glass-card px-4 py-3 rounded-2xl rounded-tl-md">
                    <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-line">{msg.text}</p>
                  </div>
                  <p className="text-[10px] text-gray-600 mt-1">{msg.time}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Input Bar */}
      <div className="px-6 pb-6 pt-2">
        <div className="max-w-3xl mx-auto">
          <div className="glass-card p-2 flex items-center gap-2">
            <div className={`flex-shrink-0 w-8 h-8 rounded-xl ${agentConfig[activeAgent].bg} border ${agentConfig[activeAgent].border} flex items-center justify-center text-sm`}>
              {agentConfig[activeAgent].icon}
            </div>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={`Ask ${activeAgent} Agent...`}
              className="flex-1 bg-transparent text-sm text-gray-200 placeholder:text-gray-600 outline-none px-2 py-2"
            />
            <button className="flex-shrink-0 w-9 h-9 rounded-xl bg-gradient-to-r from-cyan-500 to-cyan-600 flex items-center justify-center text-white shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/30 transition-all hover:scale-105 active:scale-95">
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </button>
          </div>
          <p className="text-[10px] text-gray-600 mt-2 text-center">
            StadiumOS AI agents respond with real-time stadium data • All interactions are logged
          </p>
        </div>
      </div>
    </div>
  );
}
