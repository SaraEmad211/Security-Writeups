## Challenge 3 — API3:2023 — Broken Object Property Level Authorization (Mass Assignment)

**Challenge Idea:** Modify the registration request by adding a `score` field, which the API accepts. After registering and logging in with the new account, retrieve the scores using `GET /api/scores`.

**Root Cause:** The API accepts user-supplied properties during registration without properly restricting which fields the client is allowed to set.

**Vulnerable Code (Illustrative):**
```javascript
const user = await db.users.create({
  data: req.body
});
```

**Fixed Code (Illustrative):**
```javascript
const { username, password } = req.body;

const user = await db.users.create({
  data: { username, password }
});
```

**Fix:** Allowlist the fields users can submit and assign sensitive properties, such as `score` or `isAdmin`, only through trusted server-side logic.

**Key Takeaway:** Never blindly assign client-supplied request properties to database records; explicitly control which properties users can create or modify.
