# Product Requirements Document

## Purpose
- Define the product contract for the first implementation phase of Project Minos.
- Translate the current vision, constraints, and MVP decisions into an execution-ready document.

## Product Summary
Project Minos is an Android XR product for Google AI glasses focused on crypto traders.
Its core job is to give the user continuous BTC market awareness without forcing them to stay locked to a phone or desktop screen.
The product is meant to be glanceable, passive, and useful while the trader is moving, working, or doing other activities.

## Problem
Crypto traders often feel tied to screens because price movement can create short windows for buying or selling.
This creates attention cost, interruption, and dependence on phones and desktop monitors.
Project Minos aims to reduce that dependence by surfacing the essential market signal in a lightweight glasses experience.

## Target User
- Crypto trader
- Needs frequent BTC awareness
- Cannot or does not want to stare at a phone or trading desk all the time
- Values quick understanding over deep on-device interaction

## Product Goals
- Let the user check BTC in one glance.
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
- Support a multi-asset watchlist in the first release

## Platform Scope
- Product target: Google AI glasses
- Current development model: Android XR projected experience from a phone-hosted Android app
- Product intent: glasses-first information design, even while current tooling uses the phone-hosted path

## MVP Scope
- Asset: `BTC/USDT`
- Market data source: Binance public market data
- Canonical endpoint: `GET /api/v3/ticker/24hr` for `BTCUSDT`
- Connectivity: online-only
- Refresh cadence after first success: every 60 seconds
- Startup behavior: loading state, retry every 5 seconds until first successful quote
- Interaction model: passive read-only on glasses
- Time horizon: recent 24h only
- Display contract:
  - current BTC price
  - 24h variation
  - 24h high
  - 24h low
  - last successful update time

## Core Product Principles
- Glance first, interact later.
- Minimize interruption.
- Favor stable signal over artificial “live” theater.
- Treat battery efficiency as a product requirement.
- Keep the surface understandable in one look.

## Primary User Story
As a crypto trader, I want to see the current BTC market state on AI glasses so I can keep monitoring the asset while doing other activities and still react when the market moves.

## MVP User Flow
1. User opens or activates the glasses experience.
2. The app shows a loading state.
3. The app retries every 5 seconds until the first quote arrives.
4. Once data is available, the app shows the BTC/USDT snapshot.
5. The app refreshes every 60 seconds after the first success.
6. The user reads the information passively without needing gestures or manual interaction.

## Required States

### Loading
- Shown before the first successful quote load.
- Retries every 5 seconds.

### Success
- Shows current price, 24h variation, 24h high, 24h low, and last successful update time.

### Error / Recovery
- After the first successful load, a failed refresh clears the visible quote.
- The quote area shows the standard loading indicator while recovery is in progress.
- A new quote appears only after the next successful response.

## Data Requirements
- Use Binance public endpoints only for the MVP.
- Keep the endpoint set minimal and sufficient for current price plus 24h context.
- For the MVP, use the Binance single-symbol 24hr ticker response as the main snapshot contract.
- Do not introduce a backend in the MVP.
- Do not require paid market-data providers in the MVP.

## UX Requirements
- Information must be readable quickly.
- Layout must favor short glance time and low cognitive load.
- The surface must avoid noisy updates or decorative motion.
- The design should communicate market awareness, not dashboard overload.

## Technical Constraints
- No project code, build, setup, emulator run, or downloads should begin until explicitly approved by the human.
- The product should be designed for battery-aware behavior.
- The MVP should avoid unnecessary background work and UI refreshes.

## Success Criteria
- User can understand the current BTC price in one glance.
- User can understand 24h directional context from variation, high, and low.
- The app reaches first successful load through the retry policy without user interaction.
- The steady-state experience refreshes every 60 seconds.
- The experience remains passive and usable without gestures.

## Out Of Scope For MVP
- Gestures
- Multi-asset configuration on glasses
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
