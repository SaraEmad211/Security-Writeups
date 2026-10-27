## Challenge 3 — API3:2023 — Broken Object Property Level Authorization (Mass Assignment)

**Challenge Idea:** Modify the registration request by adding a `score` field with value of at least 10000, which the API accepts. After registering and logging in with the new account, retrieve the scores using `GET /api/scores`.

**Root Cause:** The API accepts user-supplied properties during registration without properly restricting which fields the client is allowed to set.

**Vulnerable Code**
```javascript
const adduser = req.body;
const newUser = new User(adduser);
const user = await newUser.save();
```

**Fixed Code (Illustrative):**
```javascript
const { username, password } = req.body;

const newUser = new User({
  username,
  password
});

const user = await newUser.save();
```

**Fix:** Allowlist the fields users can submit and assign sensitive properties, such as `score` or `isAdmin`, only through trusted server-side logic.

**Key Takeaway:** Never blindly assign client-supplied request properties to database records; explicitly control which properties users can create or modify.
