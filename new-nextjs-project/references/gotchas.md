# Common Pitfalls & Gotchas

These are real bugs and issues encountered during full-stack Next.js project deployments. Each represents hours of debugging. Read this before scaffolding any feature.

## React & Next.js

### 1. Strict Mode Double Mounts
React Strict Mode mounts every component twice in development to detect side effects. This causes double API calls, double connections, and double effects. It only happens in dev, not production.

**Prevention**: Use cleanup functions in `useEffect`, and don't assume effects run exactly once.

### 2. Stale Closures in Callback Handlers
When a function references state or props that change, the closure captures the value at definition time, not call time.

**Example**: A save handler in a dropdown that captures `folderId` from state. If the user changes folder and saves before the re-render, the old `folderId` is sent.

**Fix**: Pass current values as explicit parameters rather than relying on state:
```typescript
async function save(overrides?: { folderId?: string }) {
  const finalFolderId = overrides?.folderId ?? currentFolderId;
  // ...
}
```

### 3. `beforeunload` SendBeacon for Unsaved Work
When the user closes the tab with unsaved work, `fetch()` in a synchronous `beforeunload` handler won't execute. Use `navigator.sendBeacon()` instead — it's fire-and-forget and guaranteed to complete:

```typescript
window.addEventListener("beforeunload", () => {
  if (hasUnsavedChanges) {
    const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
    navigator.sendBeacon("/api/save", blob);
  }
});
```

## Database

### 4. PostgreSQL B-Tree Index 8191 Byte Limit
Standard b-tree indexes have a maximum row size of 8191 bytes. Including large `text` or `varchar` columns in an index will cause writes to fail with a 500 error:

```
index row requires 8880 bytes, maximum size is 8191
```

**Fix**: Only index short columns (title, slug, status). Never index `content`, `body`, or unbounded text fields.

### 5. Self-Referencing Relations Need Matching `relationName`
When a table references itself (e.g., folder parent → folder children), both the `one` and `many` sides must use identical `relationName`:

```typescript
parent: one(folder, { fields: [...], references: [...], relationName: "children" }),
children: many(folder, { relationName: "children" }),
```

Without this, Drizzle throws: `infer relation "folder.children"` error.

### 6. Hot-Reload Singleton on `globalThis`
In Next.js dev mode, every file save triggers a hot module reload. If you create a new database connection on every reload, you'll exhaust PostgreSQL connections in minutes.

```typescript
const globalForDb = globalThis as unknown as { conn: ReturnType<typeof postgres> | undefined };
const conn = globalForDb.conn ?? postgres(url, { max: 10 });
if (process.env.NODE_ENV !== "production") globalForDb.conn = conn;
```

Cache the connection pool (db, sql), NOT config objects (auth).

### 7. `postgres` Driver, Not `pg`
The npm package is `postgres` (lowercase). The import is `import postgres from "postgres"`. Drizzle's adapter is `drizzle-orm/postgres-js`. Do not install the `pg` package — it's a different driver with different API.

## Authentication

### 8. `__Secure-` Cookie Prefix on HTTPS
Better Auth automatically prefixes session cookies with `__Secure-` when `BETTER_AUTH_URL` uses `https://`. Any cookie-parsing code (middleware, proxy, route handlers) must check BOTH names:

```typescript
cookies["better-auth.session_token"] ||
cookies["__Secure-better-auth.session_token"]
```

### 9. `additionalFields` Must Match Schema
Columns that exist in the Drizzle `user` table but NOT in Better Auth's `user.additionalFields` are invisible to `auth.api.getSession()`. This causes subtle bugs where `session.user.image` is `undefined` even though the database has it.

**Fix**: Add all user-facing columns to `additionalFields`:
```typescript
user: {
  additionalFields: {
    role: { type: "string", required: false, defaultValue: "user" },
    image: { type: "string", required: false },
    timezone: { type: "string", required: false, defaultValue: "browser" },
    timeFormat: { type: "string", required: false, defaultValue: "browser" },
    twoFactorEnabled: { type: "boolean", required: false, defaultValue: false },
  },
},
```

### 10. `window.location.href` for Auth Redirects
After sign-in, the session cookie is set by the server's response. If you use `router.push()` (client-side navigation), the browser doesn't send the cookie, and the middleware sees an unauthenticated user. Use full page navigation:

```typescript
window.location.href = "/dashboard";
```

### 11. 422 on Unverified Email Is Not Failure
Better Auth returns HTTP 422 with a valid `token` and `user` object when the user hasn't verified their email. The login technically succeeds — the session IS created. Handle 422 by checking `response.ok` and showing a "Check your email" message rather than an error.

### 12. Don't Cache Auth on globalThis
Unlike database connections, the Better Auth config object should NOT be cached on `globalThis`. In dev, the module may persist across hot reloads with stale config. Always create a fresh `betterAuth(...)` instance.

### 13. Auth Pages Whitelist in Proxy
If using middleware or proxy to guard dashboard routes, explicitly exclude all auth pages:
```
/login, /register, /forgot-password, /reset-password, /verify-totp
```

If the proxy redirects `/verify-totp` to `/login`, users get stuck in a redirect loop after enabling 2FA.

## Browser & UI

### 14. Favicon Cache-Busting
Safari and Webkit browsers aggressively cache favicons, sometimes indefinitely. After changing the favicon, append a version query parameter:

```typescript
icons: {
  icon: [
    { url: "/icon.svg?v=2", type: "image/svg+xml" },
  ],
}
```

Increment `v` on every favicon change.

### 15. Avatar Upload Cache-Busting
If avatars are stored as `{userId}.{ext}`, browsers cache the old image by URL. Append a timestamp to the filename:

```typescript
const filename = `${userId}_${Date.now()}.${ext}`;
```

Or store with a random suffix to force cache invalidation on every upload.

### 16. `<kbd>` Styling
Keyboard shortcut display in UI needs explicit styling — browsers don't have default kbd styles:

```css
kbd {
  padding: 0 0.25rem;
  border-radius: 3px;
  background-color: var(--bg-tertiary);
  font-size: 0.65rem;
  font-weight: 600;
}
```

### 17. SVG `stop-color` → `stopColor` in JSX
React JSX uses camelCase for SVG attributes in client components:

```jsx
// CORRECT
<stop offset="0%" stopColor="#abc" />
// Browser warning (still works, but logs error)
<stop offset="0%" stop-color="#abc" />
```

## Keyboard Shortcuts

### 18. Use `event.code` for Modifier Independence
Apple keyboards send different characters under Option than Windows keyboards under Alt. Use `e.code` (physical key position) not `e.key` (character) for platform-independent shortcuts:

```typescript
e.code === "KeyN"  // "N" regardless of layout
// NOT:
e.key === "n"      // "ñ" on macOS with Option held
```

### 19. Avoid Browser-Reserved Shortcuts
`Cmd+N` on macOS opens a new browser window. `Cmd+Shift+F` enters fullscreen. Use Option/Alt for app shortcuts:
- `Opt+N` / `Alt+N` — New item
- `Opt+Shift+F` / `Alt+Shift+F` — New folder

## Styling

### 20. Input Elements Need Explicit `font-family: inherit`
Browsers give `<input>`, `<select>`, and `<textarea>` default system fonts. Always override:

```css
input, select, textarea {
  font-family: inherit;
  font-size: inherit;
}
```

### 21. `border-radius: var(--border-radius)` on Form Elements
Native form elements don't inherit border-radius from body. Add it explicitly:

```css
input, select, textarea {
  border-radius: var(--border-radius);
}
```

## API Routes

### 22. Always Check `res.ok` Before Reading `res.json()`
A common pattern that silently swallows errors:

```typescript
// BAD — ignores HTTP errors
const data = await res.json();

// GOOD — validates response
if (!res.ok) {
  throw new Error(`Request failed: ${res.status}`);
}
const data = await res.json();
```

### 23. Wrap `sql.notify()` and `triggerWebhooks()` in Try-Catch
These are side effects. If they fail (e.g., PostgreSQL listener disconnected, webhook endpoint unreachable), they should NOT break the main API response. Always wrap in try-catch:

```typescript
try { await eventBus.notify(channel, payload); } catch {}
try { await triggerWebhooks(...); } catch {}
```

## Deployment

### 24. Docker Volume Mount Overwrites Build Artifacts
When mounting a volume over `public/uploads/`, the Docker volume replaces the build-time copy. This is correct for uploaded files, but the initial `.gitkeep` files need to exist or Next.js may error on missing directories.

```dockerfile
RUN mkdir -p public/uploads/avatars public/uploads/notes
```

### 25. `output: "standalone"` for Docker
Add to `next.config.ts` for Docker builds:
```typescript
output: "standalone",
```
This bundles all dependencies into `.next/standalone/`, making the Docker image self-contained without copying `node_modules`.

## Cross-Stack Gotchas

### 26. Next.js 16 `params` is a Promise
Route handler `params` must be awaited in Next.js 16:

```typescript
// CORRECT
const { id } = await params;

// BROKEN — returns undefined
const { id } = params;
```

### 27. `cookies()` Must Be Awaited
Next.js 16 cookies API requires await:

```typescript
const cookieStore = await cookies();
const token = cookieStore.get("session-token")?.value;
```

### 28. `process.cwd()` Not `__dirname`
Turbopack resolves `__dirname` to synthetic directories that don't match the filesystem. Always use `process.cwd()` for absolute paths:

```typescript
// CORRECT
const dbPath = path.join(process.cwd(), "data", "mydb.db");

// BROKEN in Turbopack
const dbPath = path.join(__dirname, "data", "mydb.db");
```

This applies to file I/O, SQLite paths, and any absolute path construction.

### 29. SQLite WAL Mode: Single Connection Pool
SQLite in WAL mode requires exactly 1 connection. Multiple connections will read stale snapshots:

```typescript
pool: {
  min: 1,
  max: 1,  // CRITICAL — do not increase
}
```

### 30. PostgreSQL Count Returns String, Not Number
PostgreSQL's `COUNT()` with raw queries returns a string. Always coerce:

```typescript
const count = Number(countResult.total);  // correct
const count = countResult.total;          // BROKEN — string, not number
```

### 31. PostgreSQL Booleans Are Strict
Never insert `0`/`1` for boolean columns on PostgreSQL:

```typescript
// CORRECT
await db.insert(table).values({ isActive: true });

// BROKEN on PostgreSQL
await db.insert(table).values({ isActive: 1 });
```

Also normalize on output: `!!row.isActive`.

### 32. Empty Strings Fail Foreign Key Constraints
Select/dropdown components emit `""` when no option is chosen. PATCH handlers must convert `""` to `null` for nullable FK columns:

```typescript
const update: Record<string, unknown> = {};
if (body.ownerId !== undefined) update.ownerId = body.ownerId || null;
if (body.parentId !== undefined) update.parentId = body.parentId || null;
```

### 33. `serverExternalPackages`: Native Bindings Only
Only add packages that contain native C/C++ bindings to `serverExternalPackages` in `next.config.ts`:

```typescript
serverExternalPackages: ["better-sqlite3", "bcryptjs"],
```

Never add pure-JS packages here — it disables bundling optimizations for those packages.

### 34. Browser Extension Errors in Dev
Firefox (`moz-extension://`) and Chrome (`chrome-extension://`) inject errors that trigger Next.js/Turbopack error overlay in development. Suppress in root layout:

```typescript
useEffect(() => {
  const handler = (e: ErrorEvent) => {
    if (e.filename?.includes("extension://")) e.stopImmediatePropagation();
  };
  window.addEventListener("error", handler, true);
  window.addEventListener("unhandledrejection", handler, true);
  return () => {
    window.removeEventListener("error", handler, true);
    window.removeEventListener("unhandledrejection", handler, true);
  };
}, []);
```

### 35. Vitest `fileParallelism: false` for SQLite
If using SQLite as test database, disable file parallelism to avoid locking:

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    fileParallelism: false,
  },
});
```

### 36. Bcrypt Salt Version Varies Across Environments
Bcrypt generates `$2a$` or `$2b$` prefixes depending on the platform. Test assertions must be flexible:

```typescript
expect(hash).toMatch(/^\$2[ab]\$/);
```

### 37. Password: 8-Character Minimum, Current Password on Self-Service Updates
- Require minimum 8 characters for all new passwords
- Require `currentPassword` verification when users change their own password (not when admin resets)
- Never allow disabling MFA via API (block in PATCH route if `twoFactorEnabled` is set to `false` without proper verification)

## Advanced Architecture Gotchas

### 38. Document & File Download UX
- **Pitfall**: Using `window.open('/api/export?format=pdf')` on endpoints returning file attachments opens a permanent, empty blank tab, creating poor UX. Using `data:application/pdf;base64,...` in anchor tags fails silently on files over 2MB.
- **Fix**: Convert binary/base64 files to a `Blob`, generate a temporary `URL.createObjectURL(blob)`, and click a hidden programmatic `<a>` tag with a `download` attribute, cleanly running `URL.revokeObjectURL(url)` on completion.

### 39. Multi-Field API Config Saves
- **Pitfall**: Saving individual form fields (like SMTP host, port, user) sequentially triggers a loop of API requests, causing a flood of toast notifications (toast spam) on the screen.
- **Fix**: Always design batch update endpoints (e.g. `PATCH /api/admin/settings` taking a JSON dictionary of key-value pairs) to handle multi-field saves in a single transaction with a single success toast.

### 40. Server-Sent Events Socket Leakage
- **Pitfall**: Next.js hot module reloading (HMR) or navigation transitions can leak SSE/pub-sub socket listeners on the server, eventually exhausting system descriptors.
- **Fix**: Always attach abort listeners (`request.signal.addEventListener('abort', cleanup)`) inside server streams and run explicit close cleanups on `useEffect` unmounts in the browser.

### 41. Client-Component Layout Gating
- **Pitfall**: Placing interactive buttons with `onClick` handlers in layouts without marking them as `"use client";` causes build-time failures during static page generation: `Error: Event handlers cannot be passed to Client Component props`.
- **Fix**: Always split layouts into modular client components or add `"use client";` at the top of layouts hosting global search or theme-toggle click handlers.

### 42. Bundling vs. On-Demand CDN Autoloading
- **Pitfall**: Bundling massive libraries like `mermaid` (supporting complex SVG renders) or `prismjs` (supporting 297 languages) directly in the NPM bundle bloats bundle size, slows compiles, and pulls in deprecated transitive CLI packages (like `esbuild-kit`).
- **Fix**: Load them dynamically on-demand from a CDN (such as `cdnjs` or `jsdelivr`) via lightweight React hooks (`useMermaid()`, `usePrism()`) only on routes containing that specific markdown code-block type, keeping the core bundle slim.

### 43. User-Directed Tagged Releases
- **Pitfall**: Automated scaffolding or versioning agents running `git tag` or creating GitHub releases without human approval.
- **Fix**: Enforce the rule that versioning must remain strictly inside files (`package.json`, `README.md`) and the CHANGELOG. The human creator retains 100% control over running `git tag` or creating releases.
