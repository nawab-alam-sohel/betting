# VelkiList Frontend (Next.js 14)

This is a fresh Next.js 14 + TypeScript + Tailwind frontend for your Django backend.

Important: We cannot copy 1xBet "same-to-same" proprietary design due to copyright. Instead, this UI uses a similar modern, dark, sports-betting aesthetic and connects to your real APIs.

## Quick start (Docker)

- Ensure the backend is running at http://localhost:8000 and CORS allows `http://localhost:3000`.
- From the backend root (`velkilist-backend`), run:

```
docker compose up frontend -d
```

The app runs at http://localhost:3000.

## Local (Node.js)

- Install Node 20+.
- In `velkilist-frontend/`:

```
npm install
npm run dev
```

## Environment

Create `.env.local` in `velkilist-frontend/`:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Pages included

- `/` — Upcoming games (reads `/api/sports/games/upcoming/`)
- `/login` — JWT login via `/api/users/token/`
- Header links for Sports and Casino (placeholders to expand)

## Next steps

- Build Sports and Casino sections using endpoints in `docs/frontend-setup.md`.
- Add auth state, profile, wallet, and bet placement flows.
- Polish styling with Tailwind components (do not copy 1xBet assets or layouts exactly).
