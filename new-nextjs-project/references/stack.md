# Dependency Stack Reference

**Core rule**: Never hardcode versions. Before every `npm install`, verify the latest stable version with `npm info <package> version`.

## Universal Foundation (always required)

| Package      | Purpose                  | Install as |
| ------------ | ------------------------ | ---------- |
| `next`       | Framework (App Router)   | dependency |
| `react`      | UI library               | dependency |
| `react-dom`  | React DOM renderer       | dependency |
| `typescript` | Type checking            | dependency |
| `@types/node` | Node.js type defs       | devDependency |
| `@types/react` | React type defs        | devDependency |
| `@types/react-dom` | React DOM type defs | devDependency |

## Category Comparison Tables

For each category, pick ONE option. The interview in SKILL.md asks the user to choose.

### Styling

| Option       | Package            | Pros                              | Cons                              | When to pick                                |
| ------------ | ------------------ | --------------------------------- | --------------------------------- | ------------------------------------------- |
| Sass/SCSS    | `sass`             | No new tooling, CSS var friendly, `.module.scss` scoping | Manual design tokens, no utility classes | Design system with custom properties, theme-heavy apps |
| Tailwind     | `tailwindcss`, `@tailwindcss/postcss` | Utility-first speed, consistent spacing, huge ecosystem | Opinionated, longer class strings, PostCSS dependency | Rapid prototyping, component libraries, design-agnostic |
| CSS Modules  | (built into Next.js) | Zero-config, scoped by default, plain CSS | No preprocessor features, verbose for complex selectors | Simple projects that don't need preprocessing |
| styled-components | `styled-components` | Dynamic styling based on props, co-located styles | Runtime overhead, bundle size, separate Babel plugin (optional) | Dynamic/theme-driven component styling |

### Database + ORM

| Option              | Packages                            | Pros                                      | Cons                                      | When to pick                          |
| ------------------- | ----------------------------------- | ----------------------------------------- | ----------------------------------------- | ------------------------------------- |
| PostgreSQL + Drizzle | `postgres`, `drizzle-orm`, `drizzle-kit` (dev) | Type-safe queries, SQL-like syntax, lightweight, native PG driver | Newer ORM, smaller ecosystem, manual migration names | TypeScript-first projects, self-hosted |
| SQLite + Drizzle    | `better-sqlite3`, `drizzle-orm`, `drizzle-kit` (dev), `@types/better-sqlite3` (dev) | Zero config, single file, fast local dev, WAL mode | Not for multi-server deployments, write concurrency limits | Local-first, edge, small teams, dev prototyping |
| PostgreSQL + Prisma | `@prisma/client`, `prisma` (dev)    | Mature, auto-migrations, great Studio UI, large ecosystem | Heavier, generated client, migration lock-in, connection management complexity | Teams that prefer Prisma Studio + schema-first workflow |
| None                | —                                   | No DB complexity                           | No persistence                            | Static sites, blogs, API-only proxies |

**Drizzle gotcha**: The npm package is `postgres` (lowercase), not `pg`. The Drizzle adapter is `drizzle-orm/postgres-js`. Do not install `pg`.

**SQLite gotcha**: WAL mode requires `pool: { min: 1, max: 1 }` to avoid stale reads. Set `fileParallelism: false` in Vitest config.

**Prisma gotcha**: `prisma generate` must run after schema changes and before `npm run build` in CI.

### Authentication

| Option      | Packages                                          | Pros                                          | Cons                                          | When to pick                               |
| ----------- | ------------------------------------------------- | --------------------------------------------- | --------------------------------------------- | ------------------------------------------ |
| Better Auth | `better-auth`, `@better-auth/drizzle-adapter` (if Drizzle) | Modern, plugin-rich (TOTP, admin, SSO), good docs, TypeScript native | Newer framework, plugins add complexity | Self-hosted, TOTP MFA, plugin-heavy apps |
| NextAuth v5 | `next-auth@beta`, `@auth/drizzle-adapter` (if Drizzle) | Most popular, huge ecosystem, many providers, battle-tested | v5 still beta, complex config, abstracted | OAuth-heavy (Google, GitHub), established teams |
| Clerk       | `@clerk/nextjs`                                   | Hosted, no auth code to write, beautiful components, webhooks | Vendor lock-in, cost at scale, not self-hosted | Quick setup, don't want to own auth infrastructure |
| None        | —                                                 | No dependencies, simplest                    | No auth, public-only                         | Marketing sites, blogs, internal tools behind VPN |

**Auth cookie gotcha**: On HTTPS, auth libraries prefix cookies with `__Secure-`. Any cookie-checking code (middleware, proxy) must check BOTH `{cookie_name}` AND `__Secure-{cookie_name}`.

**Auth redirect gotcha**: After sign-in, use `window.location.href = "/dashboard"` — not `router.push()`. Client-side navigation doesn't send the newly set cookie, causing infinite redirect loops.

### Realtime

| Option              | Packages    | Pros                                          | Cons                                          | When to pick                          |
| ------------------- | ----------- | --------------------------------------------- | --------------------------------------------- | ------------------------------------- |
| SSE + PG NOTIFY     | none (uses `postgres` driver) | Zero deps, cross-process, auto-reconnect in browser, works in Next.js App Router | One-directional (server→client only), no back-pressure | Presence, live updates, multi-tab sync |
| WebSockets + Yjs    | `yjs`, `y-protocols` | True collaborative editing, CRDT conflict resolution, cursor sync | Complex, requires custom server or separate process, heavier | Google Docs-style co-authoring, realtime editors |
| None                | —         | Simplest, no server overhead                  | No live updates                               | CRUD apps, content sites, async-first apps |

### Testing

| Option | Packages                                                          | Pros                                      | Cons                                      | When to pick                         |
| ------ | ----------------------------------------------------------------- | ----------------------------------------- | ----------------------------------------- | ------------------------------------ |
| Vitest | `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `@testing-library/user-event`, `jsdom` | Fast, Vite-native, Jest-compatible, ESM-first | Smaller ecosystem than Jest               | Always (recommended over Jest for new projects) |
| Jest   | `jest`, `ts-jest`, `@testing-library/*`                          | Largest ecosystem, huge community, battle-tested | Slower, CJS legacy, complex config        | Teams with deep Jest investment     |
| None   | —                                                                 | No test overhead                           | No test safety net                         | Prototypes, throwaway projects       |

### Deployment

| Option            | Files needed                   | Pros                                    | Cons                                    | When to pick                          |
| ----------------- | ------------------------------ | --------------------------------------- | --------------------------------------- | ------------------------------------- |
| Docker Compose    | `Dockerfile`, `docker-compose.yml` | Reproducible, includes DB, self-contained | Docker knowledge needed, image build time | Self-hosted on VPS/Proxmox |
| Docker + systemd | `Dockerfile`, `.service` unit file | Native process management, auto-restart | Manual Docker restart on crash, systemd syntax | Self-hosted with existing systemd infrastructure |
| Vercel            | none (platform-native)         | Zero-config deploy, edge functions, analytics | Vendor lock-in, cost at scale, no persistent DB | SaaS, startups, rapid iteration |
| None              | —                              | No deployment infra needed              | No production deployment                  | Dev-only, portfolio projects          |

### Icons (optional, pick one)

| Package        | Install as   | Notes                              |
| -------------- | ------------ | ---------------------------------- |
| `lucide-react` | dependency   | 400+ icons, tree-shakeable, recommended |
| `react-icons`  | dependency   | 10+ icon sets (FontAwesome, Material, etc.), larger bundle |

### Markdown & Syntax (optional)

| Package         | Install as   | Notes                                           |
| --------------- | ------------ | ----------------------------------------------- |
| `prismjs`       | dependency   | Syntax highlighting (297 languages via autoloader) |
| `@types/prismjs` | devDependency | Type definitions for Prism                     |

### Validation (optional)

| Package | Install as | Notes                                     |
| ------- | ---------- | ----------------------------------------- |
| `zod`   | dependency | Schema validation, recommended for all API routes |

### Email (optional, auth-dependent)

| Package            | Install as   | Notes                                    |
| ------------------ | ------------ | ---------------------------------------- |
| `nodemailer`       | dependency   | SMTP email sending                      |
| `@types/nodemailer` | devDependency | Type definitions for Nodemailer          |

## Check Maintenance Status

Before installing any package, verify it's actively maintained:

```bash
npm info <package> time --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
versions = [(v, t) for v, t in data.items() if v != 'created' and v != 'modified']
latest = max(versions, key=lambda x: x[1])
print(f'{latest[0]} ({latest[1][:10]})')
"
```

Flag any package whose last publish was over 12 months ago.
