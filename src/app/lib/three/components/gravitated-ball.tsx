import { useFrame } from "@react-three/fiber";
import { Sphere } from "@react-three/drei";
import { useRef } from "react";
import * as THREE from "three";

interface GravitatedBallProps extends React.ComponentProps<typeof Sphere> {
  gravity: number;
  bound: number;
  bounce: number;
}

function GravitatedBall({
  gravity,
  bound,
  bounce,
  ...props
}: GravitatedBallProps) {
  const ballRef = useRef<THREE.Mesh>(null);
  const velocity = useRef(0);

  useFrame((_, delta) => {
    if (!ballRef.current) return;
    const ball = ballRef.current;

    // accelerate downward
    velocity.current -= gravity * delta;
    ball.position.y += velocity.current * delta;

    // bounce on bound
    if (ball.position.y <= bound) {
      ball.position.y = bound;
      velocity.current *= -bounce; // reverse and dampen
    }
  });

  return <Sphere ref={ballRef} {...props} />;
}

export default GravitatedBall;
