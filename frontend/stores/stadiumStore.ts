import { create } from "zustand";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
async function getStadium(): Promise<any> {
  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${API_BASE}/api/stadium`);
  return res.json();
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
async function getGraph(): Promise<any> {
  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${API_BASE}/api/graph`);
  return res.json();
}

export interface GraphNode {
  id: string;
  type: string;
  name: string;
  position: { x: number; y: number; z: number };
  level: number;
  quadrant: string;
  accessible: boolean;
}

export interface GraphEdge {
  start_id: string;
  end_id: string;
  distance_m: number;
  travel_time_s: number;
  accessible: boolean;
}

export interface RouteStepInfo {
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

export interface RouteResult {
  route_id: string;
  steps: RouteStepInfo[];
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

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Json = any;

interface RouteState {
  routeResult: RouteResult | null;
  routePoints: [number, number, number][];
  routeLoading: boolean;
  routeError: string | null;
  navigateTo: (startId: string, destId: string) => Promise<void>;
  clearRoute: () => void;
}

interface StadiumState {
  config: Json | null;
  graphNodes: GraphNode[];
  graphEdges: GraphEdge[];
  totalSeats: number;
  loading: boolean;
  error: string | null;
  fetchStadium: () => Promise<void>;
  route: RouteState;
}

function buildRoutePoints(path: string[], nodes: GraphNode[]): [number, number, number][] {
  const nodeMap = new Map(nodes.map((n) => [n.id, n]));
  return path
    .map((id) => nodeMap.get(id))
    .filter((n): n is GraphNode => n !== undefined)
    .map((n) => [n.position.x, n.position.y + 0.5, n.position.z] as [number, number, number]);
}

const initialRouteState: RouteState = {
  routeResult: null,
  routePoints: [],
  routeLoading: false,
  routeError: null,
  navigateTo: async () => {},
  clearRoute: () => {},
};

export const useStadiumStore = create<StadiumState>((set, get) => ({
  config: null,
  graphNodes: [],
  graphEdges: [],
  totalSeats: 0,
  loading: false,
  error: null,

  fetchStadium: async () => {
    set({ loading: true, error: null });
    try {
      const [stadiumRes, graphRes] = await Promise.all([
        getStadium(),
        getGraph(),
      ]);
      set({
        config: stadiumRes.config,
        graphNodes: graphRes.nodes,
        graphEdges: graphRes.edges,
        totalSeats: stadiumRes.seats,
        loading: false,
      });
    } catch (e) {
      set({ error: (e as Error).message, loading: false });
    }
  },

  route: {
    ...initialRouteState,
    navigateTo: async (startId: string, destId: string) => {
      const state = get();
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      set((s) => ({ route: { ...s.route, routeLoading: true, routeError: null } }));
      try {
        const res = await fetch(`${API_BASE}/api/navigation/route`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ start_location: startId, destination: destId }),
        });
        if (!res.ok) throw new Error(`Route API error: ${res.status}`);
        const data: RouteResult = await res.json();
        const points = data.path.length > 0
          ? buildRoutePoints(data.path, state.graphNodes)
          : [];
        set((s) => ({
          route: {
            ...s.route,
            routeResult: data,
            routePoints: points,
            routeLoading: false,
          },
        }));
      } catch (e) {
        set((s) => ({
          route: {
            ...s.route,
            routeError: (e as Error).message,
            routeLoading: false,
          },
        }));
      }
    },
    clearRoute: () => {
      set((s) => ({
        route: { ...s.route, routeResult: null, routePoints: [], routeError: null },
      }));
    },
  },
}));
