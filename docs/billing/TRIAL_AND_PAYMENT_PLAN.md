# Athena: 14-day trial, then R149 per month

## Current offer

R0 initially; 14 full days from successful payment-method authorisation; then
R149 per calendar month until canceled. One trial per account. For a child,
an adult payer completes the subscription agreement. No card fields are served
by Athena. Current counts are generated from the curriculum and practice
registries: 399 interactive lessons, 58 topics, 5,688 practice questions.
These counts describe implemented content, not a completed educational audit.

## This patch: local simulation only

The local launcher enables ATHENA_BILLING_TEST_MODE=true. The configuration and
all mutation endpoints reject test billing outside development. No live provider
adapter or scheduler is included, so credentials alone cannot activate charging.
The simulated agreement is not evidence of an actual willingness to pay.

GET /api/v1/payments/plan is public. Status requires sign-in. Mutations use
same-origin checks and the signed-in user; request bodies reject extra fields,
including card data. Never enter real card details into this build.

Successful test authorisation stores a server-generated test method reference,
price snapshot, currency, terms version, consent timestamp, authorisation time,
and trial end time in trial_subscriptions. The primary key allows only one
trial per user. Declines store no agreement and start no clock. Double submits
or retries return the existing trial without changing its end time.

The start, end and mock first-payment dates are persisted. Test payment attempts
before authorisation + 14*24 hours are rejected by the server. The test clock can
be advanced to the end for testing; this does not change the system clock.
The first simulated payment is recorded once using a conditional update. No
permanent premium flag is set and existing development curriculum unlocking
continues independently. Cancellation stops further simulated payments and
retains the current trial/paid-period access-until date.

billing_notifications stores two durable previews: confirmation immediately,
and a reminder due seven days before trial end. These are marked
`test_preview_only`; no email is sent and no delivery is claimed. The receipt
shows both previews. A first test charge simulates the trial-to-paid transition
only; ongoing monthly collections and retries require the live adapter.

## Live integration: next action item

1. Verify PayFast account and enable recurring billing. Obtain sandbox
   credentials and a staging HTTPS origin first. Keep credentials in secrets.
2. Create a provider-hosted subscription checkout: initial amount 0.00,
   recurring amount 149.00, monthly frequency. Preserve the displayed agreement,
   payer attestation and consent version before redirecting to the provider.
3. A browser success redirect must never start a trial or grant paid access.
   Verify the PayFast ITN signature, origin/server validation, merchant, amount,
   currency and subscription reference. Process each provider event idempotently.
4. Start the trial from verified payment-method authorisation, not signup or
   checkout creation. Record the authoritative timestamp in UTC. The first
   billing time must be >= authorised_at + 14 days. PayFast's billing_date is
   date-based: choose a date that cannot produce an earlier charge, rounding
   forward in the agreed timezone when needed. Validate actual sandbox timing.
5. Send a confirmation containing the agreement, first billing date and easy
   cancellation link. Run a reliable worker to send the seven-day reminder,
   record delivery/retries, and alert on failures. Do not enable live charging
   until this notification path passes testing.
6. Cancellation must call the provider and persist its confirmed outcome.
   Reconcile webhook events, retries, failures, refunds and cancellation races.
   Permit paid access only from verified provider state; expire trial access
   from server dates. Remove development unlock overrides for staging tests.
7. Validate the hosted card flow, failed/canceled authorisations, duplicate and
   forged notifications, same-account abuse, refunds, and early-charge guards.
   Publish final merchant identity, support/contact and subscription terms.
8. Enable live mode deliberately after sandbox approval. There is no browser
   switch, environment-only toggle or placeholder webhook to activate it here.

## Research (official PayFast sources, checked 17 November 2026)

- Zero initial amount tokenises the card; recurring payments must be nonzero:
  https://support.payfast.help/portal/en/kb/articles/can-a-subscription-be-set-up-with-an-initial-zero-amount-payment-20-9-2022
- Recurring billing and billing_date:
  https://developers.payfast.co.za/docs#recurring_billing
- Free trials: consent, confirmation, cancellation, and reminder at least seven
  days before the first recurring charge:
  https://support.payfast.help/portal/en/kb/articles/can-i-offer-free-trials-and-introductory-promotions-as-part-of-an-ongoing-subscription-service-20-9-2022

## Applying and testing

Apply this patch after Athena_Remove_Progress_Tab.patch. It is also compatible
with the earlier local-unlock patch (the launcher insertion is separate).
Restart tools/run_auth_test.ps1; it migrates the existing versioned local DB to
0003_trial_subscriptions without deleting learner records. Unversioned SQLite
still requires the explicit backed-up adoption flow.

Open index.html → Start my 14-day free trial → sign in if required → tick both
consents → approve the test method. Inspect the dates, reminder preview and
Account link. Attempt an early payment: expect refusal. Advance the test clock,
then simulate the first R149 payment: expect success once only. Use another
local account to test a declined authorisation and cancellation before expiry.

After live checkout exists, measure actual completed provider authorisations,
trial usage, cancellations, first successful charges, and retention. Mock
completions must always be excluded from those conversion metrics.

## Verification for this patch

397 backend tests passed with development unlocking and isolated SQLite, followed
by a passing versioned-auth-database upgrade preservation test. Checkout, shared
layout, practice navigation and session frontend checks passed. Browser QA
verified the rendered offer counts, R0/R149 disclosure, unchecked consents,
explicit simulation notice and landing CTA destination. The authenticated
trial lifecycle was verified through API and frontend controller tests.
Mobile viewport rendering, Windows PowerShell execution, real provider
authorisation and real email delivery remain to be tested.
