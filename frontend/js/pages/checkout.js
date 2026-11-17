/* Customer membership flow. Provider simulation remains behind a disclosed preview. */
const TrialCheckout = {
  plan: null, user: null, busy: false,
  destination() { const next=AthenaAuth.safeNext(new URLSearchParams(location.search).get('next')); return next.startsWith('/checkout.html') ? '/index.html' : next; },
  async init() {
    renderNav('Account');
    document.getElementById('trial-form').onsubmit = event => { event.preventDefault(); this.beginPayment(); };
    document.getElementById('preview-activate').onclick = () => this.authorise();
    document.getElementById('preview-back').onclick = () => { document.getElementById('payment-preview').hidden=true; document.getElementById('trial-form').hidden=false; };
    try {
      this.plan = await AthenaOffer.load();
      this.user = await AthenaAuth.restoreSession(); renderNav('Account');
      document.getElementById('checkout-availability').textContent = this.plan.test_checkout_enabled
        ? 'Payment preview · No card details or money collected.'
        : 'Payment setup is not available yet. You can still explore Athena.';
      if (this.user) await this.refresh();
      else document.getElementById('trial-form').hidden = !this.plan.test_checkout_enabled;
    } catch(error) { this.feedback(error.message); }
  },
  feedback(text) { const node=document.getElementById('checkout-feedback'); node.textContent=text; node.focus(); },
  async beginPayment() {
    if (this.busy || !document.getElementById('trial-form').reportValidity()) return;
    try {
      if (!this.user) { this.user=await AthenaAuth.requireSession(); if (!this.user) return; }
      document.getElementById('trial-form').hidden=true;
      document.getElementById('payment-preview').hidden=false;
      document.getElementById('preview-activate').focus();
    } catch(error) { this.feedback(error.message); }
  },
  async refresh() {
    const status = await AthenaAuth.request('/api/v1/payments/status');
    document.getElementById('trial-form').hidden = status.status !== 'not_started' || !this.plan.test_checkout_enabled;
    document.getElementById('payment-preview').hidden=true;
    const receipt=document.getElementById('trial-receipt'); receipt.hidden=status.status==='not_started';
    if (receipt.hidden) return;
    const canceled=Boolean(status.canceled_at);
    receipt.innerHTML=`<div class="membership-confirmation"><h3>${canceled ? 'Your access is canceled.' : status.has_test_access ? 'Your access is ready.' : 'Your access period has ended.'}</h3><a class="btn btn-primary membership-cta" href="${escapeHtml(this.destination())}">Continue to Athena <span aria-hidden="true">→</span></a>${!canceled && this.plan.test_checkout_enabled ? '<button class="btn btn-ghost" type="button" data-trial-action="cancel">Cancel access preview</button>' : ''}</div>`;
    receipt.querySelector('[data-trial-action="cancel"]')?.addEventListener('click',()=>this.cancel());
  },
  async authorise() {
    if (this.busy || !document.getElementById('adult-payer').checked || !document.getElementById('trial-consent').checked) return;
    this.busy=true; const button=document.getElementById('preview-activate'); button.disabled=true;
    try {
      if (!this.user) return;
      await AthenaAuth.request('/api/v1/payments/test/authorise',{method:'POST',body:JSON.stringify({consent:true,adult_payer:true,terms_version:this.plan.terms_version,outcome:'approved'})});
      location.assign(this.destination());
    } catch(error) { this.feedback(error.message); }
    finally { this.busy=false; button.disabled=false; }
  },
  async cancel() {
    if (this.busy) return; this.busy=true;
    try {
      await AthenaAuth.request('/api/v1/payments/cancel',{method:'POST'});
      await this.refresh(); this.feedback('Your access preview has been canceled. No charge was made.');
    } catch(error) { this.feedback(error.message); }
    finally { this.busy=false; }
  }
};
document.addEventListener('DOMContentLoaded',()=>TrialCheckout.init());
