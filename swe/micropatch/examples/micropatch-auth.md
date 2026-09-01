# MicroPatch: API JWT Auth
version: 1
last_applied_upstream: v2.3.0
risk: medium
context: Protect multi-tenant API routes without changing public health or login behavior.

## What It Is
Adds JWT authentication to protected API routes and injects the decoded user into the request context.

## Intent
The upstream project is a generic HTTP service with no built-in auth. This customization protects
private API endpoints for a multi-tenant SaaS product without forcing each route to implement its
own token checks.

The important design choice is middleware-level enforcement. New protected API routes should inherit
auth automatically instead of relying on every handler to remember it.

## Scope and Non-Goals
In scope:
- protect `/api/*` routes with bearer-token JWT auth
- populate `req.user` for protected routes
- leave public routes like `/health` and `/login` untouched

Out of scope:
- refresh-token flows
- UI login screens
- role-management UX
- admin-only authorization rules beyond basic JWT validation

## What It Does
- `Authorization: Bearer <token>` is required for protected API routes
- valid tokens populate `req.user` with decoded claims
- invalid or missing tokens return `401`
- public routes remain accessible without a token

Example behavior:

```text
GET /api/projects        without token  -> 401 Unauthorized
GET /api/projects        with token     -> 200 and handler sees req.user.id
GET /health              without token  -> 200 OK
```

## Dependencies and Assumptions
- JWT verification library is available
- `JWT_SECRET` exists in environment configuration
- the server has a shared request pipeline where middleware can run before route handlers
- protected routes are grouped under `/api`

## Implementation Reference
New file:

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

function verifyJWT(req, res, next) {
  const header = req.headers['authorization'];
  if (!header || !header.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' });
  }

  try {
    const token = header.slice(7);
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

module.exports = { verifyJWT };
```

Protected-route integration:

```javascript
const { verifyJWT } = require('./middleware/auth');

app.use('/api', verifyJWT);
```

## Anchors
- `src/server.js` or the main server bootstrap file initializes the HTTP app and registers middleware.
  Add the auth middleware after JSON/body parsing and before protected `/api` routes are registered.
- the router setup file is responsible for mounting route groups; the JWT middleware belongs where API
  routes are grouped, not inside each individual handler.
- if the upstream now uses a plugin, hook, or middleware chain abstraction instead of raw `app.use`,
  attach the auth check at the equivalent pre-handler stage for protected API routes.

## Definition of Done
- Requests to protected `/api/*` routes without a bearer token must return `401 Unauthorized`.
- Requests to protected `/api/*` routes with a valid token must reach the handler.
- Protected route handlers must receive `req.user.id` and should receive the decoded claims needed by existing handlers.
- Requests to `/health` without a token must continue to return `200 OK`.
- The auth layer must not register duplicate middleware for the same protected route group if the patch is applied again.

## Notes for Future Re-application
- upstream may later add its own auth layer; compare behavior before applying this patch blindly
- if upstream changes route grouping away from `/api`, preserve the protected-route behavior rather than the old path layout
- applying this patch twice should not register duplicate auth middleware on the same route group
