## Challenge 4 — API4:2023 — Unrestricted Resource Consumption

**Challenge Idea:** Test the profile image upload functionality by submitting a very large image to investigate whether the API properly limits resource-intensive requests.

**Root Cause:** The controller moves the uploaded file and updates the user's profile image before checking its size. The size check does not reject oversized files, allowing large uploads to be stored.

**Vulnerable Code**
```javascript
file.mv(uploadPath, (err) => {
  if (err) {
    console.error(err);
    return res.status(500).send(err);
  }

  async function updateUserProfilePic(userId) {
    try {
      const updatedUser = await User.findOneAndUpdate(
        { _id: userId },
        { profilePic: req.userId + fileExtension },
        { new: true }
      );

      if (fileSize >= 1024) {
        if (fileSize >= 1024 * 50) {
          // Challenge flag is returned here.
        }
      }
    } catch (error) {
      return res.status(500).json({
        message: 'Failed to update user profile pic'
      });
    }
  }

  updateUserProfilePic(req.userId);
});
```

**Fixed Code (Illustrative):**
```javascript
const MAX_FILE_SIZE = 2 * 1024 * 1024; // 2 MiB

if (file.size > MAX_FILE_SIZE) {
  return res.status(413).json({
    status: "error",
    message: "File too large"
  });
}

// Move and process the file only after validation.
```

**Fix:** Enforce upload-size limits, validate file types, and apply appropriate request and resource limits to prevent excessive resource consumption.

**Key Takeaway:** APIs should enforce resource limits on expensive operations, including file uploads, to reduce the risk of resource exhaustion.
