import { createRootRoute, createRoute, createRouter, Link, Outlet } from "@tanstack/react-router";

import { DesignList } from "./pages/DesignList";
import { DesignPage } from "./pages/DesignPage";
import { NewDesign } from "./pages/NewDesign";

const root = createRootRoute({
  component: () => (
    <>
      <nav className="topbar">
        <Link to="/" className="brand">
          Kilndesigner
        </Link>
      </nav>
      <Outlet />
    </>
  ),
});

const routeTree = root.addChildren([
  createRoute({ getParentRoute: () => root, path: "/", component: DesignList }),
  createRoute({ getParentRoute: () => root, path: "/designs/new", component: NewDesign }),
  createRoute({ getParentRoute: () => root, path: "/designs/$designId", component: DesignPage }),
]);

export const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
