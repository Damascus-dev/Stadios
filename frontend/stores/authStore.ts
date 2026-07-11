import { create } from "zustand";
import { persist } from "zustand/middleware";

export type UserRole = "fan" | "volunteer" | "operations" | null;

interface AuthState {
  token: string | null;
  userId: string | null;
  name: string | null;
  role: UserRole;
  expiresAt: string | null;
  isAuthenticated: boolean;

  login: (token: string, userId: string, name: string, role: UserRole, expiresAt: string) => void;
  logout: () => void;
  isExpired: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      userId: null,
      name: null,
      role: null,
      expiresAt: null,
      isAuthenticated: false,

      login: (token, userId, name, role, expiresAt) => {
        localStorage.setItem("auth_token", token);
        set({ token, userId, name, role, expiresAt, isAuthenticated: true });
      },

      logout: () => {
        localStorage.removeItem("auth_token");
        set({ token: null, userId: null, name: null, role: null, expiresAt: null, isAuthenticated: false });
      },

      isExpired: () => {
        const { expiresAt } = get();
        if (!expiresAt) return true;
        return new Date(expiresAt).getTime() < Date.now();
      },
    }),
    {
      name: "stadiumos-auth",
      partialize: (state) => ({
        token: state.token,
        userId: state.userId,
        name: state.name,
        role: state.role,
        expiresAt: state.expiresAt,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
