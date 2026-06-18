# Multi-Tenancy & Permission Guard Patterns

If the project supports multiple tenants (workspaces, teams, organizations), apply these patterns consistently.

## Schema

```typescript
// workspace table
export const workspace = pgTable("workspace", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  slug: text("slug").notNull().unique(),
  createdById: text("created_by_id").notNull().references(() => user.id, { onDelete: "cascade" }),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
});

// junction table
export const workspaceMember = pgTable("workspace_member", {
  id: text("id").primaryKey(),
  workspaceId: text("workspace_id").notNull().references(() => workspace.id, { onDelete: "cascade" }),
  userId: text("user_id").notNull().references(() => user.id, { onDelete: "cascade" }),
  role: text("role").notNull().default("member"), // owner | admin | member | viewer
});
```

## Permission Guard (Reusable)

```typescript
type MinRole = "owner" | "admin" | "member" | "viewer";
const ROLE_HIERARCHY: Record<MinRole, number> = { owner: 4, admin: 3, member: 2, viewer: 1 };

export async function requireWorkspaceAccess(
  userId: string,
  workspaceId: string,
  minRole?: MinRole
): Promise<typeof workspaceMember.$inferSelect | null> {
  const membership = await db.query.workspaceMember.findFirst({
    where: and(eq(workspaceMember.userId, userId), eq(workspaceMember.workspaceId, workspaceId)),
  });
  if (!membership) return null;
  if (minRole && ROLE_HIERARCHY[membership.role as MinRole] < ROLE_HIERARCHY[minRole]) return null;
  return membership;
}
```

Use in API routes:

```typescript
const membership = await requireWorkspaceAccess(session.user.id, workspaceId);
if (!membership) return NextResponse.json({ error: "Forbidden" }, { status: 403 });
// For write: requireWorkspaceAccess(session.user.id, workspaceId, "admin")
```

## Creator Auto-Join

When creating a workspace, always insert the creator as "owner":

```typescript
await db.insert(workspaceMember).values({
  id: crypto.randomUUID(),
  workspaceId: ws.id,
  userId: session.user.id,
  role: "owner",
});
```

Without this, the creator cannot access their own workspace through the permission guard.

## Member Query Pattern

Return workspaces where the user is a member (not just creator):

```typescript
const memberships = await db.query.workspaceMember.findMany({
  where: eq(workspaceMember.userId, session.user.id),
  columns: { workspaceId: true },
});
const workspaceIds = memberships.map((m) => m.workspaceId);

const workspaces = await db.query.workspace.findMany({
  where: inArray(workspace.id, workspaceIds),
  // ...
});
```

## Super Admin Bypass

Super admins can access all workspaces:

```typescript
if (session.user.role === "super_admin") {
  // Skip membership check, return all workspaces
  const workspaces = await db.query.workspace.findMany({ ... });
} else {
  // Normal member-based query
}
```

The first registered user should be auto-promoted to super_admin:

```typescript
databaseHooks: {
  user: {
    create: {
      before: async (user) => {
        const existing = await db.select({ count: sql<number>`count(*)` }).from(userTable);
        if (existing[0]?.count === 0) {
          user.role = "super_admin";
        }
      },
    },
  },
},
```

## Audit Logging

```typescript
export const auditLog = pgTable("audit_log", {
  id: text("id").primaryKey(),
  userId: text("user_id").notNull().references(() => user.id),
  action: text("action").notNull(), // NOTE_CREATE, WORKSPACE_DELETE, etc.
  details: text("details"),
  ipAddress: text("ip_address"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
}, (table) => [
  index("audit_user_idx").on(table.userId),
  index("audit_action_idx").on(table.action),
  index("audit_created_idx").on(table.createdAt),
]);

export async function logAction(userId: string, action: string, details?: string, request?: Request) {
  try {
    const ip = request?.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || null;
    await db.insert(auditLog).values({ id: crypto.randomUUID(), userId, action, details: details || null, ipAddress: ip });
  } catch { /* never break main flow */ }
}
```

Wire into every CRUD route:

```typescript
try { await logAction(session.user.id, "NOTE_CREATE", `Created note "${title}"`, request); } catch {}
```

## Inviting Members

Two approaches:

1. **Email-based**: POST workspaceId + email → if user exists, insert membership. If not, store invitation + send email.
2. **Autocomplete**: GET non-members → list registered users not in workspace → select + add. Pattern:

```typescript
// GET /api/workspaces/[id]/non-members
const members = await db.query.workspaceMember.findMany({ where: eq(workspaceMember.workspaceId, id), columns: { userId: true } });
const memberIds = members.map((m) => m.userId);
const nonMembers = await db.query.user.findMany({ where: notInArray(user.id, memberIds) });
```
