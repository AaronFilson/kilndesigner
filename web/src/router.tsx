import {
  createRootRoute,
  createRoute,
  createRouter,
  type ErrorComponentProps,
  Link,
  Outlet,
} from "@tanstack/react-router";

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

/** A page that failed: what happened, and a way back, under the top bar. */
function PageError({ error }: ErrorComponentProps) {
  return (
    <main className="page">
      <h1>This page could not be shown</h1>
      <p className="error">{error instanceof Error ? error.message : String(error)}</p>
      <p>
        <Link to="/">Back to the designs</Link>
      </p>
    </main>
  );
}

export const router = createRouter({ routeTree, defaultErrorComponent: PageError });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
