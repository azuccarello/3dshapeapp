import ShapeCanvas from "../components/ShapeCanvas";
import ControlsPanel from "../components/ControlsPanel";

export default function Home() {
  return (
    <div className="bg-black min-h-screen text-white">
      <ShapeCanvas />
      <ControlsPanel />
    </div>
  );
}