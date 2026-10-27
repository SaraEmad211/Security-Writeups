## Challenge 8 — API8:2023 — Security Misconfiguration

**Challenge Idea:** Trigger a JWT verification error by tampering with the token in the `POST /api/addNote` request. The server rejects the token with HTTP 401 but exposes the challenge flag in the error response.

**Root Cause:** The `verifyToken` middleware exposes the error object and stack trace in the response and includes the flag in the error handler. This leaks sensitive information even when authentication fails.

**Vulnerable Code**
```javascript
} catch (err) {
  console.error(err);
  answer = 'e437a249928eaf337ce67e299848876eca1f10e1799d38b393d29305321ad70e';
  const decipher = crypto.createDecipheriv('aes-256-cbc', wrench, iv);
  let decrypted = decipher.update(answer, 'hex', 'utf-8');
  decrypted += decipher.final('utf-8');

  res.status(401).json({
    status: "error",
    err,
    stack: err.stack,
    message: 'Sever Misconfiguration',
    flag: decrypted
  });
}
```

**Fixed Code (Illustrative):**
```javascript
} catch (err) {
  console.error(err);

  return res.status(401).json({
    status: "error",
    message: "Authentication failed"
  });
}
```

**Fix:** Return generic error messages to clients instead of exposing stack traces or internal error details. Keep detailed errors in server-side logs and never include sensitive flags or secrets in error responses.
