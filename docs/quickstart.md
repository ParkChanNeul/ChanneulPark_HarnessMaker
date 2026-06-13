# Quickstart - 5 Minutes to Your First Codex Harness

> **Time budget: 5 minutes.** If these steps do not produce the expected files, open an issue with the exact command output.

**What you will have at the end:** a target repository with `.codex/agents/`, `.agents/skills/`, an orchestrator skill, an `AGENTS.md` pointer, and `_workspace/` handoff artifacts.

## Prerequisites

- Codex CLI or Codex app access for running the generated harness.
- Python 3.11+ for the installer and validation scripts.
- A target repository where you want Harness installed.

## Step 1 - Validate This Package

```bash
python3 scripts/validate_codex_port.py
python3 -m unittest discover -v
```

Expected result: validation passes and the unit test suite is green.

## Step 2 - Install Harness Into a Target Repo

```bash
python3 scripts/install_harness.py \
  --scope project \
  --target /path/to/target-repo \
  --with-agent-templates
```

What this writes:

```text
/path/to/target-repo/
├── .agents/skills/harness/SKILL.md
├── .agents/skills/harness/references/
├── .codex/agents/*.toml
└── .codex/config.toml.example
```

The installer writes `.agents/skills/harness/.harnessmaker-install.json` so future installs can distinguish managed files from user-owned files.

## Step 3 - Trigger Harness In Codex

From the target repository, ask Codex:

```text
Build a harness for a fintech risk-assessment team.
```

Equivalent prompts:

```text
하네스 구성해줘 - 핀테크 리스크 평가 팀
Design an agent team for technical due diligence on open-source repos.
Set up a harness for an e-commerce fraud-detection workflow.
```

Expected behavior: the Harness skill audits the repo, chooses an architecture pattern, defines domain agents, creates supporting skills, creates an orchestrator skill, updates `AGENTS.md`, and preserves handoff artifacts under `_workspace/`.

## Step 4 - Verify Generated Files

```bash
test -f .codex/agents/discovery_analyst.toml
test -f .agents/skills/harness/SKILL.md
test ! -d .codex/skills
find .codex/agents -name '*.toml' -maxdepth 1
find .agents/skills -name 'SKILL.md'
```

For a generated domain harness, check for:

```text
.codex/agents/{domain_agent}.toml
.agents/skills/{domain_skill}/SKILL.md
.agents/skills/{domain_orchestrator}/SKILL.md
AGENTS.md
_workspace/
```

## Step 5 - Run A Sample Task

After generation, ask Codex to run a realistic task through the new orchestrator:

```text
Ticket FIN-427: A new corporate customer (mid-cap manufacturer, $80M revenue, South Korea) has applied for a $5M working-capital line. Produce a risk assessment covering credit-history red flags, sector concentration, and regulatory exposure. Output a 1-page memo with a go/no-go recommendation.
```

Expected result: the orchestrator uses parent-mediated coordination, runs only independent subagent work in bounded parallel, collects evidence, handles conflicts, and writes the final artifact through the parent.

## Troubleshooting

**No skill was triggered:** confirm `.agents/skills/harness/SKILL.md` exists and the prompt mentions building, configuring, auditing, or maintaining a harness.

**Existing files block install:** the installer refuses to overwrite unmanaged files. Move the conflicting file or install into a clean target.

**Managed file was edited:** rerun with `--force` only if you intentionally want to replace files recorded in `.harnessmaker-install.json`; unrelated user files are preserved.

**A generated harness is too complex:** ask Harness to rerun with a smaller architecture or single-agent baseline. The skill should choose simple parent execution for simple requests.
