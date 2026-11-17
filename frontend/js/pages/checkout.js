const TrialCheckout = {
  plan: null, user: null, busy: false,
  date(value) { return new Date(value).toLocaleString('en-ZA', {dateStyle:'long', timeStyle:'short',timeZone:'Africa/Johannesburg'}) + ' SAST'; },
  async init() {
    renderNav('Account');
    document.getElementById('trial-form').onsubmit = event => { event.preventDefault(); this.authorise(); };
    try {
      this.plan = await AthenaOffer.load();
      document.getElementById('checkout-benefits').innerHTML = AthenaOffer.benefits(this.plan);
      this.user = await AthenaAuth.restoreSession(); renderNav('Account');
      document.getElementById('checkout-availability').textContent = this.plan.test_checkout_enabled
        ? 'Try the complete trial journey with a simulated payment method. Nothing is charged.'
        : 'You can review the offer. Test checkout is disabled and live payments are not connected.';
      if (this.user) await this.refresh();
      else document.getElementById('trial-form').hidden = !this.plan.test_checkout_enabled;
    } catch(error) { this.feedback(error.message); }
  },
  feedback(text) { const node = document.getElementById('checkout-feedback'); node.textContent = text; node.focus(); },
  async refresh() {
    const status = await AthenaAuth.request('/api/v1/payments/status');
    document.getElementById('trial-form').hidden = status.status !== 'not_started' || !this.plan.test_checkout_enabled;
    const receipt = document.getElementById('trial-receipt'); receipt.hidden = status.status === 'not_started';
    if (receipt.hidden) return;
    const canceled = Boolean(status.canceled_at);
    receipt.innerHTML = `<span class="badge">Test subscription</span><h3>${canceled ? 'Subscription canceled' : status.first_charge_at ? 'First payment simulated' : status.status === 'trialing' ? 'Your 14-day test trial has started' : 'Your test trial has ended'}</h3><dl class="trial-dates"><dt>Payment method authorised</dt><dd>${this.date(status.authorised_at)}</dd><dt>Trial ends / first payment due</dt><dd>${this.date(status.trial_ends_at)}</dd><dt>Recurring price</dt><dd>R149/month</dd><dt>Real amount charged</dt><dd>R0 — test mode</dd>${status.first_charge_at ? `<dt>Simulated first payment</dt><dd>R149 on ${this.date(status.first_charge_at)}</dd>` : ''}</dl><p>${canceled ? 'No further payments will be simulated. Trial or paid-period access lasts until ' + this.date(status.access_until) + '.' : 'Cancel before the first payment to pay nothing. The trial cannot restart on this account.'}</p><details><summary>Confirmation and reminder previews</summary><ul>${(status.notifications || []).map(n=>`<li>${n.kind === 'confirmation' ? 'Subscription confirmation' : 'Trial-ending reminder'}: ${this.date(n.due_at)}. Preview only; email not sent.</li>`).join('')}</ul><p>Agreement version: ${escapeHtml(status.terms_version)}</p></details>${this.plan.test_checkout_enabled ? `<div class="trial-actions">${!canceled ? '<button class="btn btn-secondary" data-trial-action="cancel">Cancel subscription</button>' : ''}</div><details class="trial-simulator"><summary>Developer test controls — no real payments</summary><p>The test clock affects this account’s test subscription only.</p><button class="btn btn-ghost" data-trial-action="test/first-charge" ${canceled || status.first_charge_at ? 'disabled' : ''}>Simulate first R149 payment</button><button class="btn btn-ghost" data-trial-action="test/advance" ${status.test_clock_at || status.first_charge_at ? 'disabled' : ''}>Advance test clock to trial end</button></details>` : ''}<p><a href="practice.html">Go to practice</a> · <a href="account.html">Back to Account</a></p>`;
    receipt.querySelectorAll('[data-trial-action]').forEach(button => button.onclick = () => this.action(button.dataset.trialAction));
  },
  async authorise() {
    if (this.busy) return;
    if (!document.getElementById('trial-form').reportValidity()) return;
    this.busy = true; const button=document.querySelector('#trial-form button[type="submit"]'); button.disabled = true;
    try {
      if (!this.user) { this.user = await AthenaAuth.requireSession(); if (!this.user) return; }
      await AthenaAuth.request('/api/v1/payments/test/authorise', {method:'POST',body:JSON.stringify({
        consent:document.getElementById('trial-consent').checked, adult_payer:document.getElementById('adult-payer').checked,
        terms_version:this.plan.terms_version,outcome:document.querySelector('input[name="outcome"]:checked').value
      })});
      await this.refresh(); this.feedback('Test payment method authorised. Your trial dates are saved. No real charge was made.');
    } catch(error) { this.feedback(error.message); }
    finally { this.busy = false; button.disabled = false; }
  },
  async action(path) {
    if (this.busy) return; this.busy=true;
    try {
      await AthenaAuth.request('/api/v1/payments/' + path, {method:'POST'});
      await this.refresh(); this.feedback(path === 'cancel' ? 'Subscription canceled. No further simulated payments.' : 'Test action saved. No real money moved.');
    } catch(error) { this.feedback(error.message); }
    finally { this.busy=false; }
  }
};
document.addEventListener('DOMContentLoaded', () => TrialCheckout.init());
