# Debate Arena (working name)

Use Debate Arena to compare hackathon ideas, projects, learning paths, or research topics in Discord. The agents debate the options, assess your readiness, check the evidence, and rank the options. Humans make the decision.

## How Switch is used
Switch bridges the existing Discord channel to a room. Codex runs the Moderator, Scout, Advocate A, Advocate B, Coach, Fact-Checker, and Judge on the host Mac. The Moderator coordinates their named handoffs. Teammates use the workflow by addressing the Moderator in Discord.

## Existing Discord setup

1. Open the installed Switch Console from Applications. If the Local Switch server shows **Not running**, select **Start** and wait for **Running**.
2. In **Templates → Import template**, choose the [Debate Arena template](switch/templates/debate-arena.template.yaml). Save it privately, choose **Use template**, select **This computer**, and create the seven agents.
3. From each agent’s **Agent settings → Add to room**, select **general · Discord** on the **Astralis Discord** bridge. Verify the agents under **Your Rooms → Astralis Discord → #general → Configuration → Participants**. Reuse the room and bridge.
4. In the Moderator’s **Agent settings → Who can talk to your agent → Custom rules**, edit the existing owner and owned-agent rule. Set **Rooms → Specific → general** first. Confirm the room is selected, then set **Users → Any** and keep **Agents → My agents**. Apply the rule. Any human who can join that Discord channel can then address the Moderator there. On a room with a wider audience, use explicit teammate identities. The six specialists use **Me and my agents** so the Moderator can reach them by name.
5. In `#general`, have each teammate select `@debate-moderator` from mention suggestions and send `DA-ACCESS`. Each account should receive `DA-ACCESS-OK`. This check does not open a case.

If the room picker does not accept input, the Switch admin can use `!invite-agent @agent-name` in the target channel for each existing agent. Use `!list-agents` or the Console’s **Participants** view to check membership. After the Moderator has replied successfully in Discord, use `!remove-agent @astralis` to take the old Cursor agent out of this room.

See the [verification log](docs/RESULTS.md) for the live deployment status and any remaining access checks.

## Start a case and vote

Tag `@debate-moderator` with a mode and your question. For example, `@debate-moderator LEARNING Should I keep learning Python or start Rust?` Include your goal, hours per day, deadline or none, examples of what you can already do, and constraints. For Learning, include what you currently study. For Project, include your proposed idea if you have one.

When the Moderator opens the ballot, tag it with the case ID and `A` or `B`. The case owner tags it with the case ID and `CLOSE` to end voting. The Moderator posts the tally and gives the result. The default report folder is `reports/` within the Moderator’s configured working directory on the host. If writing is unavailable, the Moderator posts the report in Discord.

**Session 3 in progress:** the workspace template specifies round-specific ballots (`<case-id>-R1` and `-R2`) with `A`, `B`, or `MORE INFO`; the live Moderator still needs its instructions updated and the two-round flow verified. A first-round MORE INFO majority or no majority triggers one evidence pass; a second ballot without an A/B majority ends pending. Follow the Moderator's actual prompts until the live update is verified. No agent votes count.

## Verify sources
Run `python3 tools/verify_sources.py --file <path-to-report.md>` from the project directory to check URL reachability. The Fact-Checker evaluates whether a source supports its claim.

## Limits (be honest)
Research gaps are candidates. Time estimates are labeled. The persona checks are defined in [the evaluation protocol](tests/EVAL.md).
