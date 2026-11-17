# Membership layout follow-up — 17 November 2026

Apply after Athena_Membership_Flow_and_Design.patch.

- Place the heading above the two-column layout so the worked example and
  subscription panel share the same top edge. Keep a single-column mobile flow.
- Remove the lower catalogue statistics, repeated benefit list and FAQ section
  from checkout. Retire their unused renderer and CSS. Landing-page benefits
  remain available.
- Keep essential price, renewal, consent and cancellation information in the
  subscription panel. Existing details links now target that summary.
- After successful access activation, navigate straight to the safe onward
  destination (the agreed landing page by default). Do not render the detailed
  preview-date and price receipt.
- Account can still open compact membership management and cancellation.
- No billing logic, stored trial dates or lesson content changes.

The checkout/controller, authentication, shared layout and landing checks pass.
The patch was checked against the preceding UI revision. A fresh browser visual
review and mobile device review remain to be done.

Email delivery has not been implemented by this layout change. The confirmation
and reminder previews already stored by billing remain available for the future
email integration; no customer-facing claim that an email was sent is added.
