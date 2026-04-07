# Project Minos

Project Minos is an Android XR product in planning for Google AI glasses.

## Product Vision
Project Minos gives crypto traders continuous market awareness without forcing them to stare at a screen.
The glasses surface stays glanceable, passive, and low interruption so the user can keep doing other things while still tracking the selected market.

## Product Principles
- Glance first, interact later.
- Keep the user free to move, work, or live while the app watches the market.
- Favor battery efficiency over unnecessary redraws or motion.
- Prefer a stable, trustworthy signal over flashy real-time theater.
- Keep the surface minimal enough to understand in one look.

## Current Goal
- Build an MVP that lets the user curate and select from a top-50 crypto catalog on the host app and show the active coin on AI glasses.
- Use a free public data source.
- Use CoinGecko public market data as the canonical MVP source.
- Keep the app online-only for quote retrieval.
- Use 60-second network refresh for the first MVP.
- Start with loading and retry every 5 seconds until the first quote arrives.
- Support recent free history only in the first release slice.
- Show 24h variation with high and low values.

## MVP Scope
- Asset catalog: top-50 cryptocurrencies by market cap
- Default selected asset: `Bitcoin`
- Data source: CoinGecko public market data
- Canonical endpoints:
  - `GET /api/v3/coins/markets`
  - `GET /api/v3/coins/{id}`
- Refresh cadence: every 60 seconds after the first successful load
- Startup behavior: loading state, then retry every 5 seconds until data arrives
- Display: current selected-coin price, 24h variation, 24h high, and 24h low
- Host flow: searchable top-50 list, bottom-sheet coin preview, and stacked collection cards
- Interaction: passive read-only on glasses
- History: recent 24h only
- Network posture: online-only
- Failure behavior: clear the visible quote after refresh errors and show the standard loading indicator until a fresh response arrives

## Current Delivery Phase
- Native Android MVP implementation in progress
- Product architecture and documentation refinement
- Android XR emulator environment prepared
- Initial build and emulator validation already executed

## Repository Layout
- `app/` Android application code
- `docs/` project governance, product, and operations
- `artifacts/` raw evidence bundles with tracked metadata in `artifacts/registry.json`
- `artifacts/emulator/` emulator run logs and captured UI dumps
- `artifacts/sdk/` SDK and package-manager diagnostic logs
- `repo-search/` local research scratch area kept outside the app module

## Start Here
- `AGENTS.md`
- `docs/README.md`
- `docs/PRD.md`
- `docs/OPERATIONS.md`
- `docs/FEATURES.md`
- `docs/DECISIONS.md`
- `docs/SECURITY.md`
- `docs/DATA_GOVERNANCE.md`

## Documentation Layout
- `docs/README.md` is the entry point for the documentation set.
- `docs/PRD.md` defines the product contract and MVP intent.
- `docs/FEATURES.md` records current product behavior.
- `docs/OPERATIONS.md` records factual project state and the execution queue.
- `docs/DECISIONS.md` records active decisions and open questions.
- `docs/SECURITY.md` covers secrets, transport, and security posture.
- `docs/DATA_GOVERNANCE.md` covers storage, retention, and external data handling.
- `artifacts/registry.json` tracks reusable evidence bundles that back the current docs.

## Planned Product Shape
- Primary surface: AI glasses projected experience
- Future companion surface: Android phone configuration and asset selection
- Future backend option: websocket-fed aggregation path for sub-minute real-time updates when justified

## Future Backlog
- Add gesture-based interaction after the passive MVP proves useful.
- Add a phone companion surface for selecting one or more assets.
- Add richer historical charts and comparisons.
- Add a backend market-feed aggregation path if tighter freshness becomes worth the tradeoff.
- Add alerts, thresholds, and watchlist projection later.
