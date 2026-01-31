# PWA Configuration & Status

## Overview
Pegion uses `next-pwa` to provide Progressive Web App capabilities (Installability, Offline Support, Caching).

## Current Status: **DISABLED**
As of Phase 7.1 (Jan 2025), the PWA generation is **disabled** in `next.config.ts`.

### Why?
Next.js 16 uses **Turbopack** by default for development and builds. Currently, `next-pwa` (and its underlying `workbox-webpack-plugin`) has compatibility issues with Turbopack's webpack interoperability layer, leading to `WorkerError` during `npm run build`.

### How to Re-enable

**Option A: Enable Turbopack Compatibility (Future)**
When `next-pwa` updates to support Turbopack, or if you switch to the standard Webpack bundler.

**Option B: Force Webpack (Current Workaround)**
You can force Next.js to use Webpack instead of Turbopack:
```bash
# In package.json
"build": "next build --no-turbo"
# OR via env var
NEXT_DISABLE_TURBOPACK=1 next build
```

Then in `next.config.ts`:
1.  Uncomment the `withPWA` wrapper.
2.  Change `module.exports = nextConfig` to `module.exports = withPWA(nextConfig)`.

### Alternative Recommendation
If `next-pwa` remains flaky, consider using **Workbox CLI** directly to generate your service worker, decoupling it from the Next.js bundler entirely. This provides the most robust long-term solution.
