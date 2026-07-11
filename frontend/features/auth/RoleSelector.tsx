"use client";

interface RoleOption {
  id: string;
  label: string;
  description: string;
  email: string;
}

const ROLES: RoleOption[] = [
  { id: "fan", label: "Fan", description: "Find your seat, facilities, and navigate the stadium", email: "fan@example.com" },
  { id: "volunteer", label: "Volunteer", description: "Assist fans, manage wayfinding, view assignments", email: "volunteer@example.com" },
  { id: "operations", label: "Operations", description: "Monitor crowd, alerts, and stadium systems", email: "ops@example.com" },
];

interface RoleSelectorProps {
  selected: string | null;
  onSelect: (role: string) => void;
}

export default function RoleSelector({ selected, onSelect }: RoleSelectorProps) {
  return (
    <div className="space-y-3">
      <h2 className="text-lg font-semibold text-white/90 text-center">Choose Your Role</h2>
      <p className="text-sm text-white/50 text-center mb-4">Select how you want to experience StadiumOS Navigator</p>
      {ROLES.map((role) => (
        <button
          key={role.id}
          onClick={() => onSelect(role.id)}
          className={`w-full text-left p-4 rounded-xl border transition-all ${
            selected === role.id
              ? "border-cyan-400 bg-cyan-400/10 shadow-[0_0_15px_rgba(34,211,238,0.15)]"
              : "border-white/10 bg-white/5 hover:bg-white/10 hover:border-white/20"
          }`}
        >
          <div className="font-medium text-white">{role.label}</div>
          <div className="text-sm text-white/50 mt-1">{role.description}</div>
          <div className="text-xs text-white/30 mt-1 font-mono">{role.email}</div>
        </button>
      ))}
    </div>
  );
}
