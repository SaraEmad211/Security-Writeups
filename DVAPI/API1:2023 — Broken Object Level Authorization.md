## Challenge 1 — API1:2023 — Broken Object Level Authorization (BOLA)

**Challenge Idea:** Access another user's private notes by modifying the username parameter in the API request (GET /api/getNote?username=anotheruser).


**Root Cause:** The API trusts the user-controlled `username` without verifying resource ownership.

**Vulnerable Code**
```javascript
const user = await User.findOne({
  username: req.query.username
});

return res.json({
  status: "success",
  note: user.secretNote
});
```

**Fixed Code (Illustrative):**
```javascript
const user = await User.findById(req.userId);

if (!user) {
  return res.status(404).json({
    status: "error",
    message: "User not found"
  });
}

return res.json({
  status: "success",
  note: user.secretNote
});
```

**Fix:** Use the authenticated user's identity instead of trusting a client-supplied username.
