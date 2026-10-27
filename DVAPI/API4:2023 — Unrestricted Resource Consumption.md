## Challenge 4 — API4:2023 — Unrestricted Resource Consumption

**Challenge Idea:** Test the profile image upload functionality by submitting a very large image to investigate whether the API properly limits resource-intensive requests.

**Root Cause:** The API may lack adequate restrictions on uploaded file size, allowing oversized uploads to consume excessive server resources.

**Vulnerable Code (Illustrative):**
```javascript
app.post("/api/profile/image", upload.single("image"), async (req, res) => {
  await saveProfileImage(req.file);
  res.json({ message: "Image uploaded successfully" });
});
```

**Fixed Code (Illustrative):**
```javascript
const upload = multer({
  limits: { fileSize: 2 * 1024 * 1024 } // 2 MB
});

app.post("/api/profile/image", upload.single("image"), async (req, res) => {
  await saveProfileImage(req.file);
  res.json({ message: "Image uploaded successfully" });
});
```

**Fix:** Enforce upload-size limits, validate file types, and apply appropriate request and resource limits to prevent excessive resource consumption.

**Key Takeaway:** APIs should enforce resource limits on expensive operations, including file uploads, to reduce the risk of resource exhaustion.
