import * as BoxPrimitive from "@/app/lib/three/components/box";
import { forwardRef, PropsWithChildren } from "react";
import * as THREE from "three";

interface RubicsProps extends PropsWithChildren {
  width: number;
  height: number;
  depth: number;
}

const Rubics = forwardRef<THREE.Group, RubicsProps>(({ children }) => {
  const cubes = [
    [
      // top and bottom
      [0, 0],

      // left and right
      [0, 0],

      // front and back
      [0, 0],

      // x, y, z
      [0, 0, 0],

      // width, height, depth
      [0, 0, 0],
    ],
    [
      // top and bottom
      [0, 0],

      // left and right
      [0, 0],

      // front and back
      [0, 0],

      // x, y, z
      [0, 0, 0],

      // width, height, depth
      [0, 0, 0],
    ],
    [
      // top and bottom
      [0, 0],

      // left and right
      [0, 0],

      // front and back
      [0, 0],

      // x, y, z
      [0, 0, 0],

      // width, height, depth
      [0, 0, 0],
    ],
    [
      // top and bottom
      [0, 0],

      // left and right
      [0, 0],

      // front and back
      [0, 0],

      // x, y, z
      [0, 0, 0],

      // width, height, depth
      [0, 0, 0],
    ],
    [
      // top and bottom
      [0, 0],

      // left and right
      [0, 0],

      // front and back
      [0, 0],

      // x, y, z
      [0, 0, 0],

      // width, height, depth
      [0, 0, 0],
    ],
    [
      // top and bottom
      [0, 0],

      // left and right
      [0, 0],

      // front and back
      [0, 0],

      // x, y, z
      [0, 0, 0],

      // width, height, depth
      [0, 0, 0],
    ],
  ] as const;
  for (const color of []) return <group></group>;
});
