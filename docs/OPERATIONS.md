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
- Operational artifacts are consolidated under `artifacts/` instead of the repository root.
- The repository now uses a lightweight evidence-memory pipeline: raw evidence in `artifacts/`, tracked bundle metadata in `artifacts/registry.json`, and synthesized truth in the authority docs.
- `python tools/multiagent/evidence_pipeline.py lint` currently passes against the tracked bundle set.
- The `Daily Commit Minos` automation is now configured as a thread-bound heartbeat automation for this project, with local execution instead of Codex worktrees.
- This automation model is intended to preserve one local thread per project and avoid detached-head or `.git` write failures caused by isolated worktree execution.

## Active Evidence Bundles
- `EV-EMU-LOGS` -> `artifacts/emulator/logs`
- `EV-EMU-UI-DUMPS` -> `artifacts/emulator/ui-dumps`
- `EV-SDK-LOGS` -> `artifacts/sdk/logs`
- `EV-SDK-METADATA` -> `artifacts/sdk/metadata`
- `EV-ANALYSIS-APKS` -> `artifacts/analysis/AndroidGlassesCoreHost.apk` and related top-level analysis files
- `EV-HOSTCORE-SMALI` -> `artifacts/analysis/hostcore-smali`
- `EV-HOSTCORE-DEX` -> `artifacts/analysis/hostcore-dex`
- `EV-PROJECTED-LIB` -> `artifacts/analysis/projected-lib`
- `EV-STUDIO-PLUGIN` -> `artifacts/analysis/studio-plugin`
- `EV-ANDROID-CANARY-ROLES` -> `artifacts/analysis/android-canary-roles`
- `EV-XR-PAIRING-2026-04-06-A` -> `artifacts/emulator/logs/pairing-pass-2026-04-06-a`, `artifacts/emulator/ui-dumps/pairing-pass-2026-04-06-a`, `artifacts/analysis/xr-pairing-2026-04-06-a`

## Evidence Workflow
- Register reusable evidence bundles in `artifacts/registry.json`.
- Keep bundle-level synthesis in the authority docs, not in ad hoc notes.
- Use `python tools/multiagent/evidence_pipeline.py lint` before closing a documentation-heavy investigation task.
- For future XR pairing investigations, create or update a dedicated evidence bundle instead of storing untracked emulator dumps or reverse-engineering outputs.
- Treat `docs/PRD.md`, `docs/DECISIONS.md`, and `docs/FEATURES.md` as a checked trio for MVP coherence.

## Current Pairing Finding
- Official Android XR guidance requires pairing the AI glasses AVD with a phone-host AVD before projected activities can launch.
- The preferred path is Android Studio Device Manager > AI glasses AVD overflow menu > `Pair Glasses`, then selecting the host phone AVD and accepting both association requests on the phone emulator.
- If the Pairing Assistant fails, the manual fallback is to open the `Glasses` app on the phone emulator and choose `Set up Glasses`.
- If relaunch does not reconnect the emulators, Google documents wiping the AI glasses AVD data or forgetting the Bluetooth device on the phone emulator before pairing again.
- In `EV-XR-PAIRING-2026-04-06-A`, the host advanced beyond raw scan failure:
  - host `companiondevice` now shows connected Bluetooth devices for association ids `5`, `6`, and `7`
  - emulated transports exist for ids `5`, `6`, and `7`
  - the host still keeps `Bound Companion Applications: <empty>`
  - `virtualdevice` remains at `0 active virtual devices`
- The strongest current host-side failure is now a CDM bind failure recorded in `artifacts/analysis/xr-pairing-2026-04-06-a/host-cdm-binding-failure.txt`:
  - `Can not bind companion applications u0/com.google.android.glasses.companion: eligible CompanionDeviceService not found.`
- This means the resumed pairing investigation moved past simple Bluetooth visibility and into a framework/service-eligibility failure inside the host runtime.
- After updating the host-side Google glasses packages on `Pixel_9`, the host pairing surface improved further:
  - `com.google.android.glasses.core` now runs from `/data/app` at `260115020`
  - `com.google.android.glasses.companion` is enabled and reaches `SetupActivity`
  - the host now launches `com.android.companiondevicemanager/.CompanionAssociationActivity` for `COMPANION_DEVICE_GLASSES`
- The current blocker has shifted again and is now glass-side discovery:
  - the host is scanning in `CompanionAssociationActivity`
  - the glasses emulator remains on `com.android.systemui/.xr.home.SysUiHomeActivity`
  - the glasses Bluetooth stack reports `0 BLE apps registered`
  - the glasses `GATT Advertiser Map` remains empty
  - the host device list stays empty with the timeout message `Make sure this phone has Bluetooth turned on, and keep your device nearby.`
- Current evidence suggests the `android-34/google-xr` glasses image does not keep the pairing advertiser active after reboot in the same way as the older transient state that previously appeared during investigation.
- Local SDK inventory currently exposes only the XR glasses public image family `system-images;android-34;google-xr` revision `7` plus host phone images on `android-CANARY` and `android-36.1`.
- This means the current environment does not yet provide a newer locally installable XR glasses image that obviously supersedes the `android-34/google-xr` pairing behavior.
- App work should proceed with XR pairing treated as an environment blocker, not as a blocker on market-data or host-UI progress.

## Confirmed Constraints
- AI glasses are the target product surface.
- The first market-data path must be free and public.
- CoinGecko public market data is the canonical source for the current host catalog and market snapshot flow.
- The first quote refresh cadence is 60 seconds.
- The app is online-only.
- Bitcoin remains the default selected asset, but the host supports selecting from the top-50 market-cap catalog.
- MVP history scope is 24h only.
- CoinGecko `GET /api/v3/coins/markets` is the canonical host catalog and active-snapshot endpoint.
- CoinGecko `GET /api/v3/coins/{id}` is the canonical modal-summary endpoint.
- MVP starts in loading and retries every 5 seconds until the first quote loads.
- After first success, failed refreshes clear the visible quote and return the surface to the loading indicator until recovery.
- MVP interaction is passive read-only on glasses.
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
- Validate that the XR integration still builds cleanly as the preview APIs require explicit opt-in.
- Validate the actual projected launch path from the host app button once a stable phone-host emulator/runtime path is available.
- Add lightweight XR launch diagnostics in the host and projected activities to reduce blind debugging.
- Complete the phone/glasses pairing or projected-device registration step required before `ProjectedContext` can resolve a connected device.

### P2 Tooling
- Keep `artifacts/registry.json` aligned as new reusable evidence bundles appear.
- Use the evidence pipeline lint to catch undocumented artifacts or missing doc linkage.
- Use scaffolded bundle creation instead of manual registry edits for new investigation bundles.

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
