import { useCallback, useEffect, useMemo, useState } from "react";

interface Position2D {
  x: number;
  y: number;
}

interface Vector2D {
  from: Position2D;
  to: Position2D;
  dx: number;
  dy: number;
  dt: number;
  theta: number;
  ctheta: number;
}

interface Cursor {
  vec: Vector2D;
  target: Element | null;
}

function debouncify(fn: Function, dur: number) {
  let timeout: number | NodeJS.Timeout | null = null;

  return (...args: any[]) => {
    if (timeout) {
      return;
    }

    timeout = setTimeout(() => {
      fn(...args);
      timeout = null;
    }, dur);
  };
}

function rtoc(r: number): number {
  return (57.29577951308232 * r + 360) % 360;
}

function rtoa(r: number): number {
  return 57.29577951308232 * r;
}

function useCursorHandler(
  setVec: React.Dispatch<React.SetStateAction<Vector2D>>,
  setCursorTarget: React.Dispatch<React.SetStateAction<HTMLElement | null>>,
  debounce: number = 20
) {
  let cb = (ev: MouseEvent) => {
    const x = ev.clientX;
    const y = ev.clientY;

    setVec((prev) => {
      const from = prev.to;

      const dx = x - from.x;
      const dy = y - from.y;

      if (dx === 0 && dy === 0) {
        return prev; // no movement
      }

      const cx = x - window.innerWidth / 2;
      const cy = y - window.innerHeight / 2;
      const dt = Math.hypot(dx, dy);
      const ctheta = rtoa(Math.atan2(cy, cx));
      const theta = rtoa(Math.atan2(dy, dx));

      return {
        from,
        to: { x, y },
        dx,
        dy,
        dt,
        theta,
        ctheta,
      };
    });

    setCursorTarget(ev.target as HTMLElement);
  };
  if (debounce) {
    cb = debouncify(cb, debounce);
  }

  const memoized = useCallback(cb, [debounce]);
  return memoized;
}

type BoundTargetWithoutRef = Window | HTMLElement | null;
type BoundTarget =
  | BoundTargetWithoutRef
  | React.RefObject<BoundTargetWithoutRef>;
function useCursor(
  bound: BoundTarget = typeof window !== "undefined" ? window : null,
  debounce: number = 0
): Cursor {
  console.log(bound);
  const [vec, setVec] = useState<Vector2D>({
    from: { x: 0, y: 0 },
    to: { x: 0, y: 0 },
    dx: 0,
    dy: 0,
    dt: 0,
    theta: 0,
    ctheta: 0,
  });

  const [cursorTarget, setCursorTarget] = useState<HTMLElement | null>(null);

  const handleMouse = useCursorHandler(setVec, setCursorTarget, debounce);

  useEffect(() => {
    // resolve bound dynamically
    const target = bound && "current" in bound ? bound.current : bound;

    if (!target) return; // still null → skip until next render

    const controller = new AbortController();
    const { signal } = controller;

    (target as Window).addEventListener("mousemove", handleMouse, { signal });
    (target as Window).addEventListener("click", handleMouse, { signal });

    return () => controller.abort();
  }, [bound, handleMouse]);

  return { vec, target: cursorTarget };
}

export default useCursor;
export type { BoundTarget };
