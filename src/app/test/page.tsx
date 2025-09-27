import { Canvas, useFrame, useLoader } from "@react-three/fiber";
import {
  PerspectiveCamera,
  OrbitControls,
  Sphere,
  Text,
  Stars,
  Line,
} from "@react-three/drei";
import { Suspense, useRef } from "react";
import * as THREE from "three";
import { createRoot } from "react-dom/client";
import * as BoxPrimitive from "@/app/lib/three/components/box";
import GravitatedBall from "@/app/lib/three/components/gravitated-ball";

import "../tailwind.css";

function AxisLabels() {
  return (
    <group>
      {/* X axis (red) */}
      <mesh position={[2, 0, 0]}>
        <Text color="red" fontSize={0.5} anchorX="center" anchorY="middle">
          X
        </Text>
      </mesh>

      {/* Y axis (green) */}
      <mesh position={[0, 2, 0]}>
        <Text color="green" fontSize={0.5} anchorX="center" anchorY="middle">
          Y
        </Text>
      </mesh>

      {/* Z axis (blue) */}
      <mesh position={[0, 0, 2]}>
        <Text color="blue" fontSize={0.5} anchorX="center" anchorY="middle">
          Z
        </Text>
      </mesh>
    </group>
  );
}

interface HourglassProps {
  position: [number, number, number];
  height: number;
}
function Hourglass({ height, position: [x, y, z] }: HourglassProps) {
  return (
    <group position={[x - height / 2, y, z]}>
      <mesh>
        <coneGeometry args={[0.5, 2, 32]} />
        <meshPhysicalMaterial
          color="skyblue"
          transmission={0.9}
          roughness={0.1}
          thickness={0.2}
        />
      </mesh>
    </group>
  );
}

export default function Page() {
  return (
    <div className="w-screen h-screen">
      <Canvas>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
        <pointLight position={[-10, -10, -10]} />
        <PerspectiveCamera />
        <OrbitControls enableRotate />
        <Stars />
        <axesHelper args={[5]} />
        <group>
          <mesh>
            <Line
              points={[
                [0, 0, 0],
                [1, 1, 0],
                [-1, 2, 0],
                [0, 0, 0],
              ]}
            ></Line>
          </mesh>
        </group>
        <AxisLabels />
      </Canvas>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<Page />);
createRoot(document.getElementById("root")!).render(<Page />);
