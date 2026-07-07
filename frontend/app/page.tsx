import Link from "next/link";

const agents = [
  {
    icon: "◎",
    name: "Navigation Agent",
    desc: "Real-time wayfinding with accessibility-first routing, congestion avoidance, and multilingual guidance for 80,000+ fans.",
    color: "from-cyan-400 to-blue-500",
    glow: "shadow-cyan-500/20",
  },
  {
    icon: "◫",
    name: "Operations Agent",
    desc: "Stadium health monitoring, volunteer deployment, incident response, and sustainability tracking — all in one AI command center.",
    color: "from-emerald-400 to-teal-500",
    glow: "shadow-emerald-500/20",
  },
  {
    icon: "♿",
    name: "Accessibility Agent",
    desc: "Inclusive experience design for wheelchair users, vision/hearing impaired fans, and sensory-sensitive attendees.",
    color: "from-amber-400 to-orange-500",
    glow: "shadow-amber-500/20",
  },
];

export default function LandingPage() {
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-[#0a0e1a]">
        <div className="absolute inset-0 bg-gradient-mesh" />
        <div className="absolute inset-0 bg-grid-pattern opacity-40" />
        {/* Animated orbs */}
        <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-cyan-500/[0.07] rounded-full blur-[120px] animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-indigo-500/[0.06] rounded-full blur-[100px] animate-float" style={{ animationDelay: '2s' }} />
        <div className="absolute top-1/2 left-1/2 w-[300px] h-[300px] bg-emerald-500/[0.05] rounded-full blur-[80px] animate-float" style={{ animationDelay: '4s' }} />
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center px-6 max-w-5xl mx-auto text-center">
        {/* Status badge */}
        <div className="animate-slide-in delay-1 inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 mb-8">
          <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse-slow" />
          <span className="text-xs font-medium text-cyan-300 tracking-wide uppercase">
            World Cup 2026 • Live Operations
          </span>
        </div>

        {/* Main heading */}
        <h1 className="animate-slide-in delay-2 text-6xl sm:text-7xl md:text-8xl font-black tracking-tight mb-4">
          <span className="bg-gradient-to-r from-white via-white to-gray-400 bg-clip-text text-transparent">
            Stadium
          </span>
          <span className="bg-gradient-to-r from-cyan-300 to-cyan-500 bg-clip-text text-transparent">
            OS
          </span>
          <span className="text-gray-500 font-light ml-3">AI</span>
        </h1>

        {/* Subtitle */}
        <p className="animate-slide-in delay-3 text-xl sm:text-2xl text-gray-400 font-light mb-3 max-w-2xl">
          AI Operating System for{" "}
          <span className="text-white font-medium">FIFA World Cup 2026</span>
        </p>
        <p className="animate-slide-in delay-4 text-sm text-gray-500 mb-12 max-w-lg">
          Multi-agent AI orchestrating navigation, operations, and accessibility
          for 80,000+ fans across 16 host stadiums.
        </p>

        {/* CTA */}
        <Link
          href="/dashboard"
          className="animate-slide-in delay-5 group relative inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-cyan-500 to-cyan-600 text-white font-semibold rounded-2xl shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 transition-all duration-300 hover:scale-[1.03] active:scale-[0.98]"
        >
          Enter Command Center
          <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </Link>

        {/* Agent cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 mt-16 w-full max-w-4xl">
          {agents.map((agent, i) => (
            <div
              key={agent.name}
              className={`animate-slide-in delay-${i + 6} glass-card p-6 text-left hover:scale-[1.02] transition-transform duration-300`}
            >
              <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${agent.color} flex items-center justify-center text-white text-lg font-bold mb-4 shadow-lg ${agent.glow}`}>
                {agent.icon}
              </div>
              <h3 className="text-white font-semibold mb-2">{agent.name}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{agent.desc}</p>
            </div>
          ))}
        </div>

        {/* Bottom tag */}
        <p className="animate-fade-in mt-16 text-xs text-gray-600">
          PromptWars Virtual Challenge 4 • Built for the future of stadium operations
        </p>
      </div>
    </div>
  );
}
