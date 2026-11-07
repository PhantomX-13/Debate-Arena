# Debate Arena (working name)

Use Debate Arena to compare hackathon ideas, projects, learning paths, or research topics in Discord. The agents debate two options, assess readiness, check evidence, and rank the options. Group members can share attributed opinions and evidence before the debate; humans make the decision.

## How Switch is used
Switch bridges the existing Discord channel to a room. Each of the seven roles runs as a Switch agent; Switch routes the named handoffs and messages. The checked team setup used Codex on the host Mac. The prompts and rubric are separate from the model, but this repository does not yet include its own model API adapter. See [provider setup and limits](docs/PROVIDERS.md).

## Clone and run the local checks

The Python utilities use only the Python standard library. No third-party Python packages or paid API key are required for the local vote-tally and URL-check tools.

```sh
git clone <repository-url>
cd debate-arena
python3 -m unittest discover -s tests
python3 tools/verify_sources.py --file reports/<case-id>.md
```

The standalone text client in `tools/model_provider.py` can also check an OpenAI-compatible endpoint. Set `DEBATE_ARENA_BASE_URL` and `DEBATE_ARENA_MODEL`, add `DEBATE_ARENA_API_KEY` only if the endpoint requires it, then run `python3 tools/model_provider.py "Reply with one sentence."`. This client does not run the Discord debate workflow; see [provider limits](docs/PROVIDERS.md).

To run the full Discord workflow, install Switch Console, connect a Discord bot/room, and create the agents from a template. The verified template uses Codex. For model choice through OpenCode, install OpenCode and its Switch connector, then import `switch/templates/debate-arena-opencode.template.yaml` and configure your model in OpenCode. A local model can avoid per-request API fees when a compatible server and sufficient hardware are available. The OpenCode template has not yet been verified in the team Discord room. See [provider setup and limits](docs/PROVIDERS.md).

For the example local setup, install Ollama, run `ollama pull gemma3:4b`, copy `switch/opencode.local.example.jsonc` to `~/.config/opencode/opencode.json`, then use the OpenCode template. This requires no model API key, but the model runs on your own hardware. Run the handoff and complete-case checks in the provider guide before relying on it.

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

After the Moderator presents the two options, anyone can mention it to share an opinion or source about either option. The Moderator credits contributors and asks the Fact-Checker to check factual claims where possible. When the group is ready, the person who started the decision mentions the Moderator and says **Start**.

When voting opens, mention the Moderator and say **Option A**, **Option B**, or **More info**. The person who started the decision mentions the Moderator and says **Close** to end voting. Each verified human's latest valid vote in that round counts once. The Moderator posts the tally and gives the result. The default report folder is `reports/` within the Moderator’s configured working directory on the host. If writing is unavailable, the Moderator posts the report in Discord.

**Session 3 status:** live Discord cases verified both final outcomes: an A/B choice after one MORE INFO pass (`DA-7F07-L5`) and a PENDING result after the second round also returned MORE INFO (`DA-7F07-L6`). A teammate also ran and retrieved a report in `DA-7F07-L7`. The latest Project case (`DA-7F07-P1`) exercised the optional group-input invitation, the short answer plus detailed review, and one MORE INFO follow-up. No teammate submitted optional contributions in that case; its final round still needs the Moderator to acknowledge the owner's posted `CLOSE` and save the final report. See [the verification log](docs/RESULTS.md). No agent votes count.

## Verify sources
Run `python3 tools/verify_sources.py --file <path-to-report.md>` from the project directory to check URL reachability. The Fact-Checker evaluates whether a source supports its claim.

## Limits (be honest)
Research gaps are candidates. Time estimates are labeled. The human-readable first-page summary is followed by a detailed review for teammates. The persona checks are defined in [the evaluation protocol](tests/EVAL.md).
