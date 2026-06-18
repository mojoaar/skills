---
name: new-nextjs-project
description: Scaffold a new full-stack Next.js project. Use when the user wants to start a new web application, SaaS, self-hosted tool, admin panel, API backend, blog, marketing site, or asks "how do I build a new app." This skill interviews about project type (SaaS/self-hosted/admin/blog/API/etc.), then presents multi-choice options for each stack layer (auth, database, styling, realtime, testing, deployment) with tradeoffs — it does not assume any single stack. Always use when someone says "create a new Next.js app," "scaffold a project," or asks to start a new TypeScript web application from scratch.
---

# New Next.js Project

You scaffold full-stack Next.js projects from scratch. Your job is to interview the user about their project type and stack preferences, then scaffold everything in dependency order with the latest stable packages.

## Core Rules

1. **Never hardcode package versions.** Resolve latest stable: `npm info <package> version`. Use exact versions in `package.json`.
2. **Check maintenance status.** Flag packages with last publish >12 months ago. Suggest alternatives.
3. **Scaffold in dependency order.** DB before auth, auth before UI, UI before features. Build after each major step.
4. **Stay in Plan Mode for the interview.** Ask all questions, present the full plan in a table, get explicit confirmation, then execute.
5. **Commit after each step.** `git add -A && git commit -m "feat: <step>"` — not just at the end. Push regularly.
6. **Never tag or release.** The user controls version tags and GitHub releases. Update version strings, but never run `git tag` or create releases.
7. **Docs audit rule.** When asked "is docs updated?", always check and update together: `/docs`, `/apidocs`, `README.md`, `AGENTS.md`, `plan.md`.

## Phase 0: Interview

Ask these questions in order. Defaults are shown in bold — the user can override any. Skip categories irrelevant to the project type.

### 1. Project Identity

- **Name**: lowercase-kebab-case (e.g. `"mindmatrix"`)
- **Tagline**: one-liner elevator pitch
- **Description**: 2-3 sentences — what, who, why

These flow into `package.json`, Next.js metadata, README, AGENTS.md, and the landing page.

### 2. Project Type

| Type               | Auth | Database | Realtime | Typical deploy     |
| ------------------ | :--: | :------: | :------: | ------------------ |
| SaaS               | Yes  | Yes      | Optional | Docker / Vercel    |
| Self-hosted tool   | Yes  | Yes      | Optional | Docker + systemd   |
| Admin panel        | Yes  | Yes      | No       | Docker             |
| API-only backend   | Yes  | Yes      | No       | Docker / Vercel    |
| Blog / content site| No   | Optional | No       | Vercel / static     |
| Marketing site     | No   | No       | No       | Vercel / static     |
| E-commerce         | Yes  | Yes      | No       | Docker / Vercel    |
| CLI companion      | No   | Optional | No       | N/A                |

This determines which interview steps to show. Auth is auto-skipped for blogs and marketing sites. Database is auto-skipped unless CRUD is needed. Realtime is only offered if database is selected.

### 3. License

- **AGPL-3.0 (Recommended for self-hosted)** — copyleft
- MIT — permissive
- Apache 2.0 — permissive with patent grant
- Proprietary / None

### 4. Source Control

- Provider: **GitHub** / GitLab / None
- Repo URL (can be created later)
- Branch strategy: **main only** / main + develop
- Commit convention: **Conventional Commits** (`feat:`, `fix:`, `chore:`)

### 5. Versioning

- **SemVer starting at 0.1.0** (pre-release phase)
- Generate `CHANGELOG.md` with initial entry
- Embed version bump checklist in AGENTS.md

### 6. Authentication (skip if Project Type doesn't need it)

| Option       | Description                                                                 |
| ------------ | --------------------------------------------------------------------------- |
| **Better Auth v1** | Email/password, email verification, password reset, TOTP 2FA, proxy middleware, super admin auto-promotion. Self-hosted, no recurring cost. |
| NextAuth v5  | Wide provider support (Google, GitHub, etc.). Easier OAuth, but more complex self-hosted setup with database. |
| Clerk        | Managed auth, zero-config, $0 up to 10K MAU. Best for SaaS that ships fast. Not self-hosted. |
| None         | Skip auth entirely.                                                            |

### 7. Database (skip if Project Type doesn't need it)

| Option                      | Description                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| **PostgreSQL + Drizzle ORM**| Docker Compose for dev, type-safe queries, push-based migrations. Proven in production. |
| PostgreSQL + Prisma         | More abstraction, declarative schema, migration tool built in. Heavier ORM. |
| SQLite + Drizzle            | Zero-config, file-based, great for single-server apps. No Docker needed.    |
| None                        | Skip database. Only static pages or external APIs.                           |

### 8. Styling

| Option                       | Description                                                                 |
| ---------------------------- | --------------------------------------------------------------------------- |
| **Sass/SCSS + CSS Variables**| Design system with custom properties, theme-ready, no build-time CSS generation. |
| Tailwind CSS                 | Utility-first, rapid prototyping, large community. Requires PostCSS config. |
| CSS Modules                  | Built into Next.js, zero-config, component-scoped styles.                   |
| styled-components            | CSS-in-JS, dynamic styles based on props. Requires `styled-components` package. |

### 9. Realtime (only if Database is chosen; skip otherwise)

| Option                        | Description                                                                 |
| ----------------------------- | --------------------------------------------------------------------------- |
| None                          | Standard request/response.                                                  |
| **SSE + PG NOTIFY (zero deps)**| Server-to-client push, presence tracking, EventSource API. No new packages. |
| WebSockets + Yjs (CRDT)       | Collaborative editing, cursor sync. Requires `yjs`, `y-protocols`. Complex. |

### 10. Testing

| Option        | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| **Vitest**    | Fast, Vite-native, jsdom environment. Recommended for all projects.         |
| Jest          | Mature ecosystem, slower startup. Choose if team already uses Jest.         |
| None          | Skip test scaffolding.                                                      |

### 11. Deployment (only for self-hosted / SaaS / admin)

| Option              | Description                                                                 |
| ------------------- | --------------------------------------------------------------------------- |
| **Docker + systemd**| Multi-stage Dockerfile, docker-compose.yml (PostgreSQL 17), systemd unit.   |
| Docker only         | Dockerfile + docker-compose, no systemd.                                    |
| Vercel              | Zero-config, Git-push deploy. Not for self-hosted PostgreSQL.                |
| None                | Skip deployment config.                                                     |

## Phase 1: Confirm Plan

Present a summary table after all questions:

```
## Project Plan: <name>

| Aspect         | Choice              |
| -------------- | ------------------- |
| Type           | Self-hosted tool    |
| License        | AGPL-3.0            |
| Source control | GitHub              |
| Version        | 0.1.0, SemVer       |
| Auth           | Better Auth v1      |
| Database       | PostgreSQL + Drizzle|
| Styling        | Sass/SCSS           |
| Realtime       | SSE + PG NOTIFY     |
| Testing        | Vitest              |
| Deployment     | Docker + systemd    |

**Files to create:** <N> files across <N> directories
**Scaffold order:** Meta docs → Foundation deps → DB → Auth → Theme → UI → Features → Tests → Deploy

Shall I proceed?
```

Wait for explicit confirmation before executing.

## Phase 2: Scaffold Execution

Execute in exact order. Build after each major step. If a step fails, fix it before moving on.

### Step 1: Meta Documents

1. `git init` (unless already in a repo)
2. `.gitignore` — Node.js + Next.js patterns: `node_modules`, `.next`, `.env`, `.env.local`, `public/uploads/*`
3. `LICENSE` — chosen license full text
4. `package.json` — `name`, `version` (0.1.0), `private: true`, `license`
5. `README.md` — name, tagline, description, version, license, tech stack table, features, quick start, shortcuts, changelog
6. `AGENTS.md` — project overview, tech stack, structure, conventions, commands, env vars, API routes, version bump checklist
7. `plan.md` — name, description, tech stack, project structure, schema, API routes, theme system, execution steps, roadmap
8. `CHANGELOG.md` — initial version entry
9. `git add -A && git commit -m "chore: scaffold project meta documents"`

Read `references/conventions.md` for exact AGENTS.md and version bump checklist structure.

### Step 2: Foundation Dependencies

Read `references/stacks.md` for the dependency catalog. Install in order:

1. `next react react-dom typescript`
2. Styling packages (if chosen): `sass` / `tailwindcss postcss autoprefixer` / none
3. `@types/node @types/react @types/react-dom`

Resolve latest versions first: `npm info <pkg> version`. Run `npm run build` after install.

### Step 3: Next.js Scaffold

1. `tsconfig.json` — strict mode, path aliases `@/*` → `./src/*`
2. `next.config.ts` — basic config. Add `output: "standalone"` if Docker chosen.
3. `src/app/layout.tsx` — root layout with metadata (title template, description, OG/Twitter, icons)
4. `src/app/page.tsx` — home page. If auth chosen: server component checks session → redirects to `/dashboard` or shows landing. If no auth: welcome page.
5. Load fonts via `next/font/google` (at minimum JetBrains Mono)
6. Add inline `<Script>` before interactive for theme + font initialization from localStorage
7. `npm run build` — must pass

### Step 4: Global Styles

Create `src/app/globals.scss` (or Tailwind config if chosen):

- CSS custom properties for base themes (`data-theme` attribute selectors)
- `data-font` attribute selectors for font stacks
- Utility classes: `.btn` (primary/secondary/danger/ghost + sm), `.card`, `.form-group`, `.badge`, `.table-wrapper`
- Form element reset: `input, select, textarea { font-family: inherit; font-size: inherit; border-radius: var(--border-radius); }`
- Scrollbar styles
- `npm run build && git add -A && git commit -m "feat: add global styles"`

### Step 5: Database (if chosen)

1. Install DB packages (resolve latest): `drizzle-orm drizzle-kit` + driver (`postgres` or `better-sqlite3`)
2. `.env.example` with `DATABASE_URL`
3. `deploy/docker-compose.yml` — PostgreSQL 17 service (only if PostgreSQL)
4. `src/lib/db/schema.ts` — auth tables (user, session, account, verification, twoFactor) + app tables
5. `src/lib/db/index.ts` — client with hot-reload-safe `globalThis` singleton
6. `drizzle.config.ts` at project root
7. Add scripts: `"db:push": "npx drizzle-kit push"`, `"db:migrate": "npx drizzle-kit generate && npx drizzle-kit migrate"`
8. **Migration strategy**: Use `db:push` for dev (fast, lossy). Use `generate` + `migrate` for production (creates auditable SQL files). Run `db:push` at the start of every local dev session.
9. `npm run build`

### Step 6: Auth (if chosen)

1. Install auth package + adapters
2. `src/lib/auth.ts` — server config with email/password, optional emailVerification, optional twoFactor, additionalFields, databaseHooks
3. `src/lib/auth-client.ts` — client config with plugins
4. `src/app/api/auth/[...all]/route.ts` — handler
5. `src/lib/email.ts` — nodemailer transport with dev console logger fallback
6. Auth pages: `login/page.tsx`, `register/page.tsx`, optional `forgot-password/page.tsx`, `reset-password/page.tsx`, `verify-totp/page.tsx`
7. `src/proxy.ts` — proxy middleware checking session cookies
8. If super admin: `role` field on user, first-user auto-promotion hook, admin API + dashboard
9. `npm run build && git add -A && git commit -m "feat: add authentication"`

### Step 7: Theme + Font System

1. `src/components/theme/theme-provider.tsx` — client context, `data-theme` DOM sync, localStorage
2. Load developer fonts in root layout via `next/font/google`
3. `src/components/ui/theme-toggle.tsx` — Sun/Moon toggle swapping `-dark`/`-light` suffix
4. `npm run build && git add -A && git commit -m "feat: add theme and font system"`

### Step 8: UI Components

1. `lucide-react` — icons
2. `src/components/ui/avatar.tsx` — initials fallback with color from name hash
3. `src/components/ui/toast.tsx` — Radix toast with context provider
4. `@radix-ui/react-toast @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-tooltip`
5. `npm run build && git add -A && git commit -m "feat: add UI components"`

### Step 9: Feature Scaffolding

Project-specific. General patterns:
- CRUD resources: `src/app/api/<resource>/route.ts` + `[id]/route.ts`
- Auth guard on every route: `auth.api.getSession()`
- `src/lib/validations.ts` — Zod schemas
- `src/lib/slug.ts` — `toSlug()`, `ensureUniqueSlug()`, `generateShortHash()`

### Step 10: Realtime (if chosen)

SSE + PG NOTIFY path:
1. `src/lib/realtime/event-bus.ts` — singleton wrapping `sql.listen()` / `sql.notify()`
2. `src/app/api/<resource>/[id]/events/route.ts` — SSE endpoint
3. `src/app/api/<resource>/[id]/presence/route.ts` — heartbeat POST + viewers GET
4. `src/hooks/use-realtime-<resource>.ts` — EventSource + heartbeat hook

WebSockets + Yjs path:
1. Install `yjs y-protocols`
2. `src/app/api/<resource>/[id]/delta/route.ts` — POST binary updates, broadcast via event-bus
3. Client-side Yjs doc + CodeMirror binding, 5-second debounced auto-save

### Step 11: Tests (if chosen)

1. `vitest @testing-library/react @testing-library/jest-dom` — install
2. `vitest.config.ts` — jsdom, path aliases, setup file
3. `src/__tests__/setup.ts`
4. Example tests: validations, slug utilities, a component

### Step 12: Deployment (if chosen)

1. `deploy/Dockerfile` — multi-stage Node 22 Alpine
2. `deploy/docker-compose.yml` — app + PostgreSQL 17 + volumes + health checks
3. `deploy/<app-name>.service` — systemd unit template

### Step 13: Final Verification

1. `npm run build` — zero errors
2. `npm run test` — all pass (if testing chosen)
3. `npm run db:push` — schema syncs (if database, requires DB running)
4. Print summary with next steps

## Reference Files

Read these at the start of the relevant step — not all at once:

| File                          | When to read                            |
| ----------------------------- | --------------------------------------- |
| `references/stacks.md`        | Step 2 — dependency catalog + tradeoffs |
| `references/conventions.md`   | Step 1 — meta-document structure        |
| `references/gotchas.md`       | Any step — common pitfalls              |
