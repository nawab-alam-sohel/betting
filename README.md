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
