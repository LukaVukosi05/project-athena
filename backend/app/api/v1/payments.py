"""
api/v1/payments.py — subscription checkout & webhook endpoints (Phase 5).

Endpoints to implement:

  POST /api/v1/payments/checkout
    -> creates a checkout session with whichever South African-
       compatible payment provider is chosen (decision deferred to
       Phase 5). We never handle card details ourselves — brief
       section 70: "Payments: Never handle sensitive card
       information ourselves."

  POST /api/v1/payments/webhook
    -> receives payment provider events (success, failure,
       cancellation, refund) and updates User.is_premium
       accordingly. Must verify the webhook signature.

  GET /api/v1/payments/status
    -> current subscription status for the logged-in user —
       replaces the `isPremium` flag currently flipped client-side
       in frontend/js/pages/lesson.js (renderPaywall's "Start
       Premium" button, which is a Phase-1-only stub).

Test extensively in the provider's sandbox mode before accepting
real money, per the brief's Phase 5 note.

# TODO (Phase 5 — do not build before a closed beta has validated
# willingness to pay)
"""
