'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  {
    href: '/dashboard',
    label: 'Dashboard',
    icon: '◫',
    // SVG path for mobile bottom bar
    svgPath: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0h4',
    svgFilled: 'M10.707 2.293a1 1 0 00-1.414 0l-7 7A1 1 0 003 11h1v7a2 2 0 002 2h3a1 1 0 001-1v-4h4v4a1 1 0 001 1h3a2 2 0 002-2v-7h1a1 1 0 00.707-1.707l-7-7z',
  },
  {
    href: '/navigation',
    label: 'Navigate',
    icon: '◎',
    svgPath: 'M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7',
    svgFilled: 'M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7',
  },
  {
    href: '/chat',
    label: 'Chat',
    icon: '◬',
    svgPath: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
    svgFilled: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
  },
  {
    href: '/alerts',
    label: 'Alerts',
    icon: '⚠',
    svgPath: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
    svgFilled: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  // Don't show sidebar/bottom nav on landing page
  if (pathname === '/') return null;

  return (
    <>
      {/* ─── Desktop Sidebar (md and up) ─── */}
      <aside className="hidden md:flex group fixed left-0 top-0 z-50 h-screen w-[68px] hover:w-[220px] transition-all duration-300 ease-in-out flex-col glass-panel border-r border-white/[0.06]">
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

      {/* ─── Mobile Bottom Tab Bar (below md) ─── */}
      <nav className="flex md:hidden fixed bottom-0 left-0 right-0 z-50 h-[60px] glass-panel border-t border-white/[0.08] pb-safe">
        <div className="flex items-center justify-around w-full h-full px-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  flex flex-col items-center justify-center gap-0.5 flex-1 h-full min-w-[48px] py-1
                  transition-all duration-200 relative
                  ${isActive ? 'text-cyan-400' : 'text-gray-500'}
                `}
              >
                {/* Active indicator dot */}
                {isActive && (
                  <div className="absolute top-0 left-1/2 -translate-x-1/2 w-5 h-[2px] bg-cyan-400 rounded-full" />
                )}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={`w-6 h-6 transition-all duration-200 ${isActive ? 'scale-110' : ''}`}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={isActive ? 2.2 : 1.6}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d={item.svgPath} />
                </svg>
                <span className={`text-[10px] font-medium leading-none ${isActive ? 'text-cyan-400' : 'text-gray-500'}`}>
                  {item.label}
                </span>
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}
