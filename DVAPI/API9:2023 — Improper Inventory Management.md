## Challenge 9 — API9:2023 — Improper Inventory Management

**Challenge Idea:** Discover unreleased challenges by changing the `released` parameter to `unreleased` in the `POST /api/allChallenges` request. The response reveals two hidden challenges, and Challenge 12's `shortDescription` contains the flag.

**Root Cause:** The API exposes unreleased challenge information based on a client-controlled parameter without restricting access to hidden challenges.

**Vulnerable Code**
```javascript
exports.allChallenges = (req, res) => {
  const { unreleased } = req.body;
  const { released } = req.body;

  if (unreleased === 1) {
    const answer = "c7b29f2076be7df2f1502c55ee40286e385f27d0bcda065f30678e85b040327e882d7711cd643cb94fdd438863e49758";
    const decipher = crypto.createDecipheriv(
      'aes-256-cbc', wrench, iv
    );
    let decrypted = decipher.update(answer, 'hex', 'utf-8');
    decrypted += decipher.final('utf-8');

    var unreleasedChallenges = [
      {
        "id": 11,
        "challengeName": "Challenge11",
        "shortDescription": "This is challenge11",
        "longDescription": "This is long description of challenge11",
        "challengeLogo": "/image/challenge11.png"
      },
      {
        "id": 12,
        "challengeName": "Challenge12",
        "shortDescription": "This is challenge12 " + decrypted,
        "longDescription": "This is long description of challenge12",
        "challengeLogo": "/image/challenge12.png"
      }
    ];

    return res.json({
      status: "success",
      challenges: unreleasedChallenges
    });
  } else if (released === 1) {
    // Returns the 10 released challenges
    // ...
  } else {
    return res.status(500).json({
      status: "error",
      message: "Something went wrong"
    });
  }
};
```

**Fixed Code (Illustrative):**
```javascript
exports.allChallenges = async (req, res) => {
  try {
    const challenges = await Challenge.find({
      released: true
    });

    return res.json({
      status: "success",
      challenges
    });
  } catch (err) {
    return res.status(500).json({
      status: "error",
      message: "Internal server error"
    });
  }
};
```

**Fix:** Do not expose unreleased API resources based solely on a client-controlled parameter. Enforce server-side authorization and return only resources intended to be publicly available.
