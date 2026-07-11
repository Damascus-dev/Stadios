"use client";

import { useEffect, useRef, useCallback } from "react";
import { Canvas, useThree, useFrame } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import { useStadiumStore, GraphNode } from "@/stores/stadiumStore";

interface Props {
  selectedId?: string | null;
  targetPosition?: [number, number, number] | null;
  onNodeClick?: (node: GraphNode) => void;
}

function StadiumRing({ level, elevation, innerR, outerR }: { level: number; elevation: number; innerR: number; outerR: number }) {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, elevation, 0]} receiveShadow>
      <ringGeometry args={[innerR, outerR, 64]} />
      <meshStandardMaterial color={level === 0 ? 0x1a1a2e : 0x16213e} side={THREE.DoubleSide} metalness={0.3} roughness={0.7} />
    </mesh>
  );
}

function SeatMarkers({ count = 3000 }: { count?: number }) {
  const ref = useRef<THREE.InstancedMesh>(null);
  const config = useStadiumStore((s) => s.config);
  const totalSeats = config?.total_seats ?? 57600;
  const levels = 4;
  const sectionsPer = config?.sections_per_level ?? 12;
  const rowsPer = config?.rows_per_section ?? 30;

  useEffect(() => {
    if (!ref.current) return;
    const dummy = new THREE.Object3D();
    const perLevel = Math.floor(count / levels);
    const perSection = Math.floor(perLevel / sectionsPer);
    let idx = 0;
    for (let lvl = 0; lvl < levels && idx < count; lvl++) {
      const elev = lvl * 8 + 0.3;
      for (let s = 0; s < sectionsPer && idx < count; s++) {
        const angle = s * (2 * Math.PI / sectionsPer);
        for (let r = 0; r < perSection && idx < count; r += 3) {
          const radius = 45 + r * 1.2;
          const seatAngle = angle + (r / perSection) * (2 * Math.PI / sectionsPer / 6);
          dummy.position.set(radius * Math.cos(seatAngle), elev, radius * Math.sin(seatAngle));
          dummy.updateMatrix();
          ref.current.setMatrixAt(idx, dummy.matrix);
          idx++;
        }
      }
    }
    ref.current.count = idx;
    ref.current.instanceMatrix.needsUpdate = true;
  }, [count, levels, sectionsPer, rowsPer, totalSeats]);

  return (
    <instancedMesh ref={ref} args={[undefined, undefined, count]} castShadow>
      <boxGeometry args={[0.35, 0.25, 0.35]} />
      <meshStandardMaterial color={0x0ea5e9} metalness={0.15} roughness={0.85} />
    </instancedMesh>
  );
}

const typeColors: Record<string, string> = {
  food: "#f97316",
  restroom: "#06b6d4",
  medical: "#ef4444",
  charging: "#fbbf24",
  prayer: "#a855f7",
  merchandise: "#22c55e",
  volunteer: "#8b5cf6",
};

function FacilityMarker({ node, isSelected, onClick }: { node: GraphNode; isSelected: boolean; onClick: () => void }) {
  const ref = useRef<THREE.Mesh>(null);
  const color = typeColors[node.type] || "#fbbf24";

  useFrame((_, delta) => {
    if (ref.current && isSelected) {
      ref.current.scale.setScalar(1 + 0.15 * Math.sin(performance.now() / 300));
    }
  });

  return (
    <mesh
      ref={ref}
      position={[node.position.x, node.position.y + 0.8, node.position.z]}
      onClick={(e) => { e.stopPropagation(); onClick(); }}
      onPointerOver={(e) => { e.stopPropagation(); document.body.style.cursor = "pointer"; }}
      onPointerOut={() => { document.body.style.cursor = "default"; }}
    >
      <sphereGeometry args={[isSelected ? 0.5 : 0.3, 12, 12]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={isSelected ? 0.8 : 0.3}
      />
    </mesh>
  );
}

function FacilityMarkers({ selectedId, onNodeClick }: { selectedId?: string | null; onNodeClick?: (node: GraphNode) => void }) {
  const nodes = useStadiumStore((s) => s.graphNodes);
  const facilities = nodes.filter((n) =>
    ["food", "restroom", "medical", "charging", "prayer", "merchandise", "volunteer"].includes(n.type)
  );

  return (
    <>
      {facilities.map((f) => (
        <FacilityMarker
          key={f.id}
          node={f}
          isSelected={f.id === selectedId}
          onClick={() => onNodeClick?.(f)}
        />
      ))}
    </>
  );
}

function RoutePath() {
  const routePoints = useStadiumStore((s) => s.route.routePoints);
  const ref = useRef<THREE.Mesh>(null);
  const geomRef = useRef<THREE.TubeGeometry | null>(null);

  useEffect(() => {
    if (routePoints.length < 2) {
      if (geomRef.current) { geomRef.current.dispose(); geomRef.current = null; }
      if (ref.current) ref.current.geometry = new THREE.BufferGeometry();
      return;
    }
    const curve = new THREE.CatmullRomCurve3(
      routePoints.map((p) => new THREE.Vector3(p[0], p[1], p[2]))
    );
    if (geomRef.current) geomRef.current.dispose();
    geomRef.current = new THREE.TubeGeometry(curve, 64, 0.5, 8, false);
    if (ref.current) ref.current.geometry = geomRef.current;
  }, [routePoints]);

  if (routePoints.length < 2) return null;

  return (
    <mesh ref={ref}>
      <meshStandardMaterial color={0x22d3ee} emissive={0x22d3ee} emissiveIntensity={0.5} transparent opacity={0.7} />
    </mesh>
  );
}

function CameraController({ target }: { target: [number, number, number] | null }) {
  const { camera } = useThree();
  const controlsRef = useRef<any>(null);
  const prevTarget = useRef<[number, number, number] | null>(null);

  useEffect(() => {
    if (!target || !controlsRef.current) return;
    if (prevTarget.current && prevTarget.current[0] === target[0] && prevTarget.current[1] === target[1] && prevTarget.current[2] === target[2]) return;
    prevTarget.current = target;
    controlsRef.current?.setAzimuthalAngle(0);
    controlsRef.current?.setPolarAngle(Math.PI / 3);
  }, [target]);

  return <OrbitControls
    ref={controlsRef}
    enablePan
    enableZoom
    enableRotate
    maxPolarAngle={Math.PI / 2.2}
    minDistance={20}
    maxDistance={200}
  />;
}

export function StadiumCanvas({ selectedId, targetPosition, onNodeClick }: Props) {
  const { fetchStadium, loading, error } = useStadiumStore();

  useEffect(() => {
    fetchStadium();
  }, [fetchStadium]);

  if (loading) {
    return <div className="w-full h-full flex items-center justify-center text-white/40">Loading stadium...</div>;
  }

  if (error) {
    return <div className="w-full h-full flex items-center justify-center text-red-400">{error}</div>;
  }

  return (
    <Canvas
      camera={{ position: [0, 50, 120], fov: 50, near: 1, far: 500 }}
      shadows
      dpr={[1, 1.5]}
      gl={{ antialias: true, alpha: false }}
      onCreated={({ gl }) => gl.setClearColor(0x0a0e1a)}
    >
      <ambientLight intensity={0.4} />
      <directionalLight position={[50, 80, 50]} intensity={1.2} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024} />
      <hemisphereLight args={[0x443333, 0x111122, 0.6]} />

      {[0, 1, 2, 3].map((lvl, i) => (
        <StadiumRing key={lvl} level={lvl} elevation={i * 8} innerR={40 + i * 5} outerR={80 + i * 3} />
      ))}

      <SeatMarkers count={3000} />
      <FacilityMarkers selectedId={selectedId} onNodeClick={onNodeClick} />
      <RoutePath />

      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]} receiveShadow>
        <planeGeometry args={[68, 105]} />
        <meshStandardMaterial color={0x1b4332} />
      </mesh>

      <CameraController target={targetPosition ?? null} />
    </Canvas>
  );
}
