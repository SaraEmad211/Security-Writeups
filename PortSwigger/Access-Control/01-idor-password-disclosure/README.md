# 🔐 IDOR Leading to Password Disclosure

## 📌 Summary
During testing, I discovered an **Insecure Direct Object Reference (IDOR)** vulnerability in the account functionality.

The application uses a user-controlled parameter (`id`) to retrieve account data without proper authorization checks.  
By modifying this parameter, it is possible to access other users' sensitive data, including their passwords.

---

## 🧪 My Testing Approach

After logging in as a normal user (`wiener`), I started testing how the account functionality works.

Initially, I tried:
- Modifying the `id` parameter
- Then attempting to change the password

However, I observed that:
> Even after changing the `id`, the password update was still applied to my own account (`wiener`), not the targeted user.

This indicates that:
- The application relies on **session-based identity for actions (POST requests)**  
- But uses **user-controlled input (`id`) for data retrieval (GET requests)**  

This inconsistency led me to focus on **information disclosure instead of direct account manipulation**.

---

## 📌 Vulnerability Type
- Broken Access Control (IDOR)
- Sensitive Data Exposure

---

## 📌 Affected Endpoint

GET /my-account?id=<user>


---

## 📌 Steps to Reproduce

1. Login using valid credentials:

wiener:peter


2. Navigate to:

/my-account?id=wiener


3. Intercept the request using Burp Suite.

4. Modify the `id` parameter:

id=administrator


5. Forward the request.

---

## 📸 Evidence

### 1. Normal Request
![Normal Request](https://raw.githubusercontent.com/SaraEmad211/Security-Writeups/main/PortSwigger/Access-Control/01-idor-password-disclosure/images/normal-request.png)

---

### 2. IDOR Exploitation
![IDOR Exploit](https://raw.githubusercontent.com/SaraEmad211/Security-Writeups/main/PortSwigger/Access-Control/01-idor-password-disclosure/images/idor-modified-request%20%26password-disclosure%20.png)

---

### 3. Admin Login
![Admin Login](https://raw.githubusercontent.com/SaraEmad211/Security-Writeups/main/PortSwigger/Access-Control/01-idor-password-disclosure/images/admin-login.png)

---

### 4. Delete User
![Delete User](https://raw.githubusercontent.com/SaraEmad211/Security-Writeups/main/PortSwigger/Access-Control/01-idor-password-disclosure/images/delete-user.png)
---

## 📌 Proof of Concept (PoC)

After modifying the `id` parameter to `administrator`, the response contained:

- Username: administrator  
- Password (prefilled in input field)

This confirms that:
- No authorization checks are enforced
- Sensitive data is exposed to unauthorized users

---

## 🚨 Impact

- Disclosure of administrator password
- Account takeover possibility
- Unauthorized access to sensitive user data
- Ability to perform privileged actions (e.g., delete users)

---

## ⚠️ Root Cause

- Missing authorization checks on user-controlled parameter (`id`)
- Trusting client input to fetch sensitive data
- Inconsistent access control between GET and POST requests

---

## 🛠️ Mitigation

- Enforce server-side authorization checks
- Ensure users can only access their own data
- Do not expose sensitive data (especially passwords) in responses
- Use session-based identity instead of request parameters

---

## 📊 Severity (CVSS Estimate)

**High (8.5 - 9.0)**  
Due to:
- Sensitive data exposure
- Potential account takeover

---

## 🧠 Key Insight

The vulnerability highlights a critical design flaw:

> The application separates data retrieval (based on user input) from action execution (based on session),  
> leading to unintended exposure of sensitive information.
