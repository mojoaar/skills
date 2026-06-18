# Project Conventions

These apply regardless of the chosen stack. They ensure consistency across projects and between AI agent and human maintainers.

## Mandatory Meta-Documents

Every scaffolded project must include these files at the repository root:

| File          | Purpose                                               | Template content                              |
| ------------- | ----------------------------------------------------- | --------------------------------------------- |
| `README.md`   | Project overview, quick start, features, tech stack, shortcuts, changelog | Name, one-liner, version, license, install steps, key features |
| `AGENTS.md`   | Agent instructions: architecture, conventions, commands, gotchas, version bump checklist | Project overview, directory structure, API routes, keyboard shortcuts, env vars, key conventions |
| `plan.md`     | Implementation roadmap + execution steps, completed feature checklist | Tech stack table, project structure tree, DB schema, API routes, theme system, keyboard shortcuts, roadmap (v0.x) |
| `CHANGELOG.md` | Human-readable version history                       | Version headers with dates and bullet-point feature lists |
| `LICENSE`     | License file (MIT, AGPL-3.0, etc.)                    | Full license text per user choice             |
| `.gitignore`  | Git ignore rules                                      | `node_modules/`, `.next/`, `.env`, `*.log`, `public/uploads/`, test DB files |

### AGENTS.md Key Conventions Checklist

The AGENTS.md must include these sections — they are the contract between the human and AI:

1. **Quick Commands**: `npm run dev`, `npm run build`, `npm run test`, `npm run lint`, `npm run db:push`
2. **Releases & Git Tags**: Never create git tags or GitHub releases autonomously
3. **Version bump checklist**: List every file that contains the version string — when bumping, all must be updated
4. **Docs audit rule**: When user asks "is docs updated?", always check and update together: `/docs`, `/apidocs`, `README.md`, `AGENTS.md`, `plan.md`
5. **Database convention**: Run `npm run db:push` at start of every local dev session
6. **Build verification**: Always run `npm run build` after multi-file changes
7. **Todo completion**: Always mark todos as `completed` when done — never leave tasks dangling

## Project Structure Template

**Core pattern**: CSM (Core, Shared, Modules) — flat under `src/`, not deeply nested.

```
src/
├── app/
│   ├── layout.tsx              # Root layout: fonts, theme provider, metadata
│   ├── page.tsx                # Root page: session check → dashboard or landing
│   ├── globals.scss            # CSS variables, theme tokens, global styles, utility classes
│   ├── (auth)/                 # Auth route group (unauthenticated)
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   ├── forgot-password/page.tsx
│   │   └── verify-totp/page.tsx
│   ├── (dashboard)/            # Dashboard route group (authenticated)
│   │   ├── layout.tsx          # Sidebar + header + auth guard
│   │   └── dashboard/
│   │       ├── page.tsx        # Landing page after login
│   │       └── settings/page.tsx
│   └── api/                    # REST API route handlers
│       ├── auth/[...all]/route.ts
│       ├── profile/route.ts
│       └── ...
├── components/
│   ├── ui/                     # Reusable: Button, Input, Avatar, Toast, etc.
│   ├── theme/                  # ThemeProvider, ThemeToggle
│   └── landing/                # Landing page components (if applicable)
├── lib/
│   ├── auth.ts                 # Auth server config
│   ├── auth-client.ts         # Auth client config
│   ├── db/
│   │   ├── index.ts            # Database client singleton (hot-reload-safe)
│   │   └── schema.ts           # All table definitions
│   ├── email.ts                # Email transport (if auth with email)
│   ├── validations.ts          # Zod schemas for all API routes
│   ├── slug.ts                 # Slug generation utilities
│   └── crypto.ts               # Encryption utilities (if storing secrets)
├── hooks/                      # React hooks
└── __tests__/                  # Vitest tests
    ├── basic.test.ts           # Smoke test for package.json
    ├── validations.test.ts     # Zod schema tests
    └── components/             # Component tests
```

## Version Bump Checklist

When bumping the project version, all of these must be updated together:

1. `package.json` — `"version"` field
2. `AGENTS.md` — version in project overview
3. Settings page — About section version display
4. Landing page — version badge (if applicable)
5. `src/lib/webhooks.ts` — User-Agent header version (if webhooks exist)
6. `README.md` — version badge, changelog entry
7. `plan.md` — title + current version section
8. Test assertions — version check in `basic.test.ts` (if present)

## Source Control

- **Initialize git immediately** after creating the project directory
- **Commit after each major step** — not just at the end. This creates a clean history.
- **Conventional Commits**: `feat: add auth`, `fix: input border radius`, `chore: bump deps`
- **Push regularly** — at minimum after each work session
- `.gitignore` must include: `node_modules/`, `.next/`, `.env`, `.env.local`, `*.log`, `public/uploads/*`, `.DS_Store`
- `.DS_Store` (macOS directory metadata) must be in `.gitignore` and removed from tracked files

## Tagged Releases

**Never create git tags or GitHub releases autonomously.** Only the human triggers version tags. The agent:
- Can update version strings in all files (package.json, AGENTS.md, README.md, etc.)
- Can generate changelog entries
- Must NOT run `git tag` or create GitHub releases or modify the CHANGELOG heading order without explicit user instruction

## "Is Docs Updated?" Checklist

When the user asks "is docs updated?" or "update docs", check and update ALL of these together:

1. `/docs` pages — user-facing documentation
2. `/apidocs` — API reference page
3. `README.md` — project overview, features, tech stack, shortcuts, changelog
4. `AGENTS.md` — agent instructions, conventions, version bump checklist
5. `plan.md` — roadmap, completed features, future plans

Never update just one — they must stay in sync.

## Migration Strategy

| Approach                          | When to use                     | Risk level |
| --------------------------------- | ------------------------------- | ---------- |
| `drizzle-kit push`                | Development only                | Lossy      |
| `drizzle-kit generate` + `migrate` | Production deployments           | Safe       |

- `push` directly applies schema to DB — fast but can drop columns. Never use in production.
- `generate` creates SQL migration files in `./drizzle/`. Review them, commit them, then apply with `migrate`.
- Add to `package.json` scripts: `"db:push": "npx drizzle-kit push"` and `"db:migrate": "npx drizzle-kit generate && npx drizzle-kit migrate"`.
- Always run `db:push` at the start of every local dev session to sync schema changes.

## Build After Each Step

Run `npm run build` after every multi-file change, not just at the end. This catches TypeScript errors, missing imports, and broken configs early when the fix is obvious. If the build fails, fix it before continuing to the next step.

## API Response Shapes

All API routes should use one of these consistent shapes:

**Single resource**: `{ <resource>: { ... } }`
```json
{ "note": { "id": "...", "title": "Hello", "content": "# Markdown" } }
```

**List resource**: `{ <resources>: [ ... ] }`
```json
{ "notes": [{ "id": "...", "title": "Hello" }] }
```

**Paginated list**: `{ <resources>: [...], total: N, page: N, limit: N }`
```json
{ "notes": [...], "total": 42, "page": 1, "limit": 20 }
```

**Error**: `{ "error": "message" }` (never expose stack traces in production)
```json
{ "error": "Name is required" }
```

**Success without body**: Return 200/201 with `{ "ok": true }` or the created/updated resource.

### Hot-Reload Safety
Any long-lived resource (DB connection, event bus, pub/sub listener) must be cached on `globalThis` in development to survive Next.js hot module reloads. Example:

```typescript
const globalForX = globalThis as unknown as { instance?: MyType };
const instance = globalForX.instance ?? createInstance();
if (process.env.NODE_ENV !== "production") globalForX.instance = instance;
```

**Exception**: Auth config objects should NOT be cached on `globalThis` — stale config across reloads causes subtle bugs.

### API Response Pattern
All API routes should follow a consistent response shape:
- Success: `{ data: ... }` or `{ profile: ... }` or `{ workspace: ... }`
- Error: `{ error: "message" }`
- Paginated list: `{ data: [...], total: N, limit: N, offset: N }`

### Protection Checklist
Every API route should protect against:
1. **Unauthorized** (401): No valid session
2. **Not found** (404): Resource doesn't exist
3. **Forbidden** (403): Authenticated but not authorized (wrong workspace, wrong role)
4. **Bad request** (400): Invalid/missing input

### Side Effects in API Routes
Side effects (notifications, webhooks, audit logs) must be wrapped in try-catch so they never break the main response:

```typescript
try { await eventBus.notify(...); } catch {}
try { await triggerWebhooks(...); } catch {}
try { await logAction(...); } catch {}
```
