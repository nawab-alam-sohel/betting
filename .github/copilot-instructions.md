## VelkiList — AI agent guide (concise)
```instructions
## VelkiList — AI agent guide (concise, actionable)

Django 5.2 (Python 3.11) monolith for a betting platform with DRF + SimpleJWT, Celery/Redis, PostgreSQL, and a Next.js frontend (`velkilist-frontend/`). Keep edits small, respect per‑app boundaries in `apps/`, and be strict with money/accounting.

Big picture
- Domain apps live under `apps/`: users, wallets, bets, agents, payments, sports, notifications, casino, commissions, riskengine, fraud_aml, reconciliation, realtime, reports, cms, jobs, audit, adminpanel.
- API is composed per‑app in `apps/<app>/api/` and wired in `config/urls.py`. OpenAPI at `/api/schema/`, Swagger UI at `/api/docs/`, health at `/health/`.
- Auth uses a custom user (`AUTH_USER_MODEL='users.User'`) and JWT (SimpleJWT) with token endpoints at `/api/users/token/` (+ legacy alias `/api/auth/`).

```instructions
## VelkiList — AI agent guide (concise, actionable)

Django 5.2 (Python 3.11) monolith for a betting platform with DRF + SimpleJWT, Celery/Redis, PostgreSQL, and a Next.js frontend (`velkilist-frontend/`). Keep edits small, respect per‑app boundaries in `apps/`, and be strict with money/accounting.

Big picture
- Domain apps live under `apps/`: users, wallets, bets, agents, payments, sports, notifications, casino, commissions, riskengine, fraud_aml, reconciliation, realtime, reports, cms, jobs, audit, adminpanel.
- API is composed per‑app in `apps/<app>/api/` and wired in `config/urls.py`. OpenAPI at `/api/schema/`, Swagger UI at `/api/docs/`, health at `/health/`.
- Auth uses a custom user (`AUTH_USER_MODEL='users.User'`) and JWT (SimpleJWT) with token endpoints at `/api/users/token/` (+ legacy alias `/api/auth/`).

Money and safety rules
- Amounts are integer cents everywhere (e.g., `Wallet.balance_cents`, `Transaction.amount_cents`) — never floats. Use Decimal only for display.
- Wrap balance mutations in `transaction.atomic()` and lock with `select_for_update()`; see `apps/bets/tasks.py` and `apps/wallets/api/views.py` for examples.
- Record every balance change as a `Transaction` with type in {deposit, withdraw, bet, hold, commission, win, refund}. Maintain reserved funds via `Wallet.reserve()` and `finalize_reservation()` before settlement.

Key flows and files
- Payments: `/api/payments/initiate/` creates `PaymentIntent`; provider webhooks call `/api/payments/webhook/<provider>/` and credit wallets. See `apps/payments/api/views.py`.
- Withdrawals & reconciliation: router endpoints in `apps/payments/api/urls.py`; models in `apps/payments/models_recon.py`; admin actions in `views_recon.py`.
- Sportsbook catalog: models in `apps/sports/models.py`; provider adapter at `apps/sports/providers/generic.py`. Toggle DEMO vs REAL with `SPORTS_USE_DEMO`. Commands in `apps/sports/management/commands/*`.
- Admin dashboard API (custom cards): `apps/adminpanel/api/` exposes `GET /api/admin/dashboard/summary/` and `/charts/` aggregating Users, KYC, Wallet Transactions, Bets, and Sports `Game` status.
- Notifications: provider-agnostic service in `apps/notifications/services.py` (SMS/Email/In‑App stubs), logs in `apps/notifications/models.py`.

Runtime/services
- Docker Compose: `web` (Django), `worker` (Celery), `db` (Postgres 15), `redis` (7), `frontend` (Next.js). See `docker-compose.yml` and `entrypoint.sh` (migrates on boot; prod via `DJANGO_PRODUCTION=1`).
- Env from `.env`; toggles in `config/settings.py` (DB/JWT/CORS/Redis, `CASINO_USE_DEMO`, `SPORTS_USE_DEMO`). Static/media: `staticfiles/`, `config/media/`.

Everyday commands (Windows PowerShell)
- Start: `docker compose up --build`
- Migrate: `docker compose exec web python manage.py migrate`
- Superuser: `docker compose exec web python manage.py createsuperuser`
- Sports demo sync: `docker compose exec web python manage.py configure_sports_provider --key=generic` then `docker compose exec web python manage.py sync_sports_data --provider=generic`
- Casino demo seed: `docker compose exec web python manage.py seed_casino`
- Smoke (host): `$env:SMOKE_BASE='http://localhost:8000'`; `python scripts/smoke_test.py`; sports-only: `python scripts/sports_smoke.py`

Tests & dev conventions
- Tests live per app (e.g., `apps/bets/tests.py`, `apps/bets/tests_integration.py`, `apps/payments/tests_recon.py`).
- Run all: `docker compose exec web python manage.py test`; single module: `docker compose exec web python manage.py test apps.bets.tests`
- Style: Black + Ruff (line length 88; ignore E203/W503) per `pyproject.toml`. Prefer ViewSets+routers for CRUD; use `APIView` for bespoke endpoints (wallets/payments).
- Celery tip: call `task.apply(args=(... ,))` synchronously in tests (see `apps/bets/tests.py`).

Patterns by example
- Safe wallet mutation: within `transaction.atomic()` + `select_for_update()` on `Wallet`; mutate `balance_cents`/`reserved_balance_cents`, then create a `Transaction`. See `apps/wallets/api/views.py::DepositView` and `apps/bets/tasks.py`.
- DRF pattern: register ViewSets via `DefaultRouter` (e.g., reconciliation in `apps/payments/api/urls.py`); keep purpose-built flows as `APIView` (wallets, payments initiate/webhook).
- Provider sync (REAL): implement HTTP + idempotent upserts with timeouts in `apps/sports/providers/generic.py::sync_real`.
 - Provider adapter checklist (REAL): store creds via configure command (DB `config` JSON), use `base_url` + `api_key`, upsert by stable external IDs, use 10–15s timeouts with minimal retries, and keep runs idempotent.

Gotchas
- Ensure `.env` includes `SECRET_KEY`, `DB_*`, `CORS_ALLOWED_ORIGINS`; missing values break startup.
- `scripts/smoke_test.py` defaults to `http://web:8000` (Docker network). From host, set `SMOKE_BASE=http://localhost:8000`.
- Provider toggles: DEMO uses local data; REAL requires adapter HTTP logic (sports/casino).

Start here when changing behavior
- Money flow: `apps/wallets/*`, `apps/bets/tasks.py`, `apps/payments/api/*`.
- Admin widgets & analytics: `apps/adminpanel/api/*`.
- Sports data import: `apps/sports/providers/*` + management commands.

Useful references
- API entrypoints: `config/urls.py`
- Settings & toggles: `config/settings.py`
- Compose & runtime: `docker-compose.yml`, `entrypoint.sh`
- Smoke scripts: `scripts/smoke_test.py`, `scripts/sports_smoke.py`, `scripts/test_withdrawal_post.py`
- Roadmap: `docs/ROADMAP.md`; Frontend: `velkilist-frontend/`
```