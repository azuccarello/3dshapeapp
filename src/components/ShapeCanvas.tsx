import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { Shape } from "./ShapeSettings";

export default function ShapeCanvas() {
  return (
    <Canvas camera={{ position: [0, 0, 5] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      <Shape />
      <OrbitControls enableZoom={true} />
    </Canvas>
  );
}