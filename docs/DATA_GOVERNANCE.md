# Data Governance

## Purpose
- Keep market data, user preferences, and operational telemetry clearly separated.

## Data Domains

### Market Data Cache
- Includes the latest quote snapshot, freshness metadata, and recent historical points required for user-visible views.
- Sensitivity: low.
- Retention should stay short and product-driven.

### User Preferences
- Includes selected asset, host-side saved collection, display options, and future companion-surface configuration.
- Sensitivity: low to medium.
- User preferences should remain separate from telemetry.

### Operational Telemetry
- Includes crashes, health signals, and compact operational diagnostics when telemetry is later introduced.
- Sensitivity: internal.
- Telemetry must not become the source of truth for user preferences or market history.

## Separation Rules
- Do not mix user preferences into telemetry datasets.
- Do not keep unnecessary long-lived market-history storage in the MVP.
- Keep future companion-surface pairing state separate from quote cache state.
- Keep the saved host-side coin collection separate from transient market snapshot cache state.

## Retention Direction
- Market-data cache should be retained only as long as it improves the user experience.
- User preferences follow the user lifecycle.
- Operational telemetry should be retained only as long as needed for support and reliability.

## Redaction Rule
- Telemetry and diagnostics should prefer compact structured records over raw dumps.
- If future backend ingestion exists, request-size caps and sanitization must be enforced.

## Update Rule
- If a feature writes new persistent user state, telemetry, or long-lived market data, update this file in the same task.
