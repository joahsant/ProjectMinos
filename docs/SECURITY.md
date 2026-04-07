# Security

## Purpose
- Define the minimum security contract for the current app plan.

## Secrets
- Never commit real provider keys, bearer tokens, or backend credentials.
- Prefer zero-key public market-data sources for the MVP when they are adequate.
- The current MVP path uses CoinGecko public endpoints without shipping provider secrets in the app.
- If a chosen provider later requires an API key, the key must enter the app through environment or platform-specific injection, not through repository-backed constants.

## Network And Transport
- Market-data requests must use HTTPS.
- Outside local development, any internal operational transport must use authenticated HTTPS.
- Do not silently downgrade transport security for convenience.

## Payload Safety
- Persist only the minimum market data needed for the user-visible product behavior.
- Do not log sensitive configuration, auth headers, or raw secret material.
- Keep any future websocket or backend payloads compact and bounded.

## Client And Backend Direction
- The MVP may call a free public market-data API directly if that path is sufficient and safe.
- A future backend-owned proxy or websocket fan-out path is acceptable only when it solves a clear product need such as tighter freshness, rate-limit control, or provider isolation.
- Future backend adoption must not happen silently; it requires a documented product and security decision first.

## Logging
- Debug logging may describe branch choice, cache age, and recoverable fallback behavior.
- Do not log full raw payloads if a compact summary is sufficient.

## Update Rule
- If a task changes secret handling, network transport, persistence scope, or backend architecture, update this file in the same task.
