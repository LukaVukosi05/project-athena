# Athena membership: research, design and journey

Decision date: 17 November 2026. Price: R149/month after 14 free days.

## The problem and the intended journey

The previous change fixed the logo destination but left email and OAuth defaults
pointing to dashboard.html. The offer was therefore easy to miss. The payment
page also exposed implementation controls and gave insufficient visual priority
to the service, price and cancellation arrangement.

The agreed experience is:

1. Public visitor opens the existing Athena introduction at index.html.
2. They create an account or sign in using an available method.
3. The shared post-sign-in handler asks the server whether access is active.
4. With no active access, it opens the membership offer. The requested onward
   destination is preserved, with index.html as the default.
5. The offer presents the learning value, full recurring price, trial timeline,
   adult-payer confirmation and explicit consent, beside one primary action.
6. While payment integration is unavailable, Continue to payment opens a short,
   clearly identified preview. Preview activation enters no payment agreement.
7. The confirmation offers Continue to Athena, leading to the agreed landing
   page (or a valid lesson the learner specifically requested).
8. A returning member with active access goes straight to the onward destination.
   An expired access period brings the offer back. A canceled but unexpired
   period retains access until its recorded end.

Old dashboard bookmarks redirect to index.html. The retired dashboard renderer
is removed. Account keeps the membership-management entry point. The curriculum
and practice content are unchanged. Existing development unlocking remains a
separate local-review facility; this is not a live server entitlement overhaul.

## Research method and limits

Searches covered academic free-trial field experiments, original credibility
research, checkout usability studies and official education subscription flows.
A direct Google Scholar title search was attempted but was not accessible through
the retrieval tool. The academic papers were read from the publisher and an
author-hosted publisher PDF instead. No claim is made that Scholar itself was
successfully browsed. No paywalled report was treated as fully read.

The evidence supports design principles and experiments; it does not establish
that this particular paywall, a card-required trial, or 14 days will maximise
Athena's revenue. Most source populations differ from South African parents and
school learners. The design is an evidence-informed implementation to evaluate,
not a proven conversion winner.

## Evidence and its application

### 1. Credibility is affected by the experienced interface

Stanford's Web Credibility Guidelines summarise research involving over 4,500
people. They recommend appropriate professional design, verifiable information,
real organisational identity, clear contact routes, usability and restraint in
promotion. This is foundational work from 2002, not a current conversion estimate.

Athena application: consistent navy/teal/serif styling, readable hierarchy,
correct mathematical working and an offer that does not promise unsupported
outcomes. Do not fabricate testimonials, pass rates, school endorsements or
security certification. Real merchant identity and support details remain
required before accepting live payments; none were invented for this design.

Source: https://credibility.stanford.edu/guidelines/

### 2. Put credible information where people notice it

NN/g's account of prominence-interpretation theory explains how noticed elements
shape credibility judgments. It also discusses limitations of retrospective,
self-reported reasons for trust; appearance is not proof of actual security.

Athena application: put a real learning example beside the decision, keep R149
and the renewal interval prominent, and reduce visual competition around the
primary action. These are design inferences, not measured Athena uplift.

Source: https://www.nngroup.com/articles/prominence-interpretation-theory/

### 3. Payment confidence requires coherent presentation and truthful reassurance

Baymard's original usability research observes that people can distrust payment
entry when its presentation feels fragile or undifferentiated. Its sample and
retail checkout context do not directly represent Athena's audience.

Athena application: a contained order panel, familiar form controls, consistent
spacing and plain cancellation language. Do not display a payment-provider seal,
SSL certification or a “secured by” promise before a live integration supports it.
The preview contains no card fields. A restrained disclosure remains beside the
payment action; hiding its lack of real payment capability would damage trust.

Source: https://baymard.com/research-articles/perceived-security-of-payment-form

### 4. Reveal the cost before the commitment

Baymard's checkout research identifies unexpected cost and checkout complexity
as recurring sources of abandonment. Those findings support clarity and shorter
forms, rather than promising a specific percentage gain for this app.

Athena application: R0 due today, the 14-day start condition, R149/month and
cancellation appear together. No preselected subscription consent or hidden
annual billing. The mobile layout places the decision panel before the longer
learning explanation. FAQs follow the decision rather than interrupting it.

Source: https://baymard.com/blog/reduce-cart-abandonment

### 5. Trial length is a contextual choice

Yoganarasimhan, Barzegary and Pani, Management Science (2023), report a randomised
SaaS trial experiment comparing 7, 14 and 30 days with longer-run outcomes. Their
shorter-trial result does not establish an optimum for education or card-required
trials. In particular, it cannot justify declaring Athena's 14-day choice proven.

Athena application: retain the user's selected 14 days, but track actual usage
and retained paid membership when a live trial is available.

Source: https://faculty.washington.edu/hemay/Free_Trial.pdf
DOI: 10.1287/mnsc.2022.4507

A separate 2025 Frontiers in Psychology study reports a two-year image-editing
SaaS experiment involving 680,588 users across 190 countries, comparing 3 and 7
days. It finds effects on adoption and delayed conversion, but not a statistically
significant immediate conversion lift. Different outcomes across studies and
contexts reinforce the need to evaluate Athena's own funnel and retention.

Source: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1568868/full

### 6. Relevant product patterns are inspiration, not causal evidence

Duolingo's official Super offer uses an explicit trial timeline and reminder
explanation. Athena uses that communication pattern with its own 14-day terms;
it does not copy Duolingo's trial length or claim Duolingo conversion results.

Source: https://join.duolingo.com/plus

Khanmigo's official pricing separates learner/parent benefits, and its help page
explains cancellation and the end-of-access date. Athena uses clear adult-payer
wording and a visible Account management route. It does not advertise Khanmigo
features such as parent controls or AI tutoring as though Athena has them.

Sources: https://www.khanmigo.ai/pricing
https://support.khanacademy.org/hc/en-us/articles/21192603565453-How-do-I-cancel-my-Khanmigo-subscription

## Implementation boundaries and next checks

All email and OAuth completion paths call one afterSignIn method. The server's
status endpoint supplies has_access; a persisted browser premium flag is not the
source of that navigation decision. Failed membership checks keep authentication
and lead to a page that can retry rather than granting access or showing the old
dashboard. Redirect destinations remain restricted to this origin.

Developer controls, scenario radios, debug dates and test banners are absent
from the customer page. Development-only billing API guards remain. The preview
notice and confirmation truthfully say no payment agreement or charge occurred.
The real 14-day billing guard and cancellation rules remain in the billing plan;
this patch does not silently turn on live billing or send emails.

Before live launch, finish provider-hosted authorisation, verified callbacks,
server entitlement enforcement, merchant/support information, confirmation and
seven-day reminder delivery, actual cancellation and reconciliation. Those are
functional integration tasks, not cosmetic housekeeping.

## How to evaluate the design

The placement after sign-in is the requested product hypothesis. Once live
payment authorisation exists, evaluate: sign-in to offer exposure, offer to
verified card authorisation, first lesson/practice completion, cancellation
before charge, first successful payment, retained paid users and support/refund
contacts. Segment adult payers and learners responsibly. Exclude preview activity
from paid-conversion metrics. Avoid equating card capture with satisfaction.

A controlled future comparison can evaluate this offer against a version shown
after a completed sample lesson. Keep price and trial terms constant, define a
primary retained-payment outcome in advance, and do not choose a winner from
small early fluctuations. No analytics collection or experiment is activated by
this patch.

## Verification record

The shared browser auth checks now exercise new-member routing, active-member
routing, old dashboard destinations, safe deep links and a failed membership
lookup that preserves sign-in. Controller checks cover all three successful
entry points: email login, email signup and OAuth profile completion. Landing
checks include the active-member Continue learning action.

The full backend run passed 399 tests and exposed one old test that still
expected the retired dashboard renderer. Its assertion was updated to the
landing catalogue, then the affected auth/billing/page suite passed 20 tests,
including a new production-preview isolation check. Relevant frontend suites
also passed. No claim is made that live Google/Apple callbacks or live payments
were re-exercised in the browser.

Browser QA used an isolated synthetic account and a temporary session-bootstrap
fixture outside the repository. It verified restored sign-in → membership
offer → unchecked consents → payment preview → access confirmation → agreed
landing page, followed by returning-member sign-in → landing page. The fixture
and preview launcher were excluded from the patch. Desktop visual review
prompted moving the purchase panel up so its price and action are prominent.
Mobile layout rules were added, but a mobile viewport still needs device QA.

Apply after Athena_14_Day_Trial_and_Paywall.patch. No migration is required for
this correction. The local unlock patch remains compatible. Sign out before
testing a fresh sign-in. An account that already activated an access preview
will correctly go straight to the landing page; use a new local account to
review the initial offer. Manage an existing preview through Account.
