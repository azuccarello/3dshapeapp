import { ShapeSettings } from "./ShapeSettings";

export default function ControlsPanel() {
  return (
    <div style={{ position: "absolute", top: 0, right: 0, width: 320, padding: 16, backgroundColor: "rgba(0,0,0,0.8)", color: "white" }}>
      <ShapeSettings />
    </div>
  );
}