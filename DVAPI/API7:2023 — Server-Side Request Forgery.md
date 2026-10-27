## Challenge 7 — API7:2023 — Server-Side Request Forgery (SSRF)

**Challenge Idea:** Investigate the `addNoteWithLink` functionality by supplying a URL in the request body and testing whether the server can be tricked into fetching content from an unintended destination. The fetched content is then stored in the authenticated user's `secretNote`.

**Root Cause:** The controller passes the user-supplied URL directly to `request()` without validating the destination. The server fetches the remote content and stores its first line in the user's `secretNote`, potentially allowing requests to unintended or internal resources.

**Vulnerable Code**
```javascript
exports.addNoteWithLink = (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.send('url parameter missing');
  }

  request(url, (err, response, body) => {
    try {
      const note = body.split('\n').slice(0, 1).join('\n');

      async function updateUserSecretNote(userId) {
        const updatedUser = await User.findOneAndUpdate(
          { _id: userId },
          { secretNote: note },
          { new: true }
        );

        return res.json({
          status: "success",
          message: 'Successfully added a note',
          note
        });
      }

      updateUserSecretNote(req.userId);
    } catch (err) {
      res.status(500).send('There was an error: ');
    }
  });
};
```

**Fixed Code (Illustrative):**
```javascript
const parsedUrl = new URL(url);
const allowedHosts = ["trusted.example.com"];

if (
  parsedUrl.protocol !== "https:" ||
  !allowedHosts.includes(parsedUrl.hostname)
) {
  return res.status(400).json({
    status: "error",
    message: "Invalid URL"
  });
}

// Fetch the URL only after validating the destination.
// Also validate resolved IP addresses and redirect targets.
```

**Fix:** Avoid fetching arbitrary user-supplied URLs. Allow only trusted destinations, validate resolved IP addresses to block loopback and private network access, and ensure redirects cannot bypass validation. Handle request errors and invalid responses safely.

**Key Takeaway:** SSRF occurs when an attacker can influence server-side requests to reach destinations the application should not access. Always validate outbound request destinations before fetching remote content.
