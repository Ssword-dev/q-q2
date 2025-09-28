import { Canvas } from '@react-three/fiber';

const chineseZodiacs = [
  {
    name: 'Rat',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // nose
      [0.5, 0.6, 0], // ear
      [-0.5, 0, 0], // back
      [-1, -0.3, 0], // tail base
      [-2, -0.6, 0], // tail tip
    ],
  },
  {
    name: 'Ox',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // head
      [1.5, 0.6, 0], // horn up
      [1.5, -0.6, 0], // horn down
      [-1, 0.2, 0], // back
      [-1.5, -0.2, 0], // tail
    ],
  },
  {
    name: 'Tiger',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // head
      [1.4, 0.6, 0], // ear right
      [1.4, -0.6, 0], // ear left
      [-1, 0.4, 0], // back leg
      [-1, -0.4, 0], // back leg
      [0.4, 0.8, 0], // stripe
    ],
  },
  {
    name: 'Rabbit',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // head
      [1.2, 0.9, 0], // ear right
      [1.0, 1.3, 0], // ear tip
      [0.5, -0.5, 0], // foot
      [-0.8, 0, 0], // back
      [-1.2, 0.2, 0], // tail
    ],
  },
  {
    name: 'Dragon',
    points: [
      [0, 0, 0], // body
      [1, 0.2, 0], // head
      [1.3, 0.8, 0], // horn right
      [1.3, -0.8, 0], // horn left
      [0.5, 0.8, 0], // wing
      [-0.5, 0.4, 0], // body bend
      [-1, -0.2, 0], // tail
    ],
  },
  {
    name: 'Snake',
    points: [
      [0, 0, 0], // head
      [0.5, 0.5, 0], // curve
      [0, 1, 0], // curve
      [-0.5, 0.5, 0], // curve
      [-1, 0, 0], // body
      [-1.5, -0.5, 0], // tail
    ],
  },
  {
    name: 'Horse',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // head
      [1.4, 0.6, 0], // ear
      [0.5, 0.7, 0], // mane
      [-0.8, 0.3, 0], // back
      [-1.2, -0.2, 0], // tail
      [0.2, -0.6, 0], // leg
    ],
  },
  {
    name: 'Goat',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // head
      [1.3, 0.7, 0], // horn right
      [1.3, -0.7, 0], // horn left
      [-0.8, 0.2, 0], // back
      [-1.2, -0.3, 0], // tail
    ],
  },
  {
    name: 'Monkey',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // head
      [0.8, 0.6, 0], // ear right
      [0.8, -0.6, 0], // ear left
      [-0.5, 0.5, 0], // arm
      [-0.5, -0.5, 0], // arm
      [-1.2, -0.2, 0], // tail
    ],
  },
  {
    name: 'Rooster',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // head
      [1.2, 0.6, 0], // comb
      [1.1, -0.6, 0], // beak
      [-0.6, 0.5, 0], // wing
      [-1, -0.3, 0], // tail feather
      [-1.4, -0.6, 0], // tail feather tip
    ],
  },
  {
    name: 'Dog',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // head
      [1.3, 0.5, 0], // ear
      [0.5, 0.6, 0], // back
      [-0.6, 0.4, 0], // back leg
      [-1, -0.2, 0], // tail
    ],
  },
  {
    name: 'Pig',
    points: [
      [0, 0, 0], // body
      [1, 0, 0], // head
      [1.2, 0.5, 0], // ear
      [0.8, -0.5, 0], // snout
      [-0.6, 0.3, 0], // back
      [-1, -0.2, 0], // tail
    ],
  },
];

export default function CalendarBackground() {
  return (
    <>
      <div
        id="page-background"
        className="absolute h-screen w-screen [&>canvas]:h-screen [&>canvas]:w-screen -z-10"
      >
        <Canvas camera={{ position: [0, 0, 10], fov: 75 }}>
          <ambientLight intensity={0.5} />
          <directionalLight position={[5, 5, 5]} intensity={1} />
        </Canvas>
      </div>
    </>
  );
}
