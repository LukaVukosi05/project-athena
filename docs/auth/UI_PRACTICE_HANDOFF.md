# Learner home and practice library

Base: 180bb855f4fefc75d125d9338be7f52f76556607 (auth/session feature).
Apply after the auth patch. Compatible with Athena_Unlock_Local_Lessons.patch;
the launcher and unlock setting are not changed by this UI patch.

## Behaviour

- The logo and Learn both link to index.html, the public introduction shown at the start of the reference video.
- welcome.html redirects to index.html; the learner dashboard remains at dashboard.html.
- Switching grade on the dashboard keeps the dashboard layout.
- Practice opens practice.html, with grade, topic, and lesson selection.
- One practice set appears at a time; Choose another lesson returns to the list.
- The existing self-guided engine handles multiple-choice and written answers,
  hints, feedback, worked solutions and marking. Questions are not duplicated.
- A read-only /api/v1/practice/catalogue/grades/{grade_id} endpoint lists counts
  from the registered question banks, with no answers or question payloads.
- A lesson without a registered bank says so and links back to its teaching.
- The grade selector is a browse filter. It does not change the account grade.

## Verification

393 backend tests passed with ATHENA_UNLOCK_ALL_LESSONS=true and an isolated
SQLite test database. Without that setting, 34 existing preview tests expect
public access and fail on subscription gates; they pass with the same development
configuration used by the local launcher. Entitlement tests separately restore
and verify the locked configuration.

Frontend checks passed: practice hub (catalogue rendering, missing banks,
session launch, stale grade requests and errors), curriculum pages, shared layout,
self-guided practice, hint progression and renewable authentication.

Browser QA with a disposable local display fixture verified the Grade 11 list,
opening a question, submitting a correct multiple-choice answer and receiving
feedback, returning to the list, and switching to Grade 12. The fixture and
preview configuration were removed before packaging. Real Google/Apple flows
and mobile viewport rendering were not retested for this UI patch.

No curriculum source, generated lesson file, authored practice bank, scoring rule
or database migration is modified.

## Local test

Stop the server, apply from the repository root with git apply --check first,
then restart tools/run_auth_test.ps1 and use Ctrl+F5 in the browser.
Visit http://127.0.0.1:8000/ and the Practice tab. Confirm the logo and Learn
return to the same introduction page, then try a grade, topic and lesson practice set.
