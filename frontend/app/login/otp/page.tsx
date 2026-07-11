"use client";

import { Suspense, useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import OTPInput from "@/features/auth/OTPInput";
import { requestOTP, verifyOTP } from "@/lib/api";
import { useAuthStore } from "@/stores/authStore";

export default function OTPPageWrapper() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#0a0e1a] flex items-center justify-center text-white/50">Loading...</div>}>
      <OTPPage />
    </Suspense>
  );
}

function OTPPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const login = useAuthStore((s) => s.login);

  const identifier = searchParams.get("identifier") || "";
  const role = searchParams.get("role") || "fan";

  const [status, setStatus] = useState<"sending" | "sent" | "verifying" | "error">("sending");
  const [error, setError] = useState("");
  const [otpSent, setOtpSent] = useState(false);

  useEffect(() => {
    if (!identifier) {
      router.push("/login");
      return;
    }
    // Request OTP on mount
    requestOTP(identifier)
      .then(() => {
        setStatus("sent");
        setOtpSent(true);
      })
      .catch((err) => {
        setStatus("error");
        setError(err.message);
      });
  }, [identifier, router]);

  const handleOTPComplete = async (otp: string) => {
    setStatus("verifying");
    setError("");
    try {
      const result = await verifyOTP(identifier, otp);
      login(result.token, result.user_id, result.name, result.role as "fan" | "volunteer" | "operations", result.expires_at);

      // Role-based redirect
      if (result.role === "fan") {
        router.push("/");
      } else if (result.role === "volunteer") {
        router.push("/dashboard");
      } else if (result.role === "operations") {
        router.push("/dashboard");
      } else {
        router.push("/");
      }
    } catch (err: unknown) {
      setStatus("sent");
      setError(err instanceof Error ? err.message : "Invalid OTP. Try 123456.");
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0e1a] flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-white tracking-tight">Verify Your Code</h1>
          <p className="text-white/40 text-sm mt-2">
            A 6-digit code was sent to{" "}
            <span className="text-white/60 font-mono">{identifier}</span>
          </p>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
          {status === "sending" && (
            <div className="text-center text-white/50 py-6">Sending verification code...</div>
          )}

          {status === "sent" && (
            <div className="space-y-6">
              <OTPInput length={6} onComplete={handleOTPComplete} />

              {!otpSent && (
                <div className="text-center">
                  <button
                    onClick={() => {
                      setStatus("sending");
                      requestOTP(identifier)
                        .then(() => setStatus("sent"))
                        .catch((err) => { setStatus("error"); setError(err.message); });
                    }}
                    className="text-sm text-cyan-400/70 hover:text-cyan-400 transition-colors"
                  >
                    Resend code
                  </button>
                </div>
              )}

              {error && (
                <div className="text-center text-sm text-red-400 bg-red-400/10 border border-red-400/20 rounded-lg p-3">
                  {error}
                </div>
              )}

              <p className="text-center text-white/20 text-xs">
                Demo code: <span className="font-mono">123456</span>
              </p>
            </div>
          )}

          {status === "verifying" && (
            <div className="text-center text-white/50 py-6">Verifying code...</div>
          )}

          {status === "error" && (
            <div className="text-center">
              <div className="text-red-400 text-sm mb-4">{error}</div>
              <button
                onClick={() => { setStatus("sent"); setError(""); }}
                className="text-sm text-cyan-400/70 hover:text-cyan-400 transition-colors"
              >
                Try again
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
