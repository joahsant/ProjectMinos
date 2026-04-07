# Product Requirements Document

## Purpose
- Define the product contract for the first implementation phase of Project Minos.
- Translate the current vision, constraints, and MVP decisions into an execution-ready document.

## Product Summary
Project Minos is an Android XR product for Google AI glasses focused on crypto traders.
Its core job is to give the user continuous crypto market awareness without forcing them to stay locked to a phone or desktop screen.
The product is meant to be glanceable, passive, and useful while the trader is moving, working, or doing other activities.

## Problem
Crypto traders often feel tied to screens because price movement can create short windows for buying or selling.
This creates attention cost, interruption, and dependence on phones and desktop monitors.
Project Minos aims to reduce that dependence by surfacing the essential market signal in a lightweight glasses experience.

## Target User
- Crypto trader
- Needs frequent crypto market awareness
- Cannot or does not want to stare at a phone or trading desk all the time
- Values quick understanding over deep on-device interaction

## Product Goals
- Let the user check the selected coin in one glance.
- Reduce the need to keep opening or watching a phone.
- Keep the experience passive and low interruption.
- Preserve battery by avoiding unnecessary rendering and polling behavior.
- Deliver a stable and trustworthy MVP before adding richer interaction.

## Non-Goals
- Replace a trading terminal
- Execute trades
- Authenticate with exchanges
- Provide full charting tools
- Deliver true real-time sub-second streaming in the MVP
- Support simultaneous multi-asset presentation on glasses in the first release

## Platform Scope
- Product target: Google AI glasses
- Current development model: Android XR projected experience from a phone-hosted Android app
- Product intent: glasses-first information design, even while current tooling uses the phone-hosted path

## MVP Scope
- Asset catalog: top-50 cryptocurrencies by market cap
- Default selected asset: `Bitcoin`
- Market data source: CoinGecko public market data
- Canonical endpoints:
  - `GET /api/v3/coins/markets` for host catalog and current market snapshot
  - `GET /api/v3/coins/{id}` for coin summary in the host bottom sheet
- Connectivity: online-only
- Refresh cadence after first success: every 60 seconds
- Startup behavior: loading state, retry every 5 seconds until first successful quote
- Interaction model: passive read-only on glasses
- Time horizon: recent 24h only
- Display contract:
  - current selected coin price
  - 24h variation
  - 24h high
  - 24h low
  - last successful update time
  - host-side searchable top-50 list with logo, name, and current value
  - host-side bottom-sheet coin preview with summary and add action
  - host-side selected collection rendered as a colorful stacked-card carousel

## Core Product Principles
- Glance first, interact later.
- Minimize interruption.
- Favor stable signal over artificial “live” theater.
- Treat battery efficiency as a product requirement.
- Keep the surface understandable in one look.

## Primary User Story
As a crypto trader, I want to choose the crypto assets I care about on the host app and see the selected one on AI glasses so I can keep monitoring the market while doing other activities and still react when the market moves.

## MVP User Flow
1. User opens the host app.
2. The app shows the current collection and a searchable top-50 catalog.
3. User searches for a coin and taps it.
4. The app opens a bottom-sheet preview with a summary and add action.
5. User adds the coin to the collection.
6. User browses the stacked-card carousel and selects the active coin.
7. The app retries every 5 seconds until the first quote for the active coin arrives.
8. Once data is available, the app shows the selected coin snapshot.
9. The app refreshes every 60 seconds after the first success.
10. The glasses surface remains passive and follows the active selected coin.

## Required States

### Loading
- Shown before the first successful quote load.
- Retries every 5 seconds.

### Success
- Shows current price, 24h variation, 24h high, 24h low, and last successful update time for the active selected coin.
- Shows the host collection cards and searchable catalog.

### Error / Recovery
- After the first successful load, a failed refresh clears the visible quote.
- The quote area shows the standard loading indicator while recovery is in progress.
- A new quote appears only after the next successful response.

## Data Requirements
- Use CoinGecko public endpoints only for the MVP.
- Keep the endpoint set minimal and sufficient for ranked catalog, logos, summaries, and current 24h context.
- Use the market list endpoint for the host catalog and current active-coin snapshot contract.
- Use the coin detail endpoint for a short summary in the host bottom sheet.
- Do not introduce a backend in the MVP.
- Do not require paid market-data providers in the MVP.

## UX Requirements
- Information must be readable quickly.
- Layout must favor short glance time and low cognitive load.
- The surface must avoid noisy updates or decorative motion.
- The design should communicate market awareness, not dashboard overload.
- The host collection cards should follow the approved stacked-card visual direction closely.
- The host list should prioritize quick scanning of logo, name, and price.
- The bottom sheet should feel attached to the bottom edge rather than like a detached dialog.

## Technical Constraints
- No project code, build, setup, emulator run, or downloads should begin until explicitly approved by the human.
- The product should be designed for battery-aware behavior.
- The MVP should avoid unnecessary background work and UI refreshes.

## Success Criteria
- User can search the top-50 catalog and add a coin to the host collection without confusion.
- User can understand the current selected-coin price in one glance.
- User can understand 24h directional context from variation, high, and low.
- The app reaches first successful load through the retry policy without user interaction.
- The steady-state experience refreshes every 60 seconds.
- The experience remains passive and usable without gestures.

## Out Of Scope For MVP
- Gestures
- Simultaneous multi-asset configuration on glasses
- Phone companion configuration flow
- Real-time websocket market feed
- Alerts and thresholds
- Rich charting
- Full historical exploration
- Public distribution workflow

## Post-MVP Roadmap
- Phone companion surface for asset selection
- Additional cryptocurrencies
- Gesture-based interaction
- Better historical exploration
- Backend websocket aggregation for tighter freshness
- Alerts and watchlist behavior

## Open Decisions
- Which physical AI-glasses device becomes the first real hardware validation target
- Which first phone companion slice should come after the passive glasses MVP

## Source Alignment
- Product vision: `README.md`
- Current feature truth: `docs/FEATURES.md`
- Current decisions: `docs/DECISIONS.md`
- Current operational posture: `docs/OPERATIONS.md`
