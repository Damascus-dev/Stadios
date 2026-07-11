"use client";

import { useEffect, useRef } from "react";
import { useStadiumStore } from "@/stores/stadiumStore";

const POLL_INTERVAL_MS = 30_000;

export function useAutoReroute() {
  const routeResult = useStadiumStore((s) => s.route.routeResult);
  const graphNodes = useStadiumStore((s) => s.graphNodes);
  const navigateTo = useStadiumStore((s) => s.route.navigateTo);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (!routeResult || routeResult.steps.length === 0) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      return;
    }

    if (intervalRef.current) return;

    intervalRef.current = setInterval(() => {
      if (routeResult.steps.length > 0 && graphNodes.length > 0) {
        const first = routeResult.steps[0];
        const last = routeResult.steps[routeResult.steps.length - 1];
        const startMatch = first.instruction.match(/from (\S+)/);
        const endMatch = last.instruction.match(/to (\S+)/);
        if (startMatch && endMatch) {
          const startId = graphNodes.find((n) => n.name === startMatch[1])?.id;
          const endId = graphNodes.find((n) => n.name === endMatch[1])?.id;
          if (startId && endId) {
            navigateTo(startId, endId);
          }
        }
      }
    }, POLL_INTERVAL_MS);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [routeResult, graphNodes, navigateTo]);
}
