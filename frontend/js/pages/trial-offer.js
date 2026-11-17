/* The displayed offer and catalogue counts come from the server. */
const AthenaOffer = {
  async load() {
    const response = await fetch('/api/v1/payments/plan');
    if (!response.ok) throw new Error('The trial offer could not load. Please refresh and try again.');
    return response.json();
  },
  benefits(plan) {
    return `<ul class="trial-benefits"><li><strong>${plan.interactive_lessons} interactive maths lessons</strong> across Grades 8–12</li><li><strong>${plan.topics} CAPS topics</strong> to revisit throughout the school year</li><li><strong>${plan.practice_questions.toLocaleString()} practice questions</strong> with feedback and hints</li><li>Step-by-step worked examples to understand the method</li><li>Multiple-choice and written-answer practice at your own pace</li></ul>`;
  },
  async mount() {
    for (const host of document.querySelectorAll('[data-trial-offer]')) {
      try {
        const plan = await this.load();
        host.innerHTML = `<div class="trial-offer-copy"><p class="eyebrow">More confidence in maths</p><h2 id="trial-offer-title">Give every step a chance to click.</h2><p>Build understanding today and keep the full maths library within reach.</p>${this.benefits(plan)}</div><div class="card trial-price-card"><span class="badge">14 days free</span><p class="trial-price">R0 <small>for your first 14 days</small></p><p><strong>Then R149/month</strong>, renewing monthly until you cancel.</p><p>Payment details required. Your trial starts after your payment method is authorised. Cancel before the first charge to pay nothing.</p><a class="btn btn-primary" href="checkout.html">Start my 14-day free trial</a><p class="trial-small">${plan.test_checkout_enabled ? 'Test checkout available · No real payment details or charges.' : 'Checkout preview · Live payments are not connected yet.'}</p><a href="checkout.html#trial-terms">See trial and cancellation details</a></div>`;
      } catch(error) { host.textContent = error.message; }
    }
  }
};
document.addEventListener('DOMContentLoaded', () => AthenaOffer.mount());
