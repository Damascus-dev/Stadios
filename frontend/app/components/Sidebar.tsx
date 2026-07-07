'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: '◫' },
  { href: '/navigation', label: 'Navigation', icon: '◎' },
  { href: '/chat', label: 'Chat', icon: '◬' },
  { href: '/alerts', label: 'Alerts', icon: '⚠' },
];

export default function Sidebar() {
  const pathname = usePathname();

  // Don't show sidebar on landing page
  if (pathname === '/') return null;

  return (
    <aside className="group fixed left-0 top-0 z-50 h-screen w-[68px] hover:w-[220px] transition-all duration-300 ease-in-out flex flex-col glass-panel border-r border-white/[0.06]">
      {/* Logo */}
      <Link href="/" className="flex items-center gap-3 px-4 py-5 border-b border-white/[0.06]">
        <div className="relative flex-shrink-0 w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-400 to-cyan-600 flex items-center justify-center font-bold text-white text-lg shadow-lg shadow-cyan-500/30">
          S
          <div className="absolute inset-0 rounded-xl animate-ring-pulse" />
        </div>
        <span className="text-sm font-bold text-white whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 tracking-wide">
          StadiumOS
        </span>
      </Link>

      {/* Nav Items */}
      <nav className="flex-1 flex flex-col gap-1 px-3 py-4">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`
                relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium
                transition-all duration-200
                ${isActive
                  ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/20'
                  : 'text-gray-400 hover:text-white hover:bg-white/[0.04] border border-transparent'
                }
              `}
            >
              {isActive && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-[14px] w-[3px] h-5 bg-cyan-400 rounded-r-full" />
              )}
              <span className="flex-shrink-0 text-lg w-5 text-center">{item.icon}</span>
              <span className="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                {item.label}
              </span>
            </Link>
          );
        })}
      </nav>

      {/* Bottom status */}
      <div className="px-4 py-4 border-t border-white/[0.06]">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse-slow flex-shrink-0" />
          <span className="text-[11px] text-gray-500 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            All Systems Online
          </span>
        </div>
      </div>
    </aside>
  );
}
