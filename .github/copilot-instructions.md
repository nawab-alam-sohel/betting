## VelkiList backend — quick AI guidance

This Django monolith implements core betting functionality (users, wallets, bets, payments, agents, sports).
Keep changes minimal and explicit; reference the files below when making edits.

Key facts
- Python 3.11, Django 5.2. Project uses JWT (SimpleJWT), Celery + Redis, and PostgreSQL. See `requirements.txt`.
- Services are Dockerized. Primary compose services: `web`, `db`, `redis`, `worker`. See `docker-compose.yml` and `Dockerfile`.
- Custom user model: `apps/users/models.py` (AUTH_USER_MODEL set in `config/settings.py`).

Architecture & data flows
- Apps split by domain: `apps.users`, `apps.wallets`, `apps.bets`, `apps.payments`, `apps.agents`, `apps.sports`.
- Money is stored as integer cents (field names like `*_cents`) — do not switch to floats. Use helper properties (e.g., `Wallet.balance`) when producing decimal strings.
- Payment flows: `apps/payments/api/views.py` exposes `initiate/` and `webhook/<provider>/`. Provider adapters live in `apps/payments/providers/` (see `bkash.py` — a dev stub).
- Wallets use `reserved_balance_cents` for in-flight holds. Look for `reserve()` and `finalize_reservation()` in `apps/wallets/models.py` and `select_for_update()` usage in tasks.
- Asynchronous work: Celery tasks live in app `tasks.py` (e.g., `apps/bets/tasks.py`). Worker is started via the `worker` service or `entrypoint.sh` when `WORKER=1`.

Developer workflows (most common)
- Start locally with Docker: from repo root run `docker compose up --build` (See README).
- Apply migrations inside `web` container: `docker compose exec web python manage.py makemigrations` then `docker compose exec web python manage.py migrate`.
- Create superuser: `docker compose exec web python manage.py createsuperuser`.
- Run tests inside container: `docker compose exec web python manage.py test`.
- Run a Celery worker locally: `docker compose exec worker` (worker service already configured). Alternative: set `WORKER=1` and start the image (see `entrypoint.sh`).

Project-specific conventions & gotchas
- Use cents integers for money and never mutate `balance_cents` without DB locking for concurrent flows. Many places rely on `select_for_update()`.
- User roles are stored in `apps/users/models.py` as `Role` (slug + level). Check role helper methods such as `has_minimum_role_level()`.
- Payment providers are adapters that return predictable fake responses for development. Replace `apps/payments/providers/bkash.py` internals with real HTTP calls and signature verification when integrating sandbox/production.
- Reconciliation endpoints and models exist (see `apps/payments/api/views_recon.py`, migrations `0002_recon.py`, `0003_alter_paymentintent_flow_and_more.py`). If you change reconciliation models, update migrations and index definitions.
- Admin theme: `django-jazzmin` configured in `config/settings.py` — menu and icons are customized there.

Examples and quick references
- Initiate a server-side payment: POST to `/api/payments/initiate/` with JSON `{ "provider": "bkash", "amount": "100.00", "flow": "server" }`. See `apps/payments/api/views.py` and serializer `apps/payments/api/serializers.py`.
- Webhook payloads: webhook handler expects `intent_id`, `status`, and optional `reference`. Look at `WebhookView` in `apps/payments/api/views.py`.
- Settling bets: task `settle_bet_task` in `apps/bets/tasks.py` uses `transaction.atomic()` and `select_for_update()` on `Bet` and `Wallet`. Follow that pattern for money-critical flows.

When editing code
- If you touch models: run `makemigrations` and `migrate`. Prefer small, incremental migrations.
- If you alter payment or wallet logic: add unit tests under the affected `apps/*/tests.py` files and run `python manage.py test`.
- Preserve existing API contracts (URLs in `apps/*/api/urls.py`); update API serializers when shape changes.

Where to look first
- `config/settings.py` — environment flags (DEBUG, DJANGO_PRODUCTION), Redis/Celery, JWT settings.
- `docker-compose.yml`, `Dockerfile`, `entrypoint.sh` — container lifecycle and dev vs prod behavior.
- `apps/payments/providers/` — provider adapter pattern and dev stubs.
- `apps/wallets/models.py`, `apps/bets/tasks.py` — canonical money handling patterns.

If anything in this file is unclear or you need additional examples (tests, common queries, or a sample API call), ask and I will iterate.
# VelkiList Backend AI Agent Instructions

This guide helps AI coding agents be productive in this Django-based betting platform backend.

## Project Architecture

- **Core Framework**: Django 5.2 with Django REST Framework + SimpleJWT for authentication
- **Key Apps**:
  - `users`: Custom user model with email-based auth and role management
  - `wallets`: Balance management and transactions
  - `bets`: Betting system core functionality
  - `agents`: Agent management system
  - `payments`: Payment processing with reconciliation features

## Service Components

- **Web Server**: Django application (`web` container)
- **Database**: PostgreSQL 15 (`db` container)
- **Task Queue**: Celery with Redis (`worker` and `redis` containers)
- **Static/Media**: Served from Docker volumes (`static_volume` and `media_volume`)

## Development Workflow

### Environment Setup
```shell
# 1. Create .env with required variables:
#    DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
#    SECRET_KEY (50+ chars in production)
#    DJANGO_PRODUCTION=0/1

# 2. Build and start services
docker compose up --build

# 3. Run migrations
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### Testing & Development
- Run tests: `docker compose exec web python manage.py test`
- Django shell: `docker compose exec web python manage.py shell`
- Code checks: `docker compose exec web python manage.py check`

## Project Conventions

1. **Authentication**:
   - JWT-based using `rest_framework_simplejwt`
   - Access token lifetime: 60 minutes
   - Refresh token lifetime: 7 days
   - Bearer token format

2. **Models & Database**:
   - Custom user model using email as identifier
   - All money values stored in cents (integer)
   - Migration files should be committed

3. **Security & Environment**:
   - Production mode via `DJANGO_PRODUCTION=1`
   - SSL/HSTS enforced in production
   - All sensitive data via environment variables

## Common Patterns

1. **API Structure** (example from `payments` app):
   ```
   apps/payments/
   ├── api/
   │   ├── serializers.py    # Main serializers
   │   ├── serializers_recon.py  # Specialized serializers
   │   ├── urls.py           # URL routing
   │   ├── views.py          # Main views
   │   └── views_recon.py    # Specialized views
   ```

2. **Testing**:
   - Main tests in `tests.py`
   - Integration tests in `tests_integration.py`
   - Specialized tests in `tests_*.py` (e.g., `tests_recon.py`)

## Key Integration Points

1. **Celery Tasks**:
   - Defined in app-specific `tasks.py`
   - Redis as broker and result backend
   - Task results serialized as JSON

2. **Static/Media Files**:
   - Static: `/static/` → `staticfiles/`
   - Media: `/media/` → `config/media/`

## When Making Changes

1. Always run:
   - `python manage.py check` for Django system checks
   - `python manage.py test` affected apps
   - Create/apply migrations if model changes

2. Remember to:
   - Keep money values in cents (integer)
   - Follow app-specific serializer/view patterns
   - Add tests for new functionality
   - Update environment variables in documentation