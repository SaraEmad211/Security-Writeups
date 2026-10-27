## Challenge 5 — API5:2023 — Broken Function Level Authorization

**Challenge Idea:** Investigate profile-related API endpoints by using the `OPTIONS` method to discover supported HTTP methods, then test whether a restricted function can be accessed using the `DELETE` method.

**Root Cause:** The API may expose sensitive functionality without properly checking whether the authenticated user has permission to perform the requested action.

**Vulnerable Code (Illustrative):**
```javascript
app.delete("/api/profiles/:id", async (req, res) => {
  await deleteProfile(req.params.id);
  res.sendStatus(204);
});
```

**Fixed Code (Illustrative):**
```javascript
app.delete(
  "/api/profiles/:id",
  authenticateUser,
  requireAdmin,
  async (req, res) => {
    await deleteProfile(req.params.id);
    res.sendStatus(204);
  }
);
```

**Fix:** Enforce server-side authorization checks for sensitive functions and restrict administrative operations to authorized roles.

**Key Takeaway:** Authentication alone is not enough; the API must verify that the user is authorized to perform each requested function.

*Note: The code snippets are illustrative examples, not the challenge's original source code. The solve notes mention testing `OPTIONS` and `DELETE`, but do not confirm that an unauthorized deletion succeeded.*
