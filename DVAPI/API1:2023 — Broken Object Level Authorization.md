## Challenge 1 — API1:2023 — Broken Object Level Authorization

**Challenge Idea:** Access another user's private notes by modifying the username parameter in the API request (GET /api/getNote?username=anotheruser).


**Root Cause:** The API trusts the user-controlled `username` without verifying resource ownership.

**Vulnerable Code (Illustrative):**
```javascript
const notes = await db.notes.findMany({
  where: { username: req.query.username }
});
```

**Fixed Code (Illustrative):**
```javascript
const notes = await db.notes.findMany({
  where: { username: req.user.username }
});
```

**Fix:** Use the authenticated user's identity instead of trusting a client-supplied username.

**Key Takeaway:** Authentication identifies the user; authorization determines which resources they can access.
