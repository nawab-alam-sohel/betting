# Cleanup plan

This repository had multiple dashboards and scattered CMS-like code. The unified approach uses Jazzmin with the default Django admin. No custom admin dashboards/URLs are needed.

Planned/Completed steps:

- [x] Removed custom adminpanel URLs from `config/urls.py` to avoid duplicate admin dashboards.
- [x] CMS settings and content managed via model admins under the `cms` app (singleton settings models included).
- [x] Role-aware UserAdmin implemented (Super Admin/Admin/Agent/User).
- [ ] Identify and remove unused templates and dead routes under `apps/adminpanel/templates/admin/system/*`.
- [ ] Remove `apps/adminpanel/` if no longer needed, after verifying no other code depends on it.
- [ ] Remove legacy dashboard links from Jazzmin config (done) and code references.

Notes:
- Keep domain apps (wallets, bets, payments, sports, agents) intact.
- Future: consolidate API auth to session for admin widgets, or provide a service account token.
