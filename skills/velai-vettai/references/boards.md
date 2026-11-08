# Job boards and sources

Configurable in `profile.json` (`boards`). Add any board the user names.

| Source | Notes |
|---|---|
| Naukri | Search title + location. "Apply on company site" redirects out: proceed. Direct "Apply": log as Naukri Direct Apply, skip. |
| LinkedIn | Jobs search with date filter. "Easy Apply" badge: log as LinkedIn Easy Apply, skip. Plain "Apply" opens the employer site: proceed. Use the user's own session; no volume scraping. |
| Himalayas | Remote-first, mostly external apply links. |
| Wellfound | Startups. If apply stays on Wellfound, log as Manual. |
| Others | Indeed, Instahyre, foundit, Cutshort, Hirist. Treat like the above. |

## Direct company scanning (`portals.yml`)

For target companies, scan the public ATS pages instead of the aggregator: Greenhouse (`boards.greenhouse.io/<co>` or its public JSON API), Lever (`jobs.lever.co/<co>`), Ashby (`jobs.ashbyhq.com/<co>`), Workday career sites. These show accurate posting dates and skip the redirect step. See `portals.example.yml`.

General: use "posted in last N days" filters, then still verify the date on the career page. Respect site terms and rate limits; stop on bot checks.
