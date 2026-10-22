// The kiln's 3D model: the glTF the engine built (ADR 0005), framed to fit, with orbit controls.
import { Bounds, OrbitControls } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { useQuery } from "@tanstack/react-query";
import { Component, type ReactNode } from "react";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

/**
 * The model is loaded here, outside the canvas, so a model that can't be loaded is a message and
 * not an error thrown inside React Three Fiber, which reports every error it sees as uncaught.
 */
function useModel(url: string) {
  return useQuery({
    queryKey: ["models", url],
    queryFn: async () => (await new GLTFLoader().loadAsync(url)).scene,
    staleTime: Infinity, // a build never changes
    retry: 1,
  });
}

function NotShown() {
  return (
    <p className="error viewer-message" role="alert">
      The 3D model could not be shown. The files below can still be downloaded.
    </p>
  );
}

/** Keeps a browser that can't draw in 3D (no WebGL) from taking the page down. */
class CanvasBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  override state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  override render() {
    return this.state.failed ? <NotShown /> : this.props.children;
  }
}

export function KilnViewer({ url }: { url: string }) {
  const model = useModel(url);
  return (
    <div className="viewer" aria-label="3D model of the kiln">
      {model.isError ? (
        <NotShown />
      ) : (
        <CanvasBoundary>
          <Canvas camera={{ position: [3, 2, 3], fov: 40, near: 0.01, far: 1e6 }}>
            <hemisphereLight args={["#ffffff", "#666666", 1.2]} />
            <directionalLight position={[5, 10, 7]} intensity={1.5} />
            {model.data && (
              <Bounds fit clip observe margin={1.2}>
                <primitive object={model.data} />
              </Bounds>
            )}
            <OrbitControls makeDefault />
          </Canvas>
        </CanvasBoundary>
      )}
    </div>
  );
}
