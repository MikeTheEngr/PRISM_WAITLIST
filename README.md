# PRISM — Waitlist Landing Page

AI-powered predictive intelligence across crypto and stocks.
*"Your unfair advantage in every market."*

## Structure

```
prism-waitlist/
├── index.html          # The full landing page (HTML/CSS/JS, Three.js background)
├── public/
│   ├── favicon.svg     # PRISM mark favicon
│   └── og-image.png    # Social share preview (ADD THIS — 1200x630px)
├── vercel.json          # Deployment config
└── README.md
```

## Deploy to Vercel

### Option A — Vercel CLI (fastest)
```bash
npm i -g vercel
cd prism-waitlist
vercel
```
Follow the prompts. It auto-detects this as a static site — no build step needed.

### Option B — GitHub + Vercel dashboard
1. Push this folder to a new GitHub repo
2. Go to vercel.com → New Project → Import the repo
3. Framework preset: **Other** (no build command needed)
4. Deploy

## Before going live

- [ ] Create `public/og-image.png` (1200×630px) — used for social share previews on X/LinkedIn
- [ ] Connect a custom domain (e.g. prism.yourname.com or prismai.app) in Vercel project settings
- [ ] Waitlist form currently shows a fake success message — wire it to the real backend (see Phase 2 below)

## Next: Backend (waitlist storage)

The waitlist form is currently front-end only — emails aren't saved anywhere yet.
Next step: a small FastAPI service + Supabase table to actually capture submissions.
This will be built as a separate service and the form's `fetch()` call will point to it.

## Brand Reference

- **Colors:** `#0E0B12` (dark bg) · `#F5F4F8` (light bg) · `#7C3AED` → `#06B6D4` → `#10B981` (spectrum gradient)
- **Fonts:** Space Grotesk (display) · Inter (body) · JetBrains Mono (data/numbers)
- **Tagline:** "Your unfair advantage in every market."
