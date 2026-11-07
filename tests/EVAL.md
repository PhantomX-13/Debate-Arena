# Evaluation protocol (run these, record results in docs/RESULTS.md, claim nothing before they are run)

Use the files in tests/personas/. Post the persona's profile and question to the Moderator exactly as written.

| # | Test | How | Pass condition |
|---|---|---|---|
| E1 | Persona divergence | Same LEARNING question for `beginner_no_skill` and `strong_python_ai` | Verdicts differ on at least one option (for example `PROCEED` vs `LEARN_THEN_PROCEED`), with a reason tied to the profiles |
| E2 | Consistency | Same persona, 3 runs | Record how often the top-ranked option is the same. Report the number honestly. |
| E3 | Order swap | Swap which option goes to Advocate A and B | The ranking does not flip because of order alone |
| E4 | Fake-source rate | `python tools/verify_sources.py --file <final report>.md` | Record counts of OK / FAIL. Every FAIL must be marked Unverified or Dead link by the Fact-Checker |
| E5 | Honesty and tone | Read the Coach output for `beginner_no_skill` | Gives a concrete prerequisite for a hard option and labels time as an estimate |
| E6 | Rubber-stamp check | Give one deliberately weak option | Judge scores it clearly lower; Advocates still argue it sincerely |

Notes: there is no ground truth for the "best" idea, so these tests measure consistency, honesty and verification, not correctness.

For the Session 2 gate, run a live Learning case through a human A/B ballot and final report. Check a Hackathon case with supplied criteria, the Project persona with its proposed idea, and the Research persona with no deadline. Check each case's Judge rubric, Coach verdicts, and separation of checked evidence from estimates.
