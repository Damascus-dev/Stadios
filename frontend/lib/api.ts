export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface AgentQuery {
  query: string;
  agent_type: string;
  context?: Record<string, unknown>;
  language?: string;
}

export interface AgentResponse {
  agent_type: string;
  response_text: string;
  structured_data?: Record<string, unknown>;
  recommendations: string[];
  confidence: number;
  cached: boolean;
}

export interface StadiumHealth {
  overall_score: number;
  status: string;
  capacity_pct: number;
  active_zones: number;
}

export interface CrowdZone {
  zone_id: string;
  name: string;
  density_pct: number;
  trend: string;
  risk_level: string;
}

export interface VolunteerAssignment {
  zone_id: string;
  zone_name: string;
  count: number;
  role: string;
}

export interface VolunteerStatus {
  total: number;
  deployed: number;
  available: number;
  zones: VolunteerAssignment[];
}

export interface SeverityBreakdown {
  critical: number;
  high: number;
  medium: number;
  low: number;
}

export interface IncidentCount {
  active: number;
  resolved: number;
  total: number;
  by_severity: SeverityBreakdown;
}

export interface AlertItem {
  id: string;
  type: string;
  severity: string;
  title?: string;
  message: string;
  zone: string;
  timestamp: string;
  acknowledged?: boolean;
  recommended_action?: string;
}

export interface AIRecommendation {
  id: string;
  type: string;
  priority: string;
  title: string;
  description: string;
  agent_source: string;
  confidence: number;
}

export interface ExitCongestion {
  exit_id: string;
  name: string;
  congestion_pct: number;
}

export interface TransportationStatus {
  shuttle_load_pct: number;
  parking_capacity_pct: number;
  exit_congestion: ExitCongestion[];
  prediction: string;
}

export interface SustainabilityMetrics {
  energy_load_kwh: number;
  waste_generation_kg: number;
  water_usage_liters: number;
  crowd_correlation_factor: number;
}

export interface DashboardData {
  stadium_health: StadiumHealth;
  crowd_heat: { zones: CrowdZone[] };
  volunteer_status: VolunteerStatus;
  incident_count: IncidentCount;
  active_alerts: { alerts: AlertItem[] };
  ai_recommendations: AIRecommendation[];
  transportation: TransportationStatus;
  sustainability: SustainabilityMetrics;
  generated_at: string;
}

export interface RouteStep {
  instruction: string;
  distance_m: number;
  duration_s: number;
  congestion_level: string;
}

export interface RouteAlternative {
  description: string;
  reason: string;
  tradeoff: string;
  total_distance_m: number;
  total_duration_s: number;
  confidence: number;
}

export interface NavigationResponse {
  route_id: string;
  steps: RouteStep[];
  total_distance_m: number;
  total_duration_s: number;
  eta: string;
  congestion_aware: boolean;
  accessibility_adapted: boolean;
  alternative_available: boolean;
  path: string[];
  reason: string;
  benefit: string;
  tradeoff: string;
  confidence: number;
  alternatives: RouteAlternative[];
}

export interface StadiumZone {
  zone_id: string;
  name: string;
  type: string;
  level: number;
  accessible: boolean;
}

// ── Auth Types ──────────────────────────────────────────────────────
export interface OTPRequest {
  identifier: string;
}

export interface OTPResponse {
  message: string;
  identifier: string;
  expires_in_seconds: number;
}

export interface TokenData {
  token: string;
  user_id: string;
  name: string;
  role: string;
  expires_at: string;
}

export interface UserProfile {
  user_id: string;
  name: string;
  role: string;
  phone?: string;
}

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  const token = typeof window !== "undefined" ? localStorage.getItem("auth_token") : null;
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(url, { headers, ...options });
  if (!res.ok) {
    const detail = await res.json().then((d) => d.detail).catch(() => res.statusText);
    throw new Error(`API error: ${res.status} ${detail}`);
  }
  return res.json();
}

// ── Auth API ────────────────────────────────────────────────────────
export async function requestOTP(identifier: string): Promise<OTPResponse> {
  return fetchJSON<OTPResponse>(`${API_BASE}/api/auth/request-otp`, {
    method: "POST",
    body: JSON.stringify({ identifier } satisfies OTPRequest),
  });
}

export async function verifyOTP(identifier: string, otp: string): Promise<TokenData> {
  return fetchJSON<TokenData>(`${API_BASE}/api/auth/verify-otp`, {
    method: "POST",
    body: JSON.stringify({ identifier, otp }),
  });
}

export async function getMe(): Promise<UserProfile> {
  return fetchJSON<UserProfile>(`${API_BASE}/api/auth/me`);
}

export async function getDashboard(): Promise<DashboardData> {
  const data = await fetchJSON<{ dashboard: DashboardData }>(`${API_BASE}/api/dashboard/`);
  return data.dashboard;
}

export async function getNavigationRoute(
  from: string,
  to: string,
  accessibility?: string
): Promise<NavigationResponse> {
  return fetchJSON<NavigationResponse>(`${API_BASE}/api/navigation/route`, {
    method: "POST",
    body: JSON.stringify({
      start_location: from,
      destination: to,
      accessibility_preference: accessibility || null,
      language: "en",
    }),
  });
}

export async function getZones(): Promise<StadiumZone[]> {
  return fetchJSON<StadiumZone[]>(`${API_BASE}/api/navigation/zones`);
}

export async function getAlerts(): Promise<AlertItem[]> {
  const data = await fetchJSON<{ alerts: AlertItem[] }>(`${API_BASE}/api/alerts/`);
  return data.alerts;
}

export async function acknowledgeAlert(id: string): Promise<void> {
  await fetchJSON(`${API_BASE}/api/alerts/${id}/acknowledge`, { method: "POST" });
}

export async function queryAgent(agentType: string, query: string): Promise<AgentResponse> {
  return fetchJSON<AgentResponse>(`${API_BASE}/api/agents/${agentType}`, {
    method: "POST",
    body: JSON.stringify({ query, agent_type: agentType } satisfies AgentQuery),
  });
}

export async function getStadium(): Promise<Record<string, unknown>> {
  return fetchJSON(`${API_BASE}/api/stadium`);
}

export async function getGraph(): Promise<{ nodes: unknown[]; edges: unknown[] }> {
  return fetchJSON(`${API_BASE}/api/graph`);
}

export async function getFacilities(type: string): Promise<Record<string, unknown>> {
  return fetchJSON(`${API_BASE}/api/facilities/${type}`);
}

export async function detectIntent(query: string): Promise<string> {
  const data = await fetchJSON<{ agent_type: string }>(`${API_BASE}/api/agents/detect-intent`, {
    method: "POST",
    body: JSON.stringify({ query }),
  });
  return data.agent_type;
}
