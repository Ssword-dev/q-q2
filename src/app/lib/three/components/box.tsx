import React, { createContext, forwardRef, useContext, useRef } from 'react';
import * as THREE from 'three';
import '@react-three/fiber';
import { Html } from '@react-three/drei';
import { ator } from '../utils';

interface BoxProps {
  color?: React.ComponentProps<'meshBasicMaterial'>['color'];
  height: number;
  width: number;
  depth: number;
  x: number;
  y: number;
  z: number;
}

// stream the props.
const BoxContext = createContext<BoxProps | null>(null);

const useBox = () => {
  const context = useContext(BoxContext);

  if (!context) {
    throw new Error(
      '`useBox()` can only be used by descendants of a box primitive root.'
    );
  }

  return context;
};

const Root = forwardRef<THREE.Group, React.PropsWithChildren<BoxProps>>(
  function Root({ children, ...props }, ref) {
    return (
      <BoxContext.Provider value={props}>
        <group ref={ref} position={[props.x, props.y, props.z]}>
          {children}
        </group>
      </BoxContext.Provider>
    );
  }
);

interface BoxFaceProps {
  offset: {
    x: number;
    y: number;
    z: number;
  };
  rot: [number, number, number];
  dim: [number, number];
}

function Face(props: React.PropsWithChildren<BoxFaceProps>) {
  const cube = useBox();
  return (
    <mesh
      position={[props.offset.x, props.offset.y, props.offset.z]}
      rotation={props.rot}
    >
      <planeGeometry args={props.dim} />
      <meshBasicMaterial color={cube.color} side={THREE.DoubleSide} />
      <canvasTexture>{props.children}</canvasTexture>
      {/* {props.children && <Html center>{props.children}</Html>} */}
    </mesh>
  );
}

function createFaceComponent(
  factory: (box: BoxProps) => BoxFaceProps,
  name: string = 'Component'
) {
  const Component: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
    const box = useBox();
    const props = factory(box);
    return <Face {...props}>{children}</Face>;
  };

  Component.displayName = name;
  return Component;
}

const FrontFace = createFaceComponent(
  ({ depth, width, height }) => ({
    offset: {
      x: 0,
      y: 0,
      z: depth / 2,
    },
    rot: [0, 0, 0],
    dim: [width, height],
  }),
  'FrontFace'
);

const BackFace = createFaceComponent(
  ({ width, height, depth }) => ({
    offset: { x: 0, y: 0, z: (-1 * depth) / 2 },
    rot: [0, 0, 0],
    dim: [width, height],
  }),
  'BackFace'
);

const LeftFace = createFaceComponent(
  ({ width, height, depth }) => ({
    offset: { x: (-1 * width) / 2, y: 0, z: 0 },
    rot: [0, ator(90), 0],
    dim: [depth, height],
  }),
  'LeftFace'
);

const RightFace = createFaceComponent(
  ({ width, height, depth }) => ({
    offset: { x: width / 2, y: 0, z: 0 },
    rot: [0, ator(90), 0],
    dim: [depth, height],
  }),
  'RightFace'
);

const TopFace = createFaceComponent(
  ({ width, height, depth }) => ({
    offset: { x: 0, y: height / 2, z: 0 },
    rot: [ator(90), 0, 0],
    dim: [width, depth],
  }),
  'TopFace'
);

const BottomFace = createFaceComponent(
  ({ width, height, depth }) => ({
    offset: { x: 0, y: (-1 * height) / 2, z: 0 },
    rot: [ator(90), 0, 0],
    dim: [width, depth],
  }),
  'BottomFace'
);

export {
  Root,
  FrontFace,
  BackFace,
  TopFace,
  BottomFace,
  LeftFace,
  RightFace,
  useBox,
};
