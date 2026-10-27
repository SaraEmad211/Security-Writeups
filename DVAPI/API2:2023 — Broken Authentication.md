## Challenge 2 — API2:2023 — Broken Authentication


**Challenge Idea:** Forge a JWT by discovering the weak HMAC signing secret, changing the `admin` claim to `true`, and signing the modified token to access a protected API endpoint (`GET /api/user/user`).

**Root Cause:** The application uses a weak JWT signing secret that can be discovered, allowing an attacker to forge tokens with modified claims.

**Vulnerable Code (Illustrative):**
```javascript
const token = jwt.sign(
  { userId: user.id, admin: user.isAdmin },
  "weak-secret",
  { algorithm: "HS256" }
);
```

**Fixed Code (Illustrative):**
```javascript
const token = jwt.sign(
  { userId: user.id, admin: user.isAdmin },
  process.env.JWT_SECRET,
  { algorithm: "HS256", expiresIn: "15m" }
);
```

**Fix:** Use a strong, randomly generated signing secret stored securely, explicitly restrict accepted algorithms during token verification, and enforce authorization checks on protected endpoints.
