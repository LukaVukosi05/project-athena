# Athena sign-in: evidence and decisions

Research checked 16 November 2026. Intended audience: South African Grade 8–12
learners, with parents/guardians supporting account setup. This is a returning-user
sign-in page, not the subscription sales page.

## What the evidence supports

| Primary source | Observation | Athena decision |
| --- | --- | --- |
| [Desmos account guide](https://help.desmos.com/hc/en-us/articles/4405021623565-Sign-Up-for-and-Manage-Your-Account) | A maths product offers Google, Apple and email, and one account across its tools. | Familiar sign-in choices; one Athena browser session across pages. |
| [Khan Academy account guide](https://support.khanacademy.org/hc/en-us/articles/202487450-How-do-I-set-up-a-new-user-account) | Its education account flow supports external identity providers and distinguishes learner/parent/teacher roles. | Provider buttons plus email fallback; acknowledge supporting adults. Do not claim Athena already has a separate parent portal. |
| [Nielsen Norman Group mobile login checklist](https://www.nngroup.com/articles/checklist-registration-login/) | Mobile password entry is difficult and error-prone; alternatives and show-password controls reduce this effort. | Autofill, email keyboard, visible labels, show/hide password and provider choices. |
| [NN/g cognitive-load principles](https://www.nngroup.com/articles/4-principles-reduce-cognitive-load/) | Structure, clarity, transparency and guidance reduce the mental work of completing forms. | One clear email action, concise recovery feedback, no extra grade/marketing fields in the returning-user form. |
| [Baymard show-password public summary](https://baymard.com/guidelines/665-show-password-feature) | Masking makes typing errors difficult to notice. Full research is paywalled. | Password is masked initially, with an explicit Show/Hide button. |
| [OWASP session guidance](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | Session secrets need appropriate cookie protections and server-side controls. | HttpOnly renewal secret, HTTPS in production, SameSite protection, server-side hashed/revocable sessions. |

Desmos and Khan Academy are relevant design precedents, not evidence of a measured
conversion rate. Their private funnels and A/B results were unavailable. The
current Khan Academy/Duolingo JavaScript login pages did not expose a useful full
layout through retrieval, so the review relies on the cited first-party account
guides rather than claiming to have visually inspected those live screens.
No numerical uplift or guaranteed conversion is claimed.

## Psychology, with limits

The most defensible mechanism is lower cognitive and physical effort: reuse a
familiar identity, reduce recall, support recognition with labels and show the
user what happened after submission. Calm learning copy and the worked-equation
illustration are Athena-specific design hypotheses intended to reduce intimidation;
they are not a clinical claim or a proven conversion intervention. The palette
and textbook typography are inherited from Athena's existing design tokens.

Desktop uses a reassuring learning panel beside a concise form. Mobile collapses
the illustration so the sign-in controls remain prominent. Both provider options
are visible. Disabled buttons explicitly say they need configuration; the page
does not simulate a working provider. Remember-me is optional and unchecked for
shared-device safety. There are no fabricated testimonials, urgency counters,
payment demands or promises that unfinished curriculum is approved.

## Measurement plan

Define sign-in success as authenticated access to the intended destination,
not a button click. Start with usability sessions with 5–8 learner/guardian pairs,
then use actual traffic to estimate completion, error and abandonment rates.
Collect consent-aware aggregate events only; never log passwords, tokens, email
addresses or raw provider subjects into marketing analytics.

| Metric | Definition / use |
| --- | --- |
| Sign-in completion | Completed sessions / unique sign-in visits; distinguish existing and new accounts |
| Time to authenticated destination | Median and p90, split by device and method |
| Failure/recovery rate | Failed submissions and provider errors followed by a successful retry |
| Reauthentication friction | Unexpected sign-in prompts per active session and per page transition |
| Provider availability | Separate disabled/unconfigured methods from real provider failures |
| Learning activation | A completed meaningful lesson/practice action after sign-in, not just a dashboard view |

This patch does not add an analytics vendor or claim those events are already
being collected. Once provider setup and the session bug are verified, compare a
stable version with a single deliberate variation. Do not interpret low-volume
changes as statistical proof, and do not equate sign-in completion with paid
subscription conversion.

## Provider/security references

- [Google OpenID Connect server flow](https://developers.google.com/identity/openid-connect/openid-connect)
- [Authlib Starlette/OIDC integration](https://docs.authlib.org/en/v1.6.5/client/starlette.html)
- [Apple web configuration](https://developer.apple.com/help/account/capabilities/configure-sign-in-with-apple-for-the-web/)
- [Apple callback and first-authorisation behaviour](https://developer.apple.com/documentation/signinwithapple/configuring-your-webpage-for-sign-in-with-apple)
- [Apple environment and key setup](https://developer.apple.com/documentation/signinwithapple/configuring-your-environment-for-sign-in-with-apple)

The application uses Authlib's verified authorization-code/OIDC path, with state,
nonce, signed ID-token verification, and Google PKCE. Apple returns via form POST;
its transient OAuth cookie therefore uses Secure/SameSite=None on HTTPS. Athena's
separate browser-renewal cookie remains SameSite=Lax. Tokens from Google/Apple are
not written to URLs, logs or localStorage and are not retained as API access grants.
