# Apply and test the auth patch (Windows PowerShell)

Base commit: `442e8a4c9ec18180756fa454806b77a16bfb6ad8` on main.
Feature branch: `feature/auth-session-social-2026-11-16`. This change is for review
and local testing first; it is not a production authentication release.

## Apply

Run from your project-athena repository. Save the download as
`Athena_Auth_and_Database.patch` in Downloads. Start with a clean working tree;
if `git status --short` lists work, commit that work on its current branch before
switching. Do not delete or commit local learner databases or `.env` files.

```powershell
git status --short
git fetch origin
git switch -c test/auth-session-social origin/main
git apply --check "$HOME\Downloads\Athena_Auth_and_Database.patch"
git apply "$HOME\Downloads\Athena_Auth_and_Database.patch"
python -m pip install -r backend/requirements-dev.txt
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\run_auth_test.ps1
```

The script generates a **local test secret** once in
`backend/.env.auth-test-secret` and reuses it. It selects
`backend/athena-auth-test.db` explicitly, applies migrations, then starts FastAPI.
The secret and all local SQLite files are ignored by Git. Your normal `.env` and
`athena-measurement-review.db` are not edited or deleted. If port 8000 is already
serving Athena, stop that server first rather than leaving two versions running.

Open **http://127.0.0.1:8000/login.html**. Use `127.0.0.1` consistently: `localhost`
and `127.0.0.1` have separate browser cookies and storage. Do not serve the frontend
from a different static server. Create a new synthetic test account through the
existing signup page; the isolated test database starts empty.

If the patch check fails, stop and compare the current commit with the base above;
do not force apply. If your repository already contains this feature branch,
checkout that branch instead of applying the patch twice. A clean reversal before
committing is `git apply -R --check <patch>` followed by `git apply -R <patch>`;
keep the test database/secret separate. Do not use reset/clean to remove data.

## What to test

1. Email signup and sign-in. Move between dashboard, progress, account, grades,
   topics and lessons. Open another tab on the same host. No extra sign-in should
   be needed while the server-side browser session is valid.
2. Sign out from Account. Other tabs clear cached credentials via storage changes;
   protected pages/requests require authentication again. Existing access JWTs have
   a maximum default lifetime of 30 minutes; stolen bearer revocation is not
   immediate in this compatibility-based design.
3. Password Show/Hide, browser autofill, keyboard navigation, mobile widths,
   wrong-password feedback and resuming a `?next=/lesson.html?...` destination.
4. In developer tools, simulate a failed `/auth/me` request or a temporary network
   outage. Athena must retain the account state and offer retry, rather than
   redirecting you to sign-in as if you logged out.
5. To exercise expiration quickly, set
   `$env:ATHENA_ACCESS_TOKEN_EXPIRE_MINUTES = '1'` before launching. Wait over a
   minute, then load a protected page or submit practice. Renewal should happen
   without another password. Reset the variable to `30` afterward.
6. Remember-me unchecked: server-side renewal lasts up to 12 hours, with a browser
   session cookie. Checked: up to 30 days on that browser/device. Browser restore
   features may retain session cookies; always sign out on a shared computer.
7. Check browser storage: the long-lived session secret is HttpOnly. Access JWTs
   remain available to JavaScript in per-tab sessionStorage for existing bearer
   clients; this is not a complete move to a cookie-only/BFF architecture.

Google/Apple buttons are disabled until their server configuration is complete.
There is no fake social login, and real credentials have not been tested here.
Existing local email accounts are not automatically linked by email alone; use
the original email/password method. Authenticated provider linking is later work.
Password reset remains an honestly labelled, unfinished backend feature.

## Enable Google

Create a **web application OAuth client** in your Google Cloud project, configure
its consent screen/test users and register exactly:

`http://127.0.0.1:8000/api/v1/auth/oauth/google/callback`

Set `ATHENA_GOOGLE_CLIENT_ID` and `ATHENA_GOOGLE_CLIENT_SECRET` in your local
backend `.env` or process environment and restart the server. For a deployed
staging site, register its exact HTTPS callback and set `ATHENA_PUBLIC_BASE_URL`.
Use only the scopes already requested by this patch: openid, email and profile.
Never add these secrets to the patch or Git. Use a separate test identity when
there is already a local account with the same email.

## Enable Apple

Apple's web setup requires an Apple Developer configuration: a primary App ID
with Sign in with Apple, a related Services ID, a private key/Key ID and Team ID,
plus a registered real HTTPS domain/return URL. It cannot use plain localhost.
Register `https://YOUR-STAGING-DOMAIN/api/v1/auth/oauth/apple/callback` and set:

- `ATHENA_APPLE_CLIENT_ID` (Services ID)
- `ATHENA_APPLE_TEAM_ID`
- `ATHENA_APPLE_KEY_ID`
- `ATHENA_APPLE_PRIVATE_KEY` (PEM, or literal `\n` separated lines)
- `ATHENA_PUBLIC_BASE_URL=https://YOUR-STAGING-DOMAIN`
- `ATHENA_COOKIE_SECURE=true`

The local PowerShell launcher deliberately forces HTTP/local testing; do not use
it for HTTPS Apple staging. Start uvicorn/deploy with the staging environment
instead. Suppress or redact callback query strings in server/proxy logs so temporary
authorisation codes are not retained. Apple may hide the user's email and only supplies name details on first
authorisation; Athena asks for a first name when necessary and uses the provider
subject as the durable identity. If using Apple's relay address for future emails,
configure Apple's email relay requirements before sending messages.

## Automated checks

From the repository root with a disposable database and test JWT configured:

```powershell
$env:PYTHONPATH = 'backend'
$env:ATHENA_JWT_SECRET = 'local-regression-tests-only'
$env:ATHENA_DATABASE_URL = 'sqlite://'
$env:ATHENA_UNLOCK_ALL_LESSONS = 'true'
python -m pytest backend/tests -q
node --test frontend/tests/*.test.js
python tools/verify_runtime_parity.py --content-only
```

The API schema intentionally changes for the new auth endpoints. Content-only
parity checks ensure lesson/reveal/bank outputs stay the same. The content unlock
is for local curriculum QA; access-control tests explicitly disable it.

Automated provider tests use real signature/claim validation with an offline test
provider. They are not evidence of live Google/Apple console setup. This execution
environment previously blocked Chromium's process socket; desktop/mobile visual,
real provider and audio acceptance remain local/staging checks.
