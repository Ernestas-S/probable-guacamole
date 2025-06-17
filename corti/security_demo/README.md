# Flask Security Demo

## Overview

This project demonstrates a **reflected XSS vulnerability** in a simple Flask app and how to mitigate it using custom middleware that leverages [Bleach](https://bleach.readthedocs.io/) to sanitize user input.

The app contains two endpoints:
1. **Vulnerable Endpoint**: Demonstrates the XSS vulnerability by directly embedding user input into the response without sanitization.
2. **Secure Endpoint**: Mitigates the vulnerability by sanitizing user input using the custom middleware.

---

## Setup

Follow these steps to set up and run the application:

```bash
# Navigate to the project directory
cd security_demo

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python -m app
```

---

## Demonstration

### Vulnerable Endpoint

Open the following URL in your browser:

```
http://127.0.0.1:5000/vulnerable/greet?name=<script>alert('XSS')</script>
```

**Expected Behavior**:
- A JavaScript alert will pop up, demonstrating the reflected XSS vulnerability.
- The `<script>` tags are not sanitized, and the malicious input is directly embedded into the response.

---

### Secured Endpoint

Open the following URL in your browser:

```
http://127.0.0.1:5000/secure/greet?name=<script>alert('XSS')</script>
```

**Expected Behavior**:
- The `<script>` tags are sanitized (removed or escaped), so no alert will appear.
- The inner text of the `<script>` tag (e.g., `alert('XSS')`) may appear as plain text or HTML-escaped.

---

## Custom Middleware

The sanitizer middleware is implemented in `middleware/sanitizer.py`. It hooks into Flask’s request lifecycle using the `@app.before_request` decorator and sanitizes incoming request data for routes in the `secure` blueprint.

### Key Features:
- **Sanitization**: Uses `bleach.clean` to remove disallowed HTML tags and attributes.
- **Selective Application**: Only sanitizes routes in the `secure` blueprint.
- **Targets**:
  - Query parameters (`request.args`)
  - Form data (`request.form`)
  - Path parameters (`request.view_args`)

### Example Middleware Code:

```python
from bleach import clean

def sanitize_request(app, allowed_tags=None, allowed_attrs=None):
    allowed_tags = allowed_tags or []
    allowed_attrs = allowed_attrs or {}

    @app.before_request
    def _sanitize():
        if request.blueprint != 'secure':
            return

        for key, val in request.args.items():
            request.args = request.args.copy()
            request.args[key] = clean(val, tags=allowed_tags, attributes=allowed_attrs)
```

---

## Testing

### Manual Testing

You can manually test the endpoints using a browser, `curl`, or Postman:

1. **Vulnerable Endpoint**:
   ```bash
   curl "http://127.0.0.1:5000/vulnerable/greet?name=<script>alert('XSS')</script>"
   ```
   - The response will include the raw `<script>` tags, demonstrating the vulnerability.

2. **Secure Endpoint**:
   ```bash
   curl "http://127.0.0.1:5000/secure/greet?name=<script>alert('XSS')</script>"
   ```
   - The response will sanitize the `<script>` tags, removing or escaping them.

---

### Automated Testing

Automated tests are implemented in `tests/test_xss.py` using `pytest` and Flask’s test client.

#### Example Test Cases:

1. **Vulnerable Endpoint**:
   - Verifies that the `/vulnerable/greet` endpoint allows raw `<script>` tags in the response.
   ```python
   def test_vulnerable_endpoint_allows_script_tags(client):
       payload = "<script>alert('XSS')</script>"
       resp = client.get(f"/vulnerable/greet?name={payload}")
       assert payload in resp.get_data(as_text=True)
   ```

2. **Secure Endpoint**:
   - Verifies that the `/secure/greet` endpoint removes or escapes `<script>` tags.
   ```python
   def test_secure_endpoint_strips_script_tags(client):
       payload = "<script>alert('XSS')</script>"
       resp = client.get(f"/secure/greet?name={payload}")
       assert "<script>" not in resp.get_data(as_text=True)
   ```

---

### Edge Cases

The middleware is designed to handle various edge cases, including:
1. **Nested Tags**:
   - Input: `name=<b><i>test</i></b>`
   - Expected: Only allowed tags (if any) remain.
2. **Unclosed Tags**:
   - Input: `name=<script>alert('XSS')`
   - Expected: The unclosed `<script>` tag is removed.
3. **Attribute Injection**:
   - Input: `name=<img src=x onerror=alert(1)>`
   - Expected: Disallowed attributes (e.g., `onerror`) are removed.

Bleach’s default cleaning policy ensures that these cases are handled securely.

---

## Conclusion

This project demonstrates:
1. How reflected XSS vulnerabilities can occur in applications
2. How to mitigate such vulnerabilities using middleware and libraries

To extend this project:
- Adding more test cases for edge scenarios
- Exploring other sanitization libraries or techniques, that are up to date
- Implementing additional security features