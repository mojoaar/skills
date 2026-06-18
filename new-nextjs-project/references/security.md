# Security Patterns

Apply these to every API route that handles user data or triggers external requests. Each section covers one OWASP category.

## SSRF Protection (Webhooks)

When the app sends HTTP requests to user-supplied URLs (webhooks), validate the target before resolving DNS:

```typescript
import { isIP } from "net";

async function validateUrl(url: string): Promise<boolean> {
  const parsed = new URL(url);
  // Block loopback / private ranges
  const hostname = parsed.hostname;
  if (hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1") return false;
  // RFC 1918 private ranges
  const ip = isIP(hostname) ? hostname : (await dns.resolve4(hostname))?.[0];
  if (!ip) return false;
  if (ip.startsWith("10.") || ip.startsWith("172.16.") || ip.startsWith("192.168.")) return false;
  return true;
}
```

Wrap webhook dispatch in `try-catch` with a 5-second abort timeout. Never let a failing webhook break the main API response.

## XSS Sanitization (Markdown)

ReactMarkdown with `rehype-sanitize` strips dangerous HTML. Use the explicit schema to allow safe elements like `<br>`:

```typescript
import rehypeSanitize from "rehype-sanitize";
import { defaultSchema } from "hast-util-sanitize";

<ReactMarkdown
  rehypePlugins={[[rehypeSanitize, { ...defaultSchema }]]}
>
  {content}
</ReactMarkdown>
```

## Rate Limiting

In-memory sliding window — no Redis needed for single-instance:

```typescript
const buckets = new Map<string, number[]>();

export function checkRateLimit(key: string, maxRequests: number, windowMs: number): boolean {
  const now = Date.now();
  const timestamps = buckets.get(key) || [];
  const windowStart = now - windowMs;
  const recent = timestamps.filter((t) => t > windowStart);
  if (recent.length >= maxRequests) return false;
  recent.push(now);
  buckets.set(key, recent);
  return true;
}
```

Apply to auth endpoints (30/min) and file upload endpoints (10/min).

## BOLA (Broken Object-Level Authorization)

Every resource access must verify the user is a member of the parent workspace/tenant:

```typescript
// GUARD PATTERN — apply to every route that returns or modifies resources
const membership = await db.query.workspaceMember.findFirst({
  where: and(eq(workspaceMember.userId, session.user.id), eq(workspaceMember.workspaceId, workspaceId)),
});
if (!membership) {
  return NextResponse.json({ error: "Forbidden" }, { status: 403 });
}
// For write operations, also check role
if (!["owner", "admin"].includes(membership.role)) {
  return NextResponse.json({ error: "Forbidden" }, { status: 403 });
}
```

Never trust client-supplied IDs. Always verify ownership server-side.

## Encryption at Rest

Store sensitive plugin credentials and API keys encrypted with AES-256-GCM:

```typescript
import crypto from "crypto";

const ALGORITHM = "aes-256-gcm";
const KEY = Buffer.from(process.env.ENCRYPTION_KEY!, "hex"); // 64 hex chars = 32 bytes

export function encrypt(text: string): { encrypted: string; iv: string; tag: string } {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv);
  let encrypted = cipher.update(text, "utf8", "hex");
  encrypted += cipher.final("hex");
  const tag = cipher.getAuthTag().toString("hex");
  return { encrypted, iv: iv.toString("hex"), tag };
}

export function decrypt(encrypted: string, iv: string, tag: string): string {
  const decipher = crypto.createDecipheriv(ALGORITHM, KEY, Buffer.from(iv, "hex"));
  decipher.setAuthTag(Buffer.from(tag, "hex"));
  let decrypted = decipher.update(encrypted, "hex", "utf8");
  decrypted += decipher.final("utf8");
  return decrypted;
}
```

Sensitive key names to encrypt: `apiKey`, `secret`, `password`, `accessToken`, `refreshToken`, `clientSecret`, `tokenId`, `token`, `privateKey`.

Before sending to client, mask encrypted values with `"••••••••"` — never leak plaintext credentials to the browser.

## Protection Checklist (Every API Route)

1. **401** — no valid session
2. **404** — resource not found
3. **403** — authenticated but unauthorized (wrong workspace, wrong role)
4. **400** — invalid/missing input (validate with Zod)
5. Side effects wrapped in `try-catch` (webhooks, notifications, audit logs)
