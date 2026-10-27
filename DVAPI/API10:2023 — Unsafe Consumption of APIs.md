## Challenge 10 — API10:2023 — Unsafe Consumption of APIs

**Challenge Idea:** Bypass login authentication by sending a MongoDB operator (`{"$gt": 0}`) in the password field. The SQL injection payload fails with HTTP 401, while the NoSQL injection payload returns HTTP 200 and the flag.

**Root Cause:** The login endpoint passes user-controlled `username` and `password` values directly into a MongoDB query. Because the password input is not validated as a string, a MongoDB operator object can alter the query conditions and potentially bypass authentication.

**Vulnerable Code**
```javascript
// Controller function for user login
exports.login = async (req, res) => {
  try {
    const { username, password } = req.body;

    // Find the user with the given username and password
    const user = await User.findOne({
      username: username,
      password: password
    });

    if (!user) {
      return res.status(401).json({
        message: 'Authentication failed'
      });
    }

    // Generate a JWT token and send it in the response
    console.log(user);
    const token = jwt.sign({
      userId: user._id,
      username: user.username,
      isAdmin: "false"
    }, JWT_SECRET);

    if (username == "admin") {
      res.cookie("auth", token, {
        httpOnly: false,
      });
      res.set('Authorization', `Bearer ${token}`);

      const answer = '6c09249f4efc5d6b95ce3419d1790952b3a37ee634aea77d5a68a3055decf2d1';
      const decipher = crypto.createDecipheriv(
        'aes-256-cbc', wrench, iv
      );
      let decrypted = decipher.update(answer, 'hex', 'utf-8');
      decrypted += decipher.final('utf-8');

      return res.json({
        status: "success",
        message: 'Authentication successful',
        flag: decrypted
      });
    }

    res.cookie("auth", token, {
      httpOnly: false,
    });
    res.set('Authorization', `Bearer ${token}`);

    return res.json({
      status: 'success',
      message: 'Authentication successful'
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({
      message: 'Internal server error'
    });
  }
};
```

**Fixed Code (Illustrative):**
```javascript
exports.login = async (req, res) => {
  try {
    const { username, password } = req.body;

    if (
      typeof username !== 'string' ||
      typeof password !== 'string'
    ) {
      return res.status(400).json({
        message: 'Invalid input'
      });
    }

    const user = await User.findOne({ username });

    if (!user || !(await verifyPassword(password, user.passwordHash))) {
      return res.status(401).json({
        message: 'Authentication failed'
      });
    }

    // Generate a token only after successful password verification
    // Apply the application's normal token and response logic here.
  } catch (err) {
    console.error(err);
    return res.status(500).json({
      message: 'Internal server error'
    });
  }
};
```

**Fix:** Validate that `username` and `password` are strings before using them. Avoid passing untrusted objects directly into MongoDB queries. Retrieve the user by username and verify the submitted password against a securely stored password hash.
