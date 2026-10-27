## Challenge 6 — API6:2023 — Unrestricted Access to Sensitive Business Flows

**Challenge Idea:** Use Burp Suite Intruder with null payloads to send repeated requests and investigate whether a sensitive business flow can be abused through excessive automated requests.

**Root Cause:** The API may lack appropriate controls to prevent repeated automated requests from abusing a sensitive business operation.

**Vulnerable Code (Illustrative):**
```javascript
app.post("/api/action", async (req, res) => {
  const result = await performSensitiveAction(req.user.id);
  res.json(result);
});
```

**Fixed Code (Illustrative):**
```javascript
app.post(
  "/api/action",
  authenticateUser,
  rateLimitSensitiveActions,
  async (req, res) => {
    const result = await performSensitiveAction(req.user.id);
    res.json(result);
  }
);
```

**Fix:** Apply rate limits and business-specific controls to sensitive operations, and prevent repeated requests from producing unintended outcomes.
