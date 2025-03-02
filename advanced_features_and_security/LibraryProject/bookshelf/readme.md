`can_view`: Allows users to view books.
- `can_create`: Allows users to create books.
- `can_edit`: Allows users to edit books.
- `can_delete`: Allows users to delete books.

## Groups
The following groups are created and assigned permissions:
- **Viewers**: Can view books.
- **Editors**: Can view, create, and edit books.
- **Admins**: Can view, create, edit, and delete books.

## Views
Views are protected using the `@permission_required` decorator to enforce these permissions.
Deliverables
models.py: Updated with custom permissions for the Book model.

views.py: Updated to include permission checks in relevant views.

## settings.py to secure the App:

DEBUG = False: Ensures debug information is not exposed in production, preventing sensitive information leaks.
ALLOWED_HOSTS: Restricts the application to only respond to requests from specified hosts, preventing host header attacks.
SECURE_BROWSER_XSS_FILTER, X_FRAME_OPTIONS, SECURE_CONTENT_TYPE_NOSNIFF: These settings enable browser-side protections against XSS and other attacks.
CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE, SECURE_SSL_REDIRECT: Enforce HTTPS and secure cookie handling, protecting against man-in-the-middle attacks.
CSP configuration is added to prevent XSS attacks by restricting the sources from which content can be loaded.
templates/my_form.html:
{% csrf_token %}: Includes a CSRF token in the form, preventing CSRF attacks.
views.py:
Uses Django's ORM for database queries, which automatically parameterizes queries and prevents SQL injection.
get_object_or_404 is used to safely retrieve objects from the database.
Forms are used for user input validation, preventing malicious input from being processed.
Search views now utilize the django ORM to prevent SQL injection.

--------------------------------------------------------------------------------------------------------------------

## Security Review:

HTTPS Enforcement:
SECURE_SSL_REDIRECT ensures all traffic is redirected to HTTPS, preventing data transmission in plaintext.
SECURE_HSTS_SECONDS, SECURE_HSTS_INCLUDE_SUBDOMAINS, and SECURE_HSTS_PRELOAD enforce HTTPS by instructing browsers to only connect via HTTPS, even for subdomains, and allows preloading this policy into browsers.
Secure Cookies:
SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE prevent cookies from being sent over unencrypted connections, mitigating the risk of session hijacking and CSRF attacks.
Secure Headers:
X_FRAME_OPTIONS prevents clickjacking attacks by disallowing the site from being embedded in frames.
SECURE_CONTENT_TYPE_NOSNIFF prevents MIME sniffing, reducing the risk of malicious content being interpreted as a different type.
SECURE_BROWSER_XSS_FILTER enables the browser's XSS protection, helping to mitigate cross-site scripting attacks.
Deployment Security:
Configuring Nginx with SSL/TLS certificates ensures secure communication between the server and clients.
Nginx also provides the ability to add and manage security related headers.


