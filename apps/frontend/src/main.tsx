import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App.tsx";
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "https://0ed160636c491507cae8825fa59ef94b@o4511216682795008.ingest.us.sentry.io/4511216719036416",
  // Setting this option to true will send default PII data to Sentry.
  // For example, automatic IP address collection on events
  sendDefaultPii: true,
});

async function enableMocking() {
  // You can add a check here for `dev` mode to conditionally enable this
  if (!import.meta.env.VITEST) return;

  const { worker } = await import("./utils/testing-utils/server");
  return worker.start();
}

enableMocking().then(() => {
  createRoot(document.getElementById("root")!).render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
});
