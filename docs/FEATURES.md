# Features

## Purpose
- Keep one compact source of truth for current product behavior.

## Product Shell
- The product is an Android XR AI-glasses experience planned for native Android development.
- During the current platform preview model, the active runtime assumption is a phone-hosted surface projected to the glasses display.
- The product should remain glasses-first in behavior and information hierarchy.
- The surface is intended for traders who need to monitor BTC while doing something else, not for a full-screen desk replacement.

## MVP
- The MVP shows the current Bitcoin quote.
- The MVP shows the last successful update timestamp.
- The MVP refreshes the quote from the network every 60 seconds.
- The MVP starts in loading and retries every 5 seconds until the first successful quote arrives.
- The MVP is online-only.
- The MVP uses Binance public market data as the source of truth.
- The MVP shows 24h variation with high and low values.
- The MVP uses the Binance single-symbol 24hr ticker response as the canonical market snapshot contract.
- The MVP presents market values using human-readable grouped currency formatting instead of raw exchange strings.
- The MVP should avoid unnecessary UI redraws, loops, and background work.
- The MVP is passive read-only on glasses (no gestures).
- The current canonical host presentation is the glasses-focused UI, not the earlier baseline comparison layout.
- After the first successful load, failed refreshes clear the visible quote and replace it with the standard loading indicator.
- A fresh quote is shown again only after connectivity is re-established and a new successful response arrives.

## Initial User Value
- A trader can glance at the glasses display and understand the current Bitcoin price quickly.
- A user can understand whether the data is fresh.
- A user can see 24h context from variation, high, and low without opening a chart.

## Out Of Scope For MVP
- True sub-second or websocket-driven streaming
- Paid market-data providers
- Full historical market coverage
- Trading, orders, balances, wallets, or exchange authentication
- Offline mode
- Multiple-asset watchlists on the glasses surface
- Public-store distribution workflow

## Future Scope
- Companion phone configuration surface for selecting one or more assets
- Multiple tracked cryptocurrencies
- Better historical exploration
- Back-end market-feed aggregation for more frequent updates
- Alerts, thresholds, and summary cards
- Comparative asset views and watchlist projection

## Current Documentation Rule
- If feature behavior changes materially, update this file and any directly affected operations, security, or data-governance document in the same task.
