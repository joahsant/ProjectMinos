# Activation Matrix

## Purpose
- Provide a compact routing reference for Lead intake decisions.

## Classification Heuristics
- `trivial patch`: tightly localized, reversible, and no product, UX, market-data, or governance impact.
- `localized change`: bounded implementation or review with low blast radius and clear owner.
- `feature flow`: user-visible behavior, new states, new failure paths, or unclear flow/data implications.
- `structural initiative`: governance, architecture, repository-wide tooling, cross-cutting data/runtime changes, or broad blast radius.

## Default Role Depth
- `trivial patch`
  - Lead: `deep analysis`
  - Product: `no-impact confirmation`
  - UX/UI: `light validation`
  - Market Data: `no-impact confirmation`
  - Engineer: `light validation`
  - QA: `light validation`
  - Documentation / Historian: `light validation`
- `localized change`
  - Lead: `deep analysis`
  - Product: `light validation`
  - UX/UI: `light validation` when the surface is user-visible
  - Market Data: `light validation` when quote semantics or refresh policy are touched
  - Engineer: `deep analysis`
  - QA: `light validation`
  - Documentation / Historian: `light validation`
- `feature flow`
  - Lead: `deep analysis`
  - Product: `deep analysis`
  - UX/UI: `deep analysis` when the surface or state messaging changes
  - Market Data: `deep analysis` when freshness, provider, symbols, or history semantics change
  - Engineer: `deep analysis`
  - QA: `deep analysis`
  - Documentation / Historian: `deep analysis`
- `structural initiative`
  - All active roles default to `deep analysis` unless explicitly proven unnecessary

## Trigger Signals
- Activate `Product Strategist` deeply when:
  - behavior is underdefined
  - new states, retries, or empty/error states are introduced
  - MVP versus future-scope boundaries are unclear
- Activate `UX/UI Strategist` deeply when:
  - glanceability, readability, interaction timing, accessibility, or battery-aware rendering is at issue
  - the glasses or companion surface changes materially
- Activate `Market Data Analyst` deeply when:
  - source selection, quote semantics, refresh cadence, freshness guarantees, or history coverage changes
  - free/public source constraints may drive UX or architecture
- Activate `QA` deeply when:
  - the likely failure locality is unclear
  - the request introduces new states, recovery behavior, or regressions with broad blast radius

## Gate Discipline
- Lead always opens with `Understanding / Plan`.
- Non-trivial work should make the planning path explicit before implementation.
- Documentation must be updated before or alongside implementation when truth changes.
