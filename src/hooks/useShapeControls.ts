import { useState } from "react";

export const useShapeControls = () => {
  const [shapeProps, setShapeProps] = useState({
    size: 1,
    color: "#ff0000"
  });

  const updateShape = (key: keyof typeof shapeProps, value: any) => {
    setShapeProps((prev) => ({ ...prev, [key]: value }));
  };

  return { shapeProps, updateShape };
};