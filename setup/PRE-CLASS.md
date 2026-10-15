# Pre-class setup

Target time: 10 minutes or less (timed in M9 on a clean machine). Status: draft; the full step list and
measured timings are added in M7 and verified in M9.

## Accounts you need

| Account | Plan | Why |
|---|---|---|
| OpenAI API | Paid, **Build tier or higher, with at least $5 of credit purchased** | The agent model (gpt-6-luna) lists API rate limits only for paid tiers. Your assignment spend is capped at $6 in total. |
| LangSmith | **Free Developer plan, no card on file** | Traces and experiments. Without a card the plan has a hard cap of 5,000 traces per month, so you cannot be charged. The module uses at most 400 traces. |

Do not add a credit card to LangSmith.

## Steps

1. Install git, uv, and a container runtime:
   - Windows: WSL2 with Ubuntu, then Docker Desktop with the WSL2 backend. Clone the repository inside
     the WSL2 filesystem (for example `~/shipharness`), not under `/mnt/c`.
   - macOS: Docker Desktop or Colima.
   - Linux: Docker Engine or Podman.
2. Clone: `git clone https://github.com/ANI-IN/shipharness.git && cd shipharness`
3. `make setup`
4. Create your keys file: `cp .env.example .env`, then open `.env` and fill in `OPENAI_API_KEY` and
   `LANGSMITH_API_KEY`. The file is git-ignored; never commit or share it.
5. `make doctor` must pass. It names any key that is missing or invalid.
6. `make up` and open the TeamTrack board in your browser.
