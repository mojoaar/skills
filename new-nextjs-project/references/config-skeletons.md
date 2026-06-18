# Config File Skeletons

Minimal, correct configurations for each tool. Adjust based on chosen stack (e.g., remove Drizzle if no database).

## `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## `next.config.ts`

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Required for Docker standalone builds
  output: "standalone",

  // Only add packages with native C/C++ bindings here
  // serverExternalPackages: ["better-sqlite3"],

  // Allow images from external domains (if needed)
  // images: { remotePatterns: [{ protocol: "https", hostname: "**" }] },

  // Increase body size for file uploads
  // experimental: { serverActions: { bodySizeLimit: "10mb" } },
};

export default nextConfig;
```

## `vitest.config.ts`

```typescript
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    environment: "jsdom",
    setupFiles: ["./src/__tests__/setup.ts"],
    // Required if using SQLite as test DB
    // fileParallelism: false,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

## `drizzle.config.ts`

Place at project root. Only needed if database is chosen.

```typescript
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/lib/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql", // or "sqlite"
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

## `eslint.config.mjs` (optional — Next.js defaults are sufficient)

```typescript
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({ baseDirectory: __dirname });

const eslintConfig = [...compat.extends("next/core-web-vitals", "next/typescript")];

export default eslintConfig;
```

## Package Scripts (in `package.json`)

```json
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "test": "vitest run",
  "test:watch": "vitest",
  "lint": "next lint",
  "db:push": "npx drizzle-kit push",
  "db:migrate": "npx drizzle-kit generate && npx drizzle-kit migrate"
}
```
