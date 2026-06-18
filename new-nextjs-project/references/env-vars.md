# Environment Variables

Create `.env.example` with placeholder values and `.env` (git-ignored) with real values. Groups below show which vars are needed based on chosen stack.

## Base (Always Required)

```env
NODE_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## PostgreSQL + Drizzle

```env
DATABASE_URL=postgres://<user>:<password>@localhost:<port>/<dbname>
DB_MAX_CONNECTIONS=10
```

## Authentication (Better Auth)

```env
BETTER_AUTH_SECRET=<32+ character random string>
BETTER_AUTH_URL=http://localhost:3000
# Generate: openssl rand -base64 48
```

## Email (Notification Delivery)

```env
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASS=password
EMAIL_FROM=noreply@example.com
```

## Encryption (Plugin Credentials, Sync Tokens)

```env
ENCRYPTION_KEY=<64 hex characters — 32 bytes>
# Generate: openssl rand -hex 32
```

## OAuth / Sync Integrations (pCloud, Google Drive, etc.)

```env
PCLOUD_CLIENT_ID=your_pcloud_client_id
PCLOUD_CLIENT_SECRET=your_pcloud_client_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## Docker Compose

In `docker-compose.yml`, inject these via `${VAR_NAME}` substitution or explicitly:

```yaml
services:
  app:
    environment:
      - DATABASE_URL=postgres://user:pass@postgres:5432/db
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - BETTER_AUTH_URL=${BETTER_AUTH_URL}
      - NEXT_PUBLIC_APP_URL=${NEXT_PUBLIC_APP_URL}
      - SMTP_HOST=${SMTP_HOST}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASS=${SMTP_PASS}
      - EMAIL_FROM=${EMAIL_FROM}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
```

## Systemd Deployment

Store secrets in `/opt/<app>/secrets.env` with `chmod 600`:

```service
[Service]
EnvironmentFile=/opt/<app>/secrets.env
```

## Dev Mode Fallbacks

Email (nodemailer): if `SMTP_HOST` is not set and `NODE_ENV === "development"`, print email content to console instead:

```typescript
if (!process.env.SMTP_HOST && process.env.NODE_ENV === "development") {
  console.log("[email] To:", to);
  console.log("[email] Subject:", subject);
  console.log("[email] Body:", body);
  return;
}
```

Encryption: if `ENCRYPTION_KEY` is not set, throw a clear error on startup rather than failing at runtime:

```typescript
if (!process.env.ENCRYPTION_KEY) {
  throw new Error("ENCRYPTION_KEY is required. Generate: openssl rand -hex 32");
}
```
