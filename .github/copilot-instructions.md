This file helps AI coding agents be productive in this Django project. Keep it short and specific.

- Project root: `f:/VelkiList/velkilist-backend` — Django 5.2 project in `config/` with a single local app `apps.users`.
- Purpose: REST API for user management using DRF + SimpleJWT. Models: custom `User` (`AUTH_USER_MODEL = 'users.User'`) and `Role`.

Key files and what they do:
- `config/settings.py` — DB via environment variables, `jazzmin` admin theme enabled, JWT config in `SIMPLE_JWT`.
- `apps/users/models.py` — custom user model (email as `USERNAME_FIELD`), `Role` model (FK on User).
- `apps/users/admin.py` — custom admin for `User` and `Role` (ordering uses `email`).
- `apps/users/api/serializers.py` — serializers for register, login, profile, password change/reset (note: serializer name is `ResetPasswordSerializer`).
- `apps/users/api/views.py` — API views (use `ResetPasswordView` for password reset endpoint).
- `apps/users/api/urls.py` — routes for register/login/logout/profile/password reset, token refresh.

Developer workflows (commands you’ll need):
- Docker compose up/build: `docker compose up --build` (from project root). Remove `version` from `docker-compose.yml` if present.
- Migrations: `docker compose exec web python manage.py makemigrations` then `docker compose exec web python manage.py migrate`.
- Run tests: `docker compose exec web python manage.py test`.
- Shell access: `docker compose exec web python manage.py shell`.

Conventions & gotchas discovered:
- Custom user uses `email` as the username field — admin ordering/search should reference `email` not `username`.
- Password reset serializer is named `ResetPasswordSerializer` (views import this name). Keep imports consistent.
- `docker-compose.yml` previously used obsolete `version` key — remove it to avoid warnings.
- Settings rely on `.env` — ensure `.env` has DB variables (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT) and SECRET_KEY.

If editing: prefer small, focused commits. Run `makemigrations` after model changes and `migrate` before running the server.

When asked to modify code, prefer to:
- Run `get_errors`/`python manage.py check` to surface Django issues.
- Search for exact symbol names before renaming (e.g., `PasswordResetSerializer` vs `ResetPasswordSerializer`).

Examples of useful PR checks for AI agents:
- Did tests pass? `python manage.py test`.
- Any unresolved imports or system check errors? `python manage.py check`.
- DB migrations created when models changed? `makemigrations` output should list changed apps.
