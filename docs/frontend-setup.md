# VelkiList Frontend Setup (Next.js 14, TypeScript)

This guide sets up a companion frontend app to consume the VelkiList backend APIs.

## Why Next.js 14
- SSR + SEO for sportsbook/casino pages
- App Router with layouts and nested routing
- Great DX with TypeScript, Tailwind, and shadcn/ui

## Project folder
Create a sibling folder next to `velkilist-backend` named `velkilist-frontend`.

## Prerequisites
- Node.js 18+
- pnpm or npm (examples below use `pnpm`)

## Create the app
```powershell
cd F:\VelkiList
pnpm create next-app velkilist-frontend --ts --eslint --app --src-dir --tailwind --use-pnpm --import-alias "@/*"
```
When prompted, you can accept defaults.

## Install UI and utilities
```powershell
cd F:\VelkiList\velkilist-frontend
# shadcn/ui
pnpm dlx shadcn-ui@latest init
pnpm add next-intl @tanstack/react-query zod axios clsx tailwind-merge
```

## Env configuration
Create `.env.local` in `velkilist-frontend`:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_DEFAULT_LOCALE=en
NEXT_PUBLIC_SUPPORTED_LOCALES=en,bn
```

## Project structure (key folders)
```
velkilist-frontend/
  app/
    (marketing)/          # CMS landing pages
    (sports)/             # Sportsbook
    (casino)/             # Casino
    api/                  # server actions / fetch helpers
    layout.tsx
    page.tsx
  components/
  lib/
  styles/
```

## Data fetching helper
Create `app/api/client.ts`:
```ts
export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "";

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
    cache: 'no-store',
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json();
}
```

## First pages
- Sportsbook Home (upcoming): GET `/api/sports/games/upcoming/`
- Sports Categories: GET `/api/sports/categories/`
- Leagues by category: GET `/api/sports/leagues?category=<id>`
- Game detail: GET `/api/sports/markets/?game=<id>`
- Betslip validation: POST `/api/sports/validate-betslip/`

- Casino Providers: GET `/api/casino/providers/`
- Casino Categories: GET `/api/casino/categories/`
- Casino Games: GET `/api/casino/games/?category=<id>` or `?az=A`
- Launch session: POST `/api/casino/launch/` (body: { game_id, user_id? })

## i18n
Use `next-intl` with `en` and `bn`. Set up middleware and locale segments for `/en/*` and `/bn/*`.

## Styling
Tailwind + shadcn/ui for design system and consistent components.

## Next steps
- Auth: JWT login/register screens; store access token; add Authorization headers
- Wallet: show balance; transactions list
- Betslip: client-side state; call validation endpoint
- Casino: open `launch_url` in new tab or iframe
- CMS: fetch site settings and page content by slug

## Troubleshooting
- Ensure backend is running at http://localhost:8000 and CORS allows your frontend origin.
- In backend `.env`, set `CORS_ALLOWED_ORIGINS=http://localhost:3000`.
