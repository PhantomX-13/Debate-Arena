# Debate Arena — Flip the Switch Best Blog handoff

**Status as of November 7, 2026:** The Switch and Discord foundation passed Session 1, all four decision modes have been exercised, and live `MORE INFO` cases ended in A, B, and `PENDING`. A teammate-led Learning case also produced a report attachment. A later Project case exercised the group-input invitation with no teammate contributions; its round-2 close is awaiting the Moderator's final acknowledgement. This is a reference pack for the teammate writing the article. You can read it on its own, upload it to an AI tool, or use the repository links if you have the project files.

## What the organizers want

WeMakeDevs calls the side track **Best Blog**. Publish a post about building with Switch that walks through what you made, how you set it up, and what you learned. You can enter it on its own or alongside a main track. The prize listed is AirPods 5. The event FAQ lists the submission deadline as **November 7, 2026, at 11:59 PM IST** (November 8 at 12:29 AM in Bangladesh). Confirm the submission form and where to put the public article URL in the event portal before submitting. [Official tracks](https://www.wemakedevs.org/hackathons/switch#tracks) · [Event FAQ](https://www.wemakedevs.org/hackathons/switch#faq)

| Best Blog criterion | How the article can show it |
|---|---|
| Clarity | Follow one message from the human to the Scout to the Checker and back to Discord. Define the room, the bridge, and the agent provider as they appear. |
| Accuracy | Show the exact handles and expected output. Explain the Cursor provider failure, the Codex workaround, and why the team attached the agents manually. Label the voting test and the planned full workflow separately. |
| Helpfulness to a first-time Switch user | Give setup steps, a copyable YAML fixture and Discord prompt, and a way to tell a progress message from a completed reply. Link to the official Discord guide for people starting from scratch. |

The event also lists four **general project** criteria: use of Switch, technical execution and reproducibility, creativity and impact, and presentation. Best Blog has the separate criteria above. Use the general criteria to decide what evidence to show, and leave scoring percentages out of the article. [Official judging section](https://www.wemakedevs.org/hackathons/switch#judging)

## The problem and what Debate Arena is for

Students often have to choose between two worthwhile paths without a clear way to weigh the evidence against their own goals, skills, time, and deadline. Debate Arena is designed to make that decision a team discussion in Discord. Two agents argue competing options, a Coach assesses readiness, a Fact-Checker checks sources, and a Judge scores the choices. Humans see the reasoning and make the final decision. In Project mode, the team helps the student choose **what to build** for the best expected future value. The student chooses **how to build it** so the work remains a learning experience.

A good example for the article is a student choosing what to learn next while already studying something else. The useful question is how the answer changes when the same option is assessed for a beginner and for someone with more experience. Use this as a product example until the team has two real runs to cite.

## Why Switch is central to this build

| Piece | Its job in this project |
|---|---|
| Discord | The team’s existing interface. People post requests, see the agents’ replies and source links, and cast votes from their own accounts. |
| Switch Console and local server | The Console manages the local server, agent providers, instructions, room membership, and templates. The server handles the shared room and routes messages to the agent being addressed. Our test agents ran on the team lead’s Mac. |
| Switch’s Discord bridge | Connects an existing Discord channel to a Switch room. The bridge receives Discord messages and mirrors agent replies back. One Discord bot serves the connection. Switch uses a channel webhook for replies under each agent’s own name and avatar. An agent mention can be presented as a Discord role so its name autocompletes. |
| Codex | Runs each test agent’s turn and follows its role instructions. The Scout and Checker use the same provider with different prompts and names. Switch handles how the turns connect to Discord and to one another. |
| Debate Arena files | The YAML defines agent roles and settings. The intended product rules live in its prompts and rubric. Two Python utilities handle local transcript tallying and URL reachability checks. |

**Follow a real message:** a teammate mentions `@debate-gate-scout` in Discord → the bridge brings that message into the Switch room → Switch starts the Scout’s Codex turn → the Scout posts a visible reply with a named Checker handoff → Switch starts a separate Checker turn → the Checker’s reply appears in the same channel. The second turn was triggered by the agent handoff, with no second human prompt. Both replies could be read by the team. [Switch Discord bridge docs](https://docs.switchagents.ai/switch-rooms/deploy/messaging-apps/discord) · [How Switch works](https://docs.switchagents.ai/switch-rooms/using/how-switch-works)

If you take Switch out of **this implementation**, you lose the Discord-to-agent routing, role identities, named handoffs, and shared room where humans watch the work. The YAML, Codex, and local scripts would still exist, but the Discord workflow would need a replacement bridge and agent runner. This is why the project depends on Switch. The underlying model, the decision rubric, and the human vote each have their own role.

## The setup we actually used

Session 1 used **Switch Console 0.40.1**, the local server on the team lead’s Mac, and the existing **Astralis Discord** connection to the team’s `#general` text channel. We reused the bot and channel.

1. **Start the local server and find the room.** Open Switch Console, start the **Local Switch server** if needed, and wait for **Running**. Open **Your Rooms → Astralis Discord → #general → Configuration** and check the participants. Keep the host Mac available while running the test.
2. **Verify the provider before writing product prompts.** We tagged the existing Cursor-backed `@astralis` first. Discord showed a thread and a timing message, but there was no substantive reply. Switch activity showed Cursor’s “Upgrade your plan to continue” message. That explained the failed turn and gave us a reason to test another provider.
3. **Get Codex detected.** Codex was already signed in through ChatGPT and answered a standalone CLI test. On this Mac, Switch initially could not find the executable bundled with the installed app. We made it visible through a user-local symlink at `~/.local/bin/codex`, then used **Settings → Agent providers → Refresh agent detection**. This was a fix for our machine. If Codex already shows up, skip it. On a fresh machine, follow the provider setup guide. [Set up agent providers](https://docs.switchagents.ai/switch-rooms/getting-started/set-up-agent-providers)
4. **Test one agent from end to end.** We created `@debate-codex-test` with Codex and owner access, checked it in a private Switch chat, and then joined it to the Discord room. The owner asked for `DA-CODEX-OK` in `#general` and got that exact reply. The original `@astralis` stayed on Cursor.
5. **Provision the two roles.** Open **Templates → Import template**, paste the YAML from the appendix, and create both agents with **This computer** as the machine. We used a private template named **Debate Arena Gate Test – Manual Join**. The first version tried to use `join: ["{target_room}"]`. It previewed `general`, then reported that no room of that name was visible and created neither agent. The revised fixture creates the two agents without an automatic room join. Template visibility controls who can reuse the template. Agent addressing is a separate setting. The fixture uses `owner-agents`, and the role instructions tell the Scout to take the owner’s test request and the Checker to take the Scout’s handoff.
6. **Attach the agents to the existing room.** For each new agent, open **Agent settings → Add to room**, search for `general`, select **general · Discord**, and click **Add to rooms**. Check that both agents are listed in the room’s participants. The validated route was from each agent’s settings. If you’re replaying this in the team’s existing room, use the agents that are already there.
7. **Run the handoff from Discord.** As the owner, open the `#general` text channel. Select the Scout from the Discord mention suggestions and send `@debate-gate-scout DA-GATE`. Look for `DA-GATE-SCOUT` with a mention of the Checker, then `DA-GATE-CHECKER` without a second human request. Check the channel and its threads for replies. A `Worked for ...` message by itself only shows that a turn finished.

For a first-time reader without a Discord bridge: follow the current Switch quickstart to get a local server and provider running. The official Discord guide walks through adding a bot, enabling its member and message-content intents, setting the permissions for replies, webhooks and mention roles, then connecting it in Switch with the bot token and Discord server ID. Link the Discord account you’ll use as the owner and post a message in the target channel so Switch creates the room. This is the documented fresh setup path. Our team started with that bridge already in place. [Switch quickstart](https://docs.switchagents.ai/switch-rooms/getting-started) · [Connect Discord](https://docs.switchagents.ai/switch-rooms/deploy/messaging-apps/discord)

## What we saw and what you can show

| Check | Verified result | Evidence to use |
|---|---|---|
| Discord round trip | `@debate-codex-test` (Codex) returned `DA-CODEX-OK` at 10:50 AM Dhaka time. | Search `#general` for `DA-CODEX-OK`. |
| Named handoff | At about 3:00 PM Dhaka time, the owner tagged `@debate-gate-scout` (Codex). Its reply tagged `@debate-gate-checker` (Codex), which then replied. | Search `#general` for `DA-GATE-SCOUT` and `DA-GATE-CHECKER`. The original screenshot shows both replies. For a clean reproduction, use the intended `DA-GATE` prompt. |
| Source verification | Both cited IANA. The Checker reported opening the page independently. It marked the documentation claim **supported** and the public registration claim **contradicted**. One reachable source produced two different claim verdicts. | Pair the two replies with the [IANA Example Domains page](https://www.iana.org/help/example-domains). |
| Template and room attachment | The revised YAML provisioned both agents. Manual attachment put both in the existing channel and both posted there. | A Switch Console screenshot showing **Configuration → Participants** and the two agents. |
| Teammate participation | Two teammates cast `DA-VOTE-01 A` and `DA-VOTE-01 B` from separate human accounts at 3:17 and 3:18 PM Dhaka time. The tally was **A 1, B 1**, so there was no majority. | Search for `DA-VOTE-01`. Describe it as a separate test ballot. The transcript was tallied locally. |

The local script `tools/tally_votes.py` takes a chronological JSON transcript with `author_id`, `author_type`, and `content`. Given verified author metadata, it counts each human’s latest valid A/B vote for the selected ballot. Its two unit tests passed again during this handoff. This shows the counting rules locally. Integration with a live Moderator is still pending. `tools/verify_sources.py` checks URL reachability and can look for expected terms. A reachable page can still contradict a claim. The verifier’s loopback HTTP test could not start in this review environment because socket binding was restricted. A real final-report verifier run belongs to the next evaluation session. [Project verification log](RESULTS.md)

For the post, use the Scout and Checker replies as the main screenshot. If possible, also show the two agents in **Participants** and the human test ballot. Crop or redact private Discord names, IDs, invite links, account information, and any unrelated chat before sharing. Use the team’s screenshot or a fresh run. The standalone handoff contains the evidence to look for and the public source.

## The product roadmap

**The full decision workflow** runs in one Discord room per active case. The Moderator asks for the student's goal, available time, deadline, skill evidence, current learning where relevant, and constraints. Scout proposes candidates and sources. The Moderator fixes two options, invites optional attributed opinions/facts from group members, then starts the debate. Both Advocates make openings and rebuttals; the Coach assesses readiness; the Fact-Checker checks claims; and the Judge applies the selected rubric. The result starts with a concise recommendation and includes a detailed review for teammates. Humans vote and the Moderator saves a Markdown report under `reports/`, or posts it in Discord if file writing is unavailable.

| Mode | Agreed behavior |
|---|---|
| Hackathon | Use the event criteria where provided or the project’s existing default rubric. Cap the score when an idea cannot be built in time. Keep the existing Hackathon Coach verdicts. |
| Project | Compare distinct projects that serve the same goal, including the student’s proposed idea when provided. Weigh expected future value **40%**, fit with goals and skills **25%**, feasibility in the available time **25%**, and scope realism **10%**. Identify what to learn first and what can be learned during the build. The student chooses how to build the project. |
| Learning | Capture what the student is already learning. Rank each option and give it `PROCEED`, `SKIP_FOR_NOW`, `LEARN_THEN_PROCEED`, or `NOT_NOW`. Use `SKIP_FOR_NOW` if staying on the current path is a better use of time and `NOT_NOW` if the option falls outside current readiness or constraints. |
| Research | Compare feasible topics, cite the closest related work, and label gaps as candidates. Use prerequisites and available hours to recommend starting, preparing first, or a longer learning plan. Estimate a deadline if the student has none. |

The product template uses the names `debate-moderator`, `debate-scout`, `debate-advocate-a`, `debate-advocate-b`, `debate-coach`, `debate-factchecker`, and `debate-judge`. The three live Session 1 test agents are the ones in the evidence table. Check the verification log for later provisioning and Discord results before describing the product roles as operational.

**Session 3** adds `MORE INFO`. If it wins the first ballot, or the first ballot has no A/B majority, the Moderator asks what evidence would help. The Scout investigates that question, the Fact-Checker checks new claims, and the Judge updates the ranking if warranted. Humans vote again on the same A/B options. Live cases `DA-7F07-L3` and `DA-7F07-L5` ended in A and B, and `DA-7F07-L6` ended `PENDING` after no A/B majority in round 2. Beginner and experienced profiles gave different Coach verdicts for Rust in the tested runs. Local URL-verifier tests cover an unreachable URL and a reachable page missing an expected term. The Project case `DA-7F07-P1` also demonstrated the optional group-input invitation and owner completion gate, but the contribution window was empty; actual teammate opinions and factual claims still need a live test. Its round-2 close awaits Moderator acknowledgement. The HTML prototypes are scripted; they do not connect to Switch or run live research.

## Provider portability and cost

The role prompts and rubrics are not tied to a particular model, but the current Switch template pins `provider: codex` and the verified live setup used Codex. A clone can select another provider detected by its Switch installation by editing the provider field and authenticating it in Switch Console, then checking handoffs and tool access. This repository does not yet implement direct adapters for arbitrary OpenAI-compatible endpoints, every listed vendor API, or in-browser Transformers.js/ONNX. Local models may avoid API usage charges only when a compatible installed Switch provider can run them; hardware, model downloads, provider setup, and each model's license still apply. See [provider setup and limits](PROVIDERS.md).

## A structure the author can adapt

1. Start with the student decision problem or the moment the Checker answered the Scout in Discord. Add a detail from your own role on the team.
2. Explain the message path and what would have to be rebuilt if you removed Switch. A screenshot with arrows or a short diagram is enough.
3. Show the setup with the two real problems: Cursor finished a turn without a usable answer, and Switch rejected the automatic room join. Show how changing providers and attaching the agents manually made the next run work.
4. Give the exact replay prompt and expected outcome. Explain how to read the evidence and the difference between a successful run and a status message.
5. End with what the team learned, what humans did, and what remains to be tested before the full decision workflow is ready. Add a public repository or demo link once the team has one it can share.

If you use an AI tool, upload this Markdown file or paste it as text. An example prompt:

> Read the attached handoff as source material. Help me plan my own Flip the Switch Best Blog post. Give me an outline, point out which claims I can support with the recorded Discord evidence, and ask me what I personally did or learned. Walk me through reproducing the two-agent test if needed. Keep observed results, official Switch behavior, and planned product features distinct. Flag any detail that needs a screenshot or confirmation before publishing. I will write the article myself.

## Project references

These paths work when the handoff is opened inside the project. A teammate with just this Markdown file can use the appendix and public links above.

- [Session 1 verification log](RESULTS.md) and [existing-room setup in the README](../README.md)
- [Verified two-agent YAML fixture](../tests/fixtures/switch-gate.template.yaml) and [seven-role product template](../switch/templates/debate-arena.template.yaml)
- [Local ballot tally](../tools/tally_votes.py) and [URL checker](../tools/verify_sources.py)
- [Scripted HTML prototype](../prototype.html), [evaluation protocol](../tests/EVAL.md), and [report skeleton](../reports/TEMPLATE.md)

## Appendix — copyable two-agent template

Save this as `switch-gate.template.yaml` or paste it into the Switch import form. Choose your local machine, then attach both agents to the existing Discord room as described above. The YAML contains the exact agent names and the handoff prompt used for the test.

```yaml
version: 2
# Create the agents first, then attach them using the room's Add agent control.
params:
  machine:
    type: machine
    default: [$first]
resources:
  scout:
    type: agent
    name: debate-gate-scout
    description: Tests web access and a named handoff in an existing Switch room.
    provider: codex
    machine: "{machine}"
    directory: "{$agents_dir}/{scout.name}"
    addressing: owner-agents
    instructions: |
      Run only when directly addressed by your owner for a DA-GATE check.
      Open https://www.iana.org/help/example-domains using a web tool or a read-only HTTPS fetch.
      Check whether example.com is reserved for documentation and whether it is available for public registration.
      Use the page text to support each finding. If you cannot open it, mark both claims unverified and name the limitation.
      Post exactly one visible reply in the current Discord conversation using the Switch messaging tool.
      Start with DA-GATE-SCOUT and include the source, your two findings, and a named @debate-gate-checker handoff
      asking that agent to open the same page independently and evaluate the two claims.
      Wait after posting. Do not modify files or send messages elsewhere.
  checker:
    type: agent
    name: debate-gate-checker
    description: Tests whether a second Switch agent receives and verifies a named handoff.
    provider: codex
    machine: "{machine}"
    directory: "{$agents_dir}/{checker.name}"
    addressing: owner-agents
    instructions: |
      Run only when @debate-gate-scout directly addresses you for a DA-GATE check.
      Open https://www.iana.org/help/example-domains independently using a web tool or a read-only HTTPS fetch.
      Check these claims against the page: example.com is reserved for documentation, and example.com is available for public registration.
      Label each supported, contradicted, or unverified. If you cannot open the page, say so and mark both claims unverified.
      Post exactly one visible reply in the current Discord conversation using the Switch messaging tool.
      Start with DA-GATE-CHECKER and include the source and your two findings. Stop after posting.
      Do not modify files or send messages elsewhere.
```
