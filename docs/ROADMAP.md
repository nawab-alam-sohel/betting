# Platform Roadmap

This roadmap lists practical steps to evolve the VelkiList backend into a production-ready, 1xBet-like multi-vertical platform with Bangladesh focus (bn/en, BDT-first).

## Core pillars

- Money-safety: integer cents, `select_for_update` locking, reserve/finalize flows.
- Multi-language: `en`, `bn` via Django i18n + LocaleMiddleware.
- Multi-currency: BDT-first; plan extensibility for USD/EUR.
- Multi-location: geo-aware provider catalogs and restrictions.
- Fully Dockerized runtime with schema/docs and health endpoints.

## Immediate next steps

1) Sportsbook risk & limits
- Enforce stake limits per bet and per user (daily/weekly caps).
- Exposure checks per market (don’t exceed operator-configured max liability).
- Add `RiskRule` models and a small service (`apps.riskengine`) returning allow/deny + reason.
- Integrate checks in bet quote/place endpoints.

2) Casino provider integrations
- Replace `apps.casino.providers.generic` stub with real adapters using provider config (API keys, base URLs, auth/signature).
- Implement session/launch creation, callbacks for session ended, and optional balance transfer if the provider is wallet-separated.
- Add `CasinoProvider.config` JSON for credentials and launch options.

3) Commissions & affiliates
- Models: `CommissionPlan`, `CommissionRule`, `AgentAssignment`.
- Events: on bet placed/settled -> compute commission and record `Transaction(type='commission')`.
- Reports to track agent performance and payouts.

4) Fraud/AML & KYC
- KYC: require levels for deposit/withdrawal thresholds; add document statuses and audit trail.
- AML: velocity rules (deposits/withdrawals), device/IP risk signals, PEP/sanctions integration hooks.
- Case management endpoints for manual review.

5) Reconciliation
- Import payment-provider statements; match against `PaymentIntent` and `Transaction` records.
- Batch summary views and exception queues for mismatches.

6) Realtime (channels)
- Add Django Channels + Redis layer for market updates and bet slip pushbacks.
- Authenticated WS connections per user; topic-based subscriptions.

7) Reports
- Operator dashboards: GGR/NGR, bet volume, settlement time, user retention cohorts.
- CSV export endpoints and scheduled jobs (Celery) to deliver reports.

8) CMS (bn/en)
- Content types: `Banner`, `Promo`, `Page` with multilingual fields.
- Admin-friendly previews and publish scheduling.

## Configuration suggestions

- settings.py
  - SUPPORTED_CURRENCIES = ["BDT", "USD", "EUR"]
  - DEFAULT_CURRENCY = "BDT"
  - Add feature flags for modules by country/tenant.

## Testing & quality

- Keep unit tests near endpoints; add fixtures for bn/en content and BDT edge cases.
- Property tests for money math; fuzz inputs on bet placement and reconciliation.
- Smoke tests in `scripts/` extended to casino launch and sportsbook bet flows.

## Deployment notes

- Use `.env` for secrets; ensure `DJANGO_PRODUCTION=1` for secure cookies and HSTS.
- Run `collectstatic` via `entrypoint.sh` only in production.
- Add health checks on db/redis/web/worker; use them for orchestrator readiness.
