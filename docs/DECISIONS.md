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
- The first MVP will use Binance public market data as the canonical source.
- The first MVP quote refresh cadence is 60 seconds.
- The app is online-only for quote retrieval.
- The first MVP prioritizes reliability, clarity, and battery efficiency over pseudo-real-time animation.

## DEC-005 Asset Scope
- The first MVP targets Bitcoin first.
- The canonical MVP quote pair is BTC/USDT for display and data semantics.
- Multi-asset selection is future scope, likely managed from a companion phone surface.

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

## DEC-011 Binance Endpoint Contract
- The canonical MVP endpoint is `GET /api/v3/ticker/24hr` for `BTCUSDT` using the single-symbol path.
- This endpoint provides the required MVP fields in one response: current price, 24h variation, 24h high, and 24h low.
- The app should record its own fetch-success timestamp as the last successful update time instead of treating Binance market interval timestamps as the UI freshness timestamp.

## DEC-012 Validation Target
- The first validation target is the official Android XR AI glasses emulator paired with a phone AVD.
- Real hardware validation is deferred until compatible AI glasses hardware is available to the project.

## DEC-013 Implementation Shape
- The Android host app now uses the glasses-focused Compose layout as the canonical presentation.
- The first Android XR pass is additive: a projected AI-glasses activity is layered on top of the existing native Android data and state stack instead of rewriting the host app around XR-specific code.

## DEC-013A Market Value Presentation
- Raw Binance numeric strings are not acceptable as the user-facing presentation.
- Price, 24h high, and 24h low should be rendered with grouped US-style currency formatting consistent with the BTC/USDT market context.
- 24h percentage change should be rounded for fast reading.

## DEC-014 Projected Launch Constraint
- The projected glasses activity cannot be validated by direct `adb shell am start` invocation alone.
- The Android runtime rejects the launch with result code `102` when `requiredDisplayCategory='xr_projected'` is requested without the projected launch options supplied by `ProjectedContext`.
- The authoritative validation path for `GlassesMainActivity` is launch from the host app flow that creates projected activity options, not a plain shell start.

## DEC-015 Pairing Gate
- Even with a stable phone emulator and the AI glasses emulator running, the host app may still fail at `ProjectedContext.createProjectedActivityOptions(...)` if the projected device has not been registered or paired from the platform's point of view.
- The host app must not crash on this condition; it should log the failure and surface a clear pairing-needed message instead.

## Open Questions

### Product
- Should the first future phone companion slice start with single-asset switching or multi-asset watchlist selection?

### Platform
- What pairing and handoff behavior should the future companion phone surface expose when multiple tracked assets are enabled?

### Data
- When the product adds richer 24h visualization later, should it use Binance `klines` or a different chart-oriented source?
