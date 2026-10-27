## Challenge 2 — API2:2023 — Broken Authentication


**Challenge Idea:** Forge a JWT by discovering the application's weak signing secret and modifying the `isAdmin` claim to `"true"` to trigger the privileged behavior in the token verification middleware.

**Root Cause:** The application uses a weak JWT signing secret that can be discovered, allowing an attacker to forge tokens with modified claims.

**Vulnerable Code:**
```javascript
const JWT_SECRET = 'secret123';

const token = jwt.sign(
  {
    userId: user._id,
    username: user.username,
    isAdmin: "false"
  },
  JWT_SECRET
);
```

**Fixed Code (Illustrative):**
```javascript
const crypto = require('crypto');

const JWT_SECRET = process.env.JWT_SECRET;

if (!JWT_SECRET || Buffer.byteLength(JWT_SECRET) < 32) {
  throw new Error('JWT_SECRET must be securely configured');
}

const token = jwt.sign(
  {
    userId: user._id,
    username: user.username,
    isAdmin: false
  },
  JWT_SECRET,
  {
    algorithm: 'HS256',
    expiresIn: '15m'
  }
);
```

**Fix:** Use a strong, randomly generated signing secret stored securely, explicitly restrict accepted algorithms during token verification, and enforce authorization checks on protected endpoints.
