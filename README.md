# velkilist-backend

Django backend for VelkiList (users app, JWT auth, PostgreSQL Docker setup).

Quick start (using Docker):

1. Create a `.env` with DB and secret settings (see `.env.example` if provided).
2. Build and run:

```powershell
cd F:\VelkiList\velkilist-backend
docker compose up --build
```

3. Apply migrations inside the `web` container:

```powershell
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

4. Create superuser and visit admin:

```powershell
docker compose exec web python manage.py createsuperuser
# Visit http://localhost:8000/admin
```

## Development

Services are defined in `docker-compose.yml`. Environment variables are loaded from `.env`.

- Web: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/api/docs/
- Health: http://localhost:8000/health/

### New modules and endpoints

We scaffolded and wired additional apps to support a 1xBet-like platform footprint. Each module exposes a simple `/health/` endpoint under `/api/<module>/` to validate wiring:

- `/api/casino/` — providers, categories, games (A–Z filter), and `POST /launch/`
- `/api/commissions/health/`
- `/api/riskengine/health/`
- `/api/fraud-aml/health/`
- `/api/reconciliation/health/`
- `/api/realtime/health/`
- `/api/reports/health/`
- `/api/cms/health/`
- `/api/jobs/health/`
- `/api/audit/health/`

Casino demo data: run `python manage.py seed_casino` inside the web container.

### Providers: Casino and Sports (DEMO vs REAL)

Toggles (in `.env`):

- `CASINO_USE_DEMO=1` (default) — return local demo launch URLs for games
- `SPORTS_USE_DEMO=1` (default) — populate sportsbook with demo data

Provider configuration commands (store credentials/metadata in DB):

```powershell
# Casino
docker compose exec web python manage.py configure_casino_provider --key=generic --name="Generic Casino" --base-url="https://api.example.com" --config='{"api_key": "REDACTED"}'

# Sports
docker compose exec web python manage.py configure_sports_provider --key=generic --name="Generic Sports" --base-url="https://api.example.com" --config='{"api_key": "REDACTED"}'
```

Sync sportsbook data (uses DEMO or REAL based on `SPORTS_USE_DEMO`):

```powershell
docker compose exec web python manage.py sync_sports_data --provider=generic
```

Notes:

- In DEMO mode, a minimal Football → Demo League with a sample game and 1X2 market is created.
- In REAL mode (`SPORTS_USE_DEMO=0`), implement the HTTP calls inside `apps/sports/providers/generic.py::sync_real` and re-run the sync command.

### Localization and Bangladesh focus

- Default timezone: `Asia/Dhaka`
- Languages: English (`en`) and Bengali (`bn`)
- CORS, JWT auth, and schema docs enabled by default.

### Next steps

See `docs/ROADMAP.md` for concrete integration steps (risk rules, commissions, AML/KYC, reconciliation flows, provider integrations, reports, and CMS content).
