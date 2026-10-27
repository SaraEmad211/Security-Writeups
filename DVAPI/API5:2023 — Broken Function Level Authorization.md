## Challenge 5 — API5:2023 — Broken Function Level Authorization

**Challenge Idea:** Investigate profile-related API endpoints by using the `OPTIONS` method to discover supported HTTP methods, then test whether a restricted function can be accessed using the `DELETE` method.

**Root Cause:** The API may expose sensitive functionality without properly checking whether the authenticated user has permission to perform the requested action.

**Vulnerable Code**
```javascript
const user = req.params.username;

if (user === 'admin') {
  return res.status(403).json({
    status: "error",
    message: "Cannot delete admin"
  });
}

const result = await User.deleteOne({ username: user });
```

**Fixed Code (Illustrative):**
```javascript
const targetUsername = req.params.username;

if (!req.user.isAdmin) {
  return res.status(403).json({
    status: "error",
    message: "Forbidden"
  });
}

const result = await User.deleteOne({
  username: targetUsername
});
```

**Fix:** Enforce server-side authorization checks for sensitive functions and restrict administrative operations to authorized roles.

**Key Takeaway:** Authentication alone is not enough; the API must verify that the user is authorized to perform each requested function.
