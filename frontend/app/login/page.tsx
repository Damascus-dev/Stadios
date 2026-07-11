"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import RoleSelector from "@/features/auth/RoleSelector";

const ROLE_EMAIL: Record<string, string> = {
  fan: "fan@example.com",
  volunteer: "volunteer@example.com",
  operations: "ops@example.com",
};

export default function LoginPage() {
  const router = useRouter();
  const [selectedRole, setSelectedRole] = useState<string | null>(null);

  const handleRoleSelect = useCallback(
    (role: string) => {
      setSelectedRole(role);
      const email = ROLE_EMAIL[role] || `${role}@example.com`;
      router.push(`/login/otp?identifier=${encodeURIComponent(email)}&role=${role}`);
    },
    [router]
  );

  return (
    <div className="min-h-screen bg-[#0a0e1a] flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-white tracking-tight">StadiumOS Navigator</h1>
          <p className="text-white/40 text-sm mt-2">AI-Powered Stadium Navigation</p>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
          <RoleSelector selected={selectedRole} onSelect={handleRoleSelect} />
        </div>

        <p className="text-center text-white/20 text-xs mt-6">
          Demo mode &mdash; OTP <span className="font-mono">123456</span>
        </p>
      </div>
    </div>
  );
}
