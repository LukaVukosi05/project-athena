# Landing and shared footer cleanup

The landing page now ends after its hero and three teaching principles. The blue grade catalogue, learning-path explanation and repeated trial offer have been removed, matching the cutoff in the supplied recording. Grade links remain in the hero; the underlying curriculum and lesson content are unchanged. Member continuation and the post-sign-in membership decision are preserved.

All 14 application pages load one shared footer renderer in `frontend/js/engine/footer.js`. It uses the existing brand tokens, a restrained white surface, learning and account links, a current-year copyright line and responsive columns. It is independent of authentication and API responses. Retired dashboard/welcome redirect documents retain their immediate redirects rather than rendering a transient footer. Removed page-specific footers no longer expose development notes. No contact addresses, policy destinations or trust claims were invented.

## Validation

- All 110 frontend test files pass, including authentication, membership, practice and lesson renderers.
- Shared shell checks ensure exactly one footer on every application page and valid local destinations.
- Landing tests cover active members, non-members, guests and temporary membership lookup failure.
- Both targeted backend static-serving/past-paper tests pass.
- Development static-serving regression now checks the grade page's backend catalogue integration instead of the deleted landing catalogue.
- Browser automation is unavailable in this session; desktop and mobile visual review remain part of local acceptance.

## Apply

Apply `Athena_Landing_and_Shared_Footer.patch` after the membership layout cleanup patch. Stop the local application, run `git apply --check`, then `git apply`, and restart with `tools/run_auth_test.ps1`. No database migration or dependency change is required. Use a hard refresh after restarting.
