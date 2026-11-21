# Debate Arena — AI handoff for a blog and demo

Snapshot: November 7, 2026, Bangladesh time. Share this file with a teammate or upload it to another AI assistant. The team should check the current Discord case and repository before publication.

## Instructions to the receiving AI

Help the human write their own first-person blog and plan a three-minute demo. Ask what they personally configured, learned, and can show. Do not invent quotations, screenshots, metrics, implementation details, or successful runs. Identify uncertain claims and distinguish live evidence from scripted previews. The team owns any publication or submission.

An organizer email supplied by the team stated that submissions close on November 7 at 11:59 PM IST. An earlier project note described Best Blog criteria as clarity, accuracy, and usefulness. Verify the deadline, eligibility, track requirements, and current judging criteria on the [official event page](https://www.wemakedevs.org/hackathons/switch#tracks).

## Product

Debate Arena helps a person or group compare two choices in a Discord room. It gathers the person's goal, available time, deadline, experience, and constraints. Specialized agents research the options, argue both sides, assess readiness, check sources, and score the choices. Teammates can contribute opinions and evidence before the debate, review the reasoning, and vote.

Example: a student wants a portfolio showing Python and backend skills and is choosing between a budget tracker and a study planner. The product compares their tradeoffs for that student's circumstances. The student decides how to build the chosen project.

Four modes are supported:

- Hackathon compares ideas against event criteria and applies a feasibility cap when an option cannot be built in time.
- Project compares distinct projects, including the student's own idea when provided. Its weights are future value 40%, goal and skill fit 25%, feasibility 25%, and scope realism 10%. The student chooses the implementation.
- Learning considers the person's current studies, goals, readiness, and time. The Coach can recommend proceeding, staying on the current path, learning prerequisites first, or waiting.
- Research compares feasible topics, related work, candidate gaps, resources, and prerequisite readiness.

The intended result starts with a concise recommendation, its main reason, and uncertainty, followed by a detailed review. People make the final choice. A More info vote can trigger one focused evidence pass and a second ballot. If neither option wins a majority in the second ballot, the decision remains pending.

## Architecture and why Switch matters

The verified team deployment uses Discord, Switch Console, a local Switch server on the team lead's Mac, the Switch Discord bridge, and Codex as the agent provider. The Mac and local server need to run for this setup.

A person mentions the Moderator in the Discord general channel. The bridge brings the message into the Switch room. Switch starts the addressed agent and routes named handoffs among agents in the shared room. The team can follow replies, add input, and vote there. The project provides the role prompts, rubrics, report format, and local verification utilities.

| Agent name | Responsibility |
| --- | --- |
| debate-moderator | Intake, coordination, group input, voting, and final report |
| debate-scout | Options, research, and source URLs |
| debate-advocate-a | Argument and rebuttal for Option A |
| debate-advocate-b | Argument and rebuttal for Option B |
| debate-coach | Prerequisites, readiness, time, and constraints |
| debate-factchecker | Opens sources and checks claims |
| debate-judge | Applies the rubric, ranks options, and explains uncertainty |

These are separate Switch-managed agents with different role instructions. The verified live deployment used the same Codex provider for the roles. Do not describe them as seven different model vendors. A multi-agent debate does not guarantee a correct or unbiased result.

Switch targeted handoffs are visible to the room. A recent run exposed internal case and stage codes. Updated project templates request plain-language handoffs, but the updated specialist instructions have not all been applied and verified in the live Switch agents. Switch-generated thread names and provider error messages are separate runtime behavior.

## What the team did in Switch

The team used Switch Console 0.40.1 and an existing Discord server, bot, bridge, and general channel.

1. Started the local Switch server and checked the Discord room.
2. Tried the existing Cursor-backed astralis agent. Discord created a thread and showed activity without a substantive answer. Earlier project notes report a Cursor plan-limit message in Switch activity.
3. Used Codex and a small test agent to verify a Discord round trip.
4. Imported a two-agent gate-test template. Automatic room attachment failed because Switch reported it could not see the selected room. A revised template created the agents first, and the team attached them manually from each agent's settings.
5. Tagged the Scout test agent. It opened an IANA page and handed off to the Checker, which checked a supported claim and a contradicted claim. Both replies appeared in Discord.
6. Created seven product roles from the Debate Arena template, attached them to the room, and configured Moderator access for the teammates. Both teammates reported receiving the access-test reply.
7. Exercised the four modes, voting, and the focused follow-up. Details and caveats are in the project results notes.

A new user needs Switch, a supported provider, a Discord bot and bridge, room access, and the project configuration. The team's existing bridge should not be described as a setup the project created from scratch. Refer to the current [Switch quickstart](https://docs.switchagents.ai/switch-rooms/getting-started) and [Discord bridge guide](https://docs.switchagents.ai/switch-rooms/deploy/messaging-apps/discord).

## Verified evidence and limitations

- A real Scout-to-Checker handoff appeared in Discord. The Checker distinguished a supported documentation claim from a contradicted public-registration claim using the IANA source.
- Two teammates voted in an early human ballot. A later teammate-led Learning case produced a report attachment, and the owner reported that the teammate downloaded it.
- Learning, Project, Research, and Hackathon cases were exercised. Consult docs/RESULTS.md for the precise checks before claiming every acceptance condition passed.
- Live More info cases recorded both an eventual A/B decision and a pending decision after a second ballot.
- Beginner and experienced Python profiles received different Coach verdicts for Rust in recorded runs. This is an example of profile-sensitive behavior, not an accuracy measurement.
- A Project case showed the optional group-input invitation and a short answer followed by a detailed review. The recorded input window was empty, so attributed teammate claims were not independently observed in that case. The owner accepted that limitation.
- A recent budget tracker versus study planner case progressed through Scout and both Advocates after their stale sign-in copies were repaired. Their replies still exposed internal codes. The Coach then hit a Codex usage limit. A retry was suggested after 10:29 PM Bangladesh time on November 7. The final outcome was not confirmed in this handoff.
- A revoked Codex refresh token had stopped the Moderator and Scout. Switch stored separate session sign-in copies. The stale copies for the seven Discord-room roles were moved aside with backups so Switch could recreate them from the refreshed login. The Moderator, Scout, and Advocates subsequently ran. Later roles and long-term token behavior remain to be verified.

The URL verifier checks link reachability. It does not by itself establish that a page supports a claim. The Fact-Checker compares claims with source content and should mark inaccessible or unsupported claims honestly. Future value, time estimates, and research gaps are judgments or candidates. The project has no measured accuracy percentage.

## Model choice and costs

The verified Discord workflow used Codex. An OpenCode template and a small OpenAI-compatible text smoke client exist in the repository. They do not prove that every vendor works in the full debate.

On the team lead's Apple M1 Mac with 8 GB memory, Ollama 0.40.15 ran Gemma 3 locally. OpenCode reported that this Gemma model did not support tools for its agent flow. Qwen3 4B was then downloaded and produced a response through Ollama and a simple OpenCode text request. A completed OpenCode tool call was not confirmed. Switch detected OpenCode 2.2.6 but reported that sign-in could not be checked and blocked the OpenCode smoke-test agent. The team continued with Codex.

A local model can avoid model API charges, but a complete no-paid-key Switch/Discord debate has not been verified. Hardware requirements, model quality, tool support, provider terms, and hosted free tiers vary. Browser-based Transformers.js/ONNX is not integrated into the live workflow. Do not claim universal provider support.

## Suggested blog structure

1. Open with a real decision and why competing options are hard to assess.
2. Explain the product's four modes and how people contribute and decide.
3. Follow one real Discord message through Switch, the Scout, and the Checker. Explain the shared room and named handoffs.
4. Describe the actual setup, including the existing bridge, provider, template, room membership, and access rules.
5. Explain what broke and what the team observed: the Cursor response, failed automatic room join, revoked session credentials, and usage limit.
6. Show real evidence such as the IANA handoff, human vote, report attachment, or a verified More info case.
7. Discuss source-checking limits, provider limitations, public handoffs, and what remains to be verified.
8. Close with the writer's own lessons. Ask them about their actual contributions and experience.

## Three-minute demo planning outline

Use a real working case when available. If recording an existing case, disclose meaningful cuts. Label prototype.html and feedback-preview.html as scripted previews.

| Time | Visual | Message |
| --- | --- | --- |
| 0:00–0:20 | Title and decision question | Introduce a real choice. |
| 0:20–0:45 | Discord request and profile | Show the goal, time, experience, and constraints. |
| 0:45–1:15 | Switch Console and roles | Explain the local server, bridge, and named handoffs. |
| 1:15–1:50 | Real Scout, Advocates, Coach, and Fact-Checker output | Show sources and a clear tradeoff. |
| 1:50–2:20 | Judge summary and detailed review | Explain the recommendation and uncertainty. |
| 2:20–2:45 | Human vote, report, or a recorded More info pass | Show that people decide. |
| 2:45–3:00 | Architecture and limitation | Explain what Switch connects and name a verified limit. |

Before filming, confirm that agents respond, the provider has sufficient usage, the report is retrievable, and the wording shown is actually live. Prepare a backup recording of a verified earlier case. Remove private information and unrelated conversations from footage. The user may record their own voiceover.

## Repository guide

- README.md — setup and workflow.
- docs/RESULTS.md — recorded tests, historical case IDs, and limitations.
- docs/BLOG_HANDOFF.md — earlier detailed blog material and gate-test fixture. Some status details predate later tests.
- docs/DEMO.md and tests/EVAL.md — demo and evaluation notes.
- switch/templates/debate-arena.template.yaml — Codex role instructions.
- switch/templates/debate-arena-opencode.template.yaml — prepared OpenCode alternative, not live-verified.
- tests/fixtures/switch-gate.template.yaml — foundation test fixture.
- tools/verify_sources.py — URL reachability utility.
- tools/tally_votes.py — local transcript tally utility, which uses its own ballot-ID format.
- prototype.html and feedback-preview.html — scripted interactive previews.

Inspect current files and Discord evidence before treating this snapshot as current. Never include tokens, credential files, raw account IDs, or private messages in public materials.
