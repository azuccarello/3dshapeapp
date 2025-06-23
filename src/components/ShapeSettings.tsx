import { useShapeControls } from "../hooks/useShapeControls";
import { useFrame } from "@react-three/fiber";
import { useRef } from "react";

function ShapeSettings() {
  const { shapeProps, updateShape } = useShapeControls();

  return (
    <div>
      <label>
        Size
        <input
          type="range"
          min="0.5"
          max="3"
          step="0.1"
          value={shapeProps.size}
          onChange={(e) => updateShape("size", parseFloat(e.target.value))}
        />
      </label>
      <br />
      <label>
        Color
        <input
          type="color"
          value={shapeProps.color}
          onChange={(e) => updateShape("color", e.target.value)}
        />
      </label>
    </div>
  );
}

function Shape() {
  const ref = useRef(null);
  const { shapeProps } = useShapeControls();

  useFrame(() => {
    if (ref.current) {
      ref.current.rotation.y += 0.01;
    }
  });

  return (
    <mesh ref={ref}>
      <boxGeometry args={[shapeProps.size, shapeProps.size, shapeProps.size]} />
      <meshStandardMaterial color={shapeProps.color} metalness={0.5} roughness={0.3} />
    </mesh>
  );
}

export { ShapeSettings, Shape };