# Active Decisions And Open Questions

## Purpose
- Record only the active decisions that still shape the repository.
- Keep this file short and useful.

## DEC-001 Governance
- `AGENTS.md` is the primary execution contract.
- Agent contracts live under `docs/agents/`.
- Skills hold repeatable procedures, not permanent project rules.

## DEC-002 Current Phase
- The project is in active implementation for the approved MVP shell, with planning and documentation still required for scope and behavior changes.
- New project code, setup, build, emulator execution, device install, or validation should only happen when explicitly approved by the human in the current thread.

## DEC-003 Platform Direction
- The product target is Google AI glasses under the current Android XR development model.
- The current development assumption is a phone-hosted Android app surface projected to AI glasses during preview-phase tooling.
- The product is intended for direct AI-glasses relevance after the official hardware launch, but the current project truth must stay aligned with the platform reality available today.

## DEC-004 MVP Data Strategy
- The current host-side catalog and quote source is CoinGecko public market data.
- The first MVP quote refresh cadence is 60 seconds.
- The app is online-only for quote retrieval.
- The first MVP prioritizes reliability, clarity, and battery efficiency over pseudo-real-time animation.
- The host-side searchable top-50 list uses CoinGecko market-cap ranking with logo, current value, and summary retrieval.

## DEC-005 Asset Scope
- The first MVP now supports multi-asset selection on the host app from the top-50 market-cap list.
- The current default selected asset remains Bitcoin first.
- The selected asset still drives a single passive quote surface on glasses.
- Simultaneous multi-asset watchlists on the glasses surface remain future scope.

## DEC-006 History Scope
- The first MVP includes only recent 24h history available on a free tier.
- Day/week/month/year views are deferred.
- Full historical coverage is deferred until a source and cost model justify it.

## DEC-007 Battery Posture
- Battery cost is a first-class product constraint.
- The UI should only update when the underlying state changes or when a specific UX reason justifies motion.
- There is no automatic 1-second UI refresh in the MVP.

## DEC-007A Interaction Scope
- MVP is passive read-only.
- Gestures and interaction are post-MVP.

## DEC-007B Loading And Retry
- The MVP starts with a loading state.
- While the first quote has not loaded yet, the app retries every 5 seconds.
- After the first successful load, the app returns to the 60-second refresh cadence.

## DEC-007C Refresh Failure Behavior
- After the first successful load, a failed refresh clears the visible quote value from the glasses surface.
- The quote area switches to the standard loading indicator until connectivity is re-established and a fresh value is available.
- The product does not show a stale quote in the MVP once a refresh failure state begins.

## DEC-008 Future Companion Surface
- A future Android phone companion surface may allow choosing one or more assets and projecting that selection to AI glasses.
- This future companion surface is configuration-oriented and does not redefine the glasses-first product promise.

## DEC-009 Future Real-Time Path
- A future real-time path may use a backend that consumes a websocket market feed and republishes a constrained update stream to the app.
- This is explicitly post-MVP and should stay in backlog until the free 60-second MVP is working.

## DEC-010 Product Philosophy
- The product serves crypto traders who need continuous market awareness while doing other activities.
- The glasses surface must stay glanceable and passive first.
- The product should reduce interruption, not create another screen dependency.
- Battery efficiency and attention economy are core product values, not polish details.

## DEC-011 CoinGecko Endpoint Contract
- The canonical host catalog endpoint is `GET /api/v3/coins/markets` with USD pricing, market-cap ordering, and a top-50 page size.
- The host should use that endpoint for logo, rank, name, current price, 24h variation, 24h high, and 24h low.
- The coin detail modal should use `GET /api/v3/coins/{id}` for summary copy.
- The app should record its own fetch-success timestamp as the last successful update time instead of treating provider timestamps as the UI freshness timestamp.

## DEC-012 Validation Target
- The first validation target is the official Android XR AI glasses emulator paired with a phone AVD.
- Real hardware validation is deferred until compatible AI glasses hardware is available to the project.

## DEC-013 Implementation Shape
- The Android host app now uses the glasses-focused Compose layout as the canonical presentation.
- The first Android XR pass is additive: a projected AI-glasses activity is layered on top of the existing native Android data and state stack instead of rewriting the host app around XR-specific code.

## DEC-013A Market Value Presentation
-- Raw provider numeric strings are not acceptable as the user-facing presentation.
-- Price, 24h high, and 24h low should be rendered with grouped US-style currency formatting consistent with USD display context.
- 24h percentage change should be rounded for fast reading.

## DEC-013B Host Collection UX
- The host app should present the selected collection in a stacked, colorful card carousel inspired by the approved visual reference.
- Each collection card should use a coin-specific accent palette, with the card background driven by the coin secondary color where available or by a deterministic fallback palette.
- The host search list should show a round coin logo, name, and current value.
- Tapping a coin in the searchable list should open a bottom-sheet modal attached to the bottom edge, with a short summary, current value, and an add action.
- The user returns to the list by dismissing the modal or adding the coin.

## DEC-014 Projected Launch Constraint
- The projected glasses activity cannot be validated by direct `adb shell am start` invocation alone.
- The Android runtime rejects the launch with result code `102` when `requiredDisplayCategory='xr_projected'` is requested without the projected launch options supplied by `ProjectedContext`.
- The authoritative validation path for `GlassesMainActivity` is launch from the host app flow that creates projected activity options, not a plain shell start.

## DEC-015 Pairing Gate
- Even with a stable phone emulator and the AI glasses emulator running, the host app may still fail at `ProjectedContext.createProjectedActivityOptions(...)` if the projected device has not been registered or paired from the platform's point of view.
- The host app must not crash on this condition; it should log the failure and surface a clear pairing-needed message instead.

## DEC-016 Evidence Memory Pipeline
- The repository adopts a lightweight evidence-memory pipeline instead of a broad wiki model.
- Raw evidence belongs in `artifacts/` and must be curated by bundle in `artifacts/registry.json`.
- Project truth remains in `docs/`, especially `docs/OPERATIONS.md`, `docs/DECISIONS.md`, and `docs/FEATURES.md`.
- A reusable or decision-shaping evidence bundle is not considered complete until at least one authority doc references its bundle id or registered path.
- The maintenance path for this pipeline is `python tools/multiagent/evidence_pipeline.py lint` plus the playbook in `docs/playbooks/evidence_memory_pipeline.md`.
- The lint contract also enforces selected drift checks between canonical decisions and `docs/FEATURES.md`.
- The lint contract also enforces selected drift checks between `docs/PRD.md` and canonical decisions.
- New reusable bundles should be created through the scaffold command rather than hand-editing the registry.

## Evidence Bundles In Active Use
- `EV-EMU-LOGS` -> `artifacts/emulator/logs`
- `EV-ANALYSIS-APKS` -> `artifacts/analysis/AndroidGlassesCoreHost.apk` and related analysis files
- `EV-HOSTCORE-SMALI` -> `artifacts/analysis/hostcore-smali`
- `EV-PROJECTED-LIB` -> `artifacts/analysis/projected-lib`
- `EV-STUDIO-PLUGIN` -> `artifacts/analysis/studio-plugin`
- `EV-XR-PAIRING-2026-04-06-A` -> `artifacts/analysis/xr-pairing-2026-04-06-a` and related pairing-pass directories

## DEC-017 Current XR Pairing Failure Shape
- In `EV-XR-PAIRING-2026-04-06-A`, the pairing investigation advanced past empty Bluetooth state:
  - the host can record connected Bluetooth presence for both `com.google.android.glasses.core` and `com.google.android.glasses.companion`
  - the host can create emulated transports for those associations
- Even in that state, the host still reports `0 active virtual devices`.
- The strongest currently confirmed blocker is a host-side `CompanionDeviceManager` bind failure:
  - `Can not bind companion applications u0/com.google.android.glasses.companion: eligible CompanionDeviceService not found.`
- That failure happens even though package inspection still shows declared `android.companion.CompanionDeviceService` entries for both host packages.
- Current inference: the remaining pairing blocker is not merely lack of scan discovery, but a framework/runtime eligibility mismatch between CDM and the Google glasses companion packages on the host emulator build.

## DEC-018 Current Glasses-Side Pairing Failure Shape
- After upgrading the host-side Google glasses packages, the host pairing flow can now reach `com.android.companiondevicemanager/.CompanionAssociationActivity` and actively scan for `COMPANION_DEVICE_GLASSES`.
- In the same state, the glasses emulator still remains in `com.android.systemui/.xr.home.SysUiHomeActivity` and does not expose a user-visible pairing surface such as `Pair phone to ...`.
- The glasses Bluetooth stack reports `0 BLE apps registered` and an empty `GATT Advertiser Map` while the host is waiting for a BLE device.
- The glasses runtime does show `NearbyPresence` engine activity during earlier pairing windows, but the advertiser is not sustained after reboot or after subsequent pairing retries.
- Current inference: the latest blocker is now glasses-side advertiser activation on the `android-34/google-xr` emulator image, not the host-side phone flow.

## DEC-019 XR Environment Blockage Handling
- XR pairing and projection remain an environment/runtime concern until the emulator pair can create a working virtual device.
- The host app should surface XR launch blockage explicitly as environment state instead of implying a product logic failure.
- Product work on market data, host presentation, and glasses-focused information hierarchy can continue while XR pairing remains blocked.

## Open Questions

### Product
- Should the first future phone companion slice start with single-asset switching or multi-asset watchlist selection?

### Platform
- What pairing and handoff behavior should the future companion phone surface expose when multiple tracked assets are enabled?

### Data
- When the product adds richer 24h visualization later, should it stay on CoinGecko or switch to a different chart-oriented source?
