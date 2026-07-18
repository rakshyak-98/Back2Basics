- implemented by browser to restrict how documents or scripts loaded from one origin can interact with resources from another origin. It helps protect against cross-site-request forgery and cross-site scripting attacks.

### Same-Origin Policy (SOP): Key Rules

The **Same-Origin Policy (SOP)** is a security measure implemented by web browsers to restrict how documents or scripts loaded from one origin can interact with resources from another origin. It helps protect against **cross-site request forgery (CSRF)** and **cross-site scripting (XSS)** attacks.

### Definition of "Origin":

> **Origin** = **Scheme** (protocol) + **Host** (domain) + **Port**

- Example:
  - `https://example.com:443` and `https://example.com:80` are **different origins** (different ports).
  - `http://example.com` and `https://example.com` are **different origins** (different protocols).
  - `https://sub.example.com` and `https://example.com` are **different origins** (different subdomains).

### SOP Rules:

1. **Same-Origin Requests Allowed**:
   - Requests between the same origin are permitted without restrictions.
   - Example:
     - `https://myapp.com` can freely access resources from `https://myapp.com/api`.

2. **Cross-Origin Requests Restricted**:
   - JavaScript running on `https://myapp.com` cannot access resources on `https://api.example.com` unless **CORS** headers are provided by the server.

3. **DOM Access Restricted**:
   - A script from `https://siteA.com` **cannot manipulate** or read the DOM of `https://siteB.com`.
   - Example:
     ```html
     <iframe src="https://another-site.com"></iframe>
     <script>
       // This will throw an error due to SOP
       const iframeDoc = document.querySelector('iframe').contentDocument;
     </script>
     ```

4. **Cookies and Storage Access Restricted**:
   - JavaScript on one origin cannot access cookies, `localStorage`, or `sessionStorage` of a different origin.
   - Example:
     - Code running on `https://myapp.com` **cannot read cookies** set by `https://another.com`.

5. **XMLHttpRequest and Fetch Restricted**:
   - Requests made using `XMLHttpRequest` or `fetch()` to a different origin are blocked unless the server provides appropriate CORS headers.
   - Example:
     ```javascript
     // Blocked by SOP if the API does not have CORS headers
     fetch('https://api.external.com/data')
       .then(response => response.json())
       .catch(error => console.error('Blocked by SOP:', error));
     ```

6. **Script and Image Tags Not Blocked**:
   - The SOP does **not block** loading of cross-origin **scripts** (`<script>` tags) and **images** (`<img>` tags), but it prevents access to their content.
   - Example:
     ```html
     <script src="https://cdn.example.com/library.js"></script>
     <img src="https://images.example.com/picture.jpg">
     ```

---

### Why SOP Is Important:
- **Prevents Data Leakage**: Protects sensitive user data from being accessed by malicious scripts.
- **Reduces Attack Surface**: Limits the capabilities of potentially harmful cross-origin requests.