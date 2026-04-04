# Operations

## Purpose
- Keep one compact source of truth for factual project state and the active execution queue.

## Current Posture
- The project is in active implementation for the approved MVP shell.
- A native Android app scaffold now exists with Kotlin, Compose UI, market-data polling, and the first Android XR integration pass.
- Android Studio, Android SDK command-line tools, platform-tools, and a baseline emulator environment already exist on the machine.
- Android XR environment preparation has started.
- `platforms;android-CANARY` is installed.
- XR and host-phone system image downloads are complete.
- The following AVDs now exist locally: `MinosAiGlasses`, `MinosHostCanary`, and `MinosHostStable`.
- Local build validation has been performed with the machine-wide Gradle installation.
- The APK installs on the host emulator and launches `MainActivity`.
- The APK also installs on the AI glasses emulator.
- The AI glasses emulator boots reliably and remains available through `adb`.
- The phone-host emulator path is still unstable in practice: the CANARY image produced repeated system ANRs, and the stable `android-36.1` host AVD still enters `offline` in both headless and windowed validation attempts.
- The latest `android-36.1` windowed run also reported `UpdateLayeredWindowIndirect failed`, suggesting a Windows-side emulator window/rendering issue on top of the `adb` instability.
- A manually opened Pixel phone emulator from Android Studio is stable through `adb` and can run the host app.
- With that manual host plus the AI glasses emulator active, the app reaches `ProjectedContext.createProjectedActivityOptions(...)`, but the runtime still reports `Projected device not found`.
- The host app now handles the missing projected-device condition without crashing and logs the pairing-required state explicitly.
- No successful end-to-end projected-activity handoff has been validated yet.
- Operational artifacts are being consolidated under `artifacts/` instead of the repository root.

## Current Pairing Finding
- Official Android XR guidance requires pairing the AI glasses AVD with a phone-host AVD before projected activities can launch.
- The preferred path is Android Studio Device Manager > AI glasses AVD overflow menu > `Pair Glasses`, then selecting the host phone AVD and accepting both association requests on the phone emulator.
- If the Pairing Assistant fails, the manual fallback is to open the `Glasses` app on the phone emulator and choose `Set up Glasses`.
- If relaunch does not reconnect the emulators, Google documents wiping the AI glasses AVD data or forgetting the Bluetooth device on the phone emulator before pairing again.

## Confirmed Constraints
- AI glasses are the target product surface.
- The first market-data path must be free and public.
- Binance public market data is the canonical source for the MVP.
- The first quote refresh cadence is 60 seconds.
- The app is online-only.
- Canonical MVP quote pair is BTC/USDT.
- MVP history scope is 24h only.
- Binance `GET /api/v3/ticker/24hr` for `BTCUSDT` is the canonical MVP market snapshot endpoint.
- MVP starts in loading and retries every 5 seconds until the first quote loads.
- After first success, failed refreshes clear the visible quote and return the surface to the loading indicator until recovery.
- MVP interaction is passive read-only.
- Battery efficiency matters more than cosmetic UI motion.

## External Dependencies To Decide Before Setup
- Android Studio channel choice for Android XR work
- Android XR emulator and system image version
- First physical device target, if any, once hardware becomes available

## Backlog

### P1 Scope Closure
- Confirm the first future-scope slice for the phone companion surface.

### P1 Planning
- Lock the product architecture for projected AI-glasses rendering.
- Lock the data model for quote, freshness, and historical snapshots.
- Lock the battery-aware refresh policy.
- Lock the backlog boundary between MVP and post-MVP real-time work.

### P2 Environment Setup
- Verify the current Android Studio installation against Android XR requirements.
- Complete the Android XR system image download.
- Complete the CANARY host-phone system image download.
- Create AI glasses and host-phone AVDs after the images finish installing.
- Verify tool and package versions after the environment is fully ready.

### P2 Implementation
- Finish the first projected AI-glasses activity using the official `androidx.xr.*` APIs.
- Keep a single comparison screen in the phone-hosted app that renders the baseline and glasses-focused variants together.
- Validate that the XR integration still builds cleanly as the preview APIs require explicit opt-in.
- Validate the actual projected launch path from the host app button once a stable phone-host emulator/runtime path is available.
- Add lightweight XR launch diagnostics in the host and projected activities to reduce blind debugging.
- Complete the phone/glasses pairing or projected-device registration step required before `ProjectedContext` can resolve a connected device.

### P2 Future Roadmap
- Companion phone configuration experience
- Multi-asset watchlist selection
- Backend websocket aggregation path
- More frequent quote updates where justified
- Richer historical charts
- Alerts and threshold-based surfacing

## Update Rule
- Keep this file factual and action-oriented.
- Do not use it as a changelog.
