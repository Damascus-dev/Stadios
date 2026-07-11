"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: string[];
}

export default function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const router = useRouter();
  const { isAuthenticated, role, isExpired, logout } = useAuthStore();

  useEffect(() => {
    if (!isAuthenticated || isExpired()) {
      if (isExpired()) logout();
      router.push("/login");
      return;
    }

    if (requiredRole && role && !requiredRole.includes(role)) {
      router.push("/login");
      return;
    }
  }, [isAuthenticated, role, isExpired, logout, router, requiredRole]);

  if (!isAuthenticated || isExpired()) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#0a0e1a]">
        <div className="animate-pulse text-white/30">Redirecting to login...</div>
      </div>
    );
  }

  if (requiredRole && role && !requiredRole.includes(role)) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#0a0e1a]">
        <div className="text-amber-400/70">Access denied. Required role: {requiredRole.join(", ")}</div>
      </div>
    );
  }

  return <>{children}</>;
}
