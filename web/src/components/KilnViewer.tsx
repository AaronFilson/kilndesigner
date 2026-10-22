// The kiln's 3D model: the glTF the engine built (ADR 0005), framed to fit, with orbit controls.
import { Bounds, OrbitControls, useGLTF } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";

function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url);
  return <primitive object={scene} />;
}

export function KilnViewer({ url }: { url: string }) {
  return (
    <div className="viewer" aria-label="3D model of the kiln">
      <Canvas camera={{ position: [3, 2, 3], fov: 40, near: 0.01, far: 1e6 }}>
        <hemisphereLight args={["#ffffff", "#666666", 1.2]} />
        <directionalLight position={[5, 10, 7]} intensity={1.5} />
        <Suspense fallback={null}>
          <Bounds fit clip observe margin={1.2}>
            <Model url={url} />
          </Bounds>
        </Suspense>
        <OrbitControls makeDefault />
      </Canvas>
    </div>
  );
}
