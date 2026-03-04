import * as Sentry from "@sentry/astro";

Sentry.init({
  dsn: "https://b2444d1c6a314d090437d15631d1e222@o4508247438655488.ingest.us.sentry.io/4510983744192512",
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
  ],
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
