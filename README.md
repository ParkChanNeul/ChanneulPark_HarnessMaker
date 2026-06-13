<p align="center">
  <img src="harness_banner.png" alt="Harness Banner" width="600">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.2.0-brightgreen.svg" alt="Version">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Codex-Skill_Package-purple.svg" alt="Codex Skill Package">
  <img src="https://img.shields.io/badge/Patterns-6_Architectures-orange.svg" alt="6 Architecture Patterns">
  <img src="https://img.shields.io/badge/Mode-Agent_Teams-green.svg" alt="Agent Teams">
  <a href="https://github.com/revfactory/harness/stargazers"><img src="https://img.shields.io/github/stars/revfactory/harness?style=social" alt="GitHub Stars"></a>
</p>

<p align="center">
  <a href="#category--where-harness-sits"><img src="https://img.shields.io/badge/Layer-L3%20Meta--Factory-orange" alt="Layer"></a>
  <a href="#category--where-harness-sits"><img src="https://img.shields.io/badge/Sub--layer-Team--Architecture%20Factory-teal" alt="Sub-layer"></a>
  <a href="#"><img src="https://img.shields.io/badge/README-EN%20%7C%20KO%20%7C%20JA-lightgrey" alt="i18n"></a>
</p>

# Harness — The Team-Architecture Factory for Codex

**English** | [한국어](README_KO.md) | [日本語](README_JA.md)

> **Harness is a team-architecture factory for Codex.** Say **"build a harness for this project"** (English) or **"하네스 구성해줘"** (한국어) or **"ハーネスを構成して"** (日本語), and the skill turns your domain description into custom agents and the skills they use — picked from six pre-defined team-architecture patterns.

## Overview

Harness uses Codex parent-mediated coordination to decompose complex tasks into teams of specialized custom agents. Say "build a harness for this project" and it generates agent definitions (`.codex/agents/*.toml`), skills (`.agents/skills/`), an orchestrator skill, an `AGENTS.md` pointer, and `_workspace/` handoff artifacts tailored to your domain.

## Category — Where Harness Sits

Harness lives at the **L3 Meta-Factory** layer of the Codex ecosystem — the layer that generates other harnesses rather than being one. Inside L3, we pick a specific sub-layer: **Team-Architecture Factory**.

| Layer | What it does | Neighbors we coexist with |
|-------|--------------|---------------------------|
| **L3 — Meta-Factory / Team-Architecture Factory** (us) | Domain sentence → agent team + skills, via 6 pre-defined team patterns | — |
| L3 — Meta-Factory / Runtime-Configuration Factory | Deterministic, repeatable runtime configurations | [coleam00/Archon](https://github.com/coleam00/Archon) |
| L3 — Meta-Factory / Runtime Port | Same concept, alternate runtime | [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) |
| L2 — Cross-Harness Workflow | Standardize skills/rules/hooks across multiple harnesses | [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) |

> Archon generates deterministic runtime configurations. Harness generates team architectures (pipeline, fan-out/fan-in, expert pool, producer-reviewer, supervisor, hierarchical delegation) plus the skills agents use. Different sub-layers of the same L3. Pick Archon for runtime determinism, Harness for team architecture, or combine them.

## Star History

<a href="https://www.star-history.com/?repos=revfactory%2Fharness&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=revfactory/harness&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=revfactory/harness&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=revfactory/harness&type=date&legend=top-left" />
 </picture>
</a>


## Key Features

- **Agent Team Design** — 6 architectural patterns: Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, and Hierarchical Delegation
- **Skill Generation** — Auto-generates skills with Progressive Disclosure for efficient context management
- **Orchestration** — Parent-mediated data passing, error handling, retry, timeout, partial failure, and team coordination protocols
- **Validation** — Trigger verification, dry-run testing, and with-skill vs without-skill comparison tests


## Workflow

```
Phase 1: Domain Analysis
    ↓
Phase 2: Team Architecture Design (Parent-Orchestrated Team vs Single Subagent)
    ↓
Phase 3: Agent Definition Generation (.codex/agents/*.toml)
    ↓
Phase 4: Skill Generation (.agents/skills/)
    ↓
Phase 5: Integration & Orchestration
    ↓
Phase 6: Validation & Testing
```

## Installation

Install into a target repository:

```shell
python3 scripts/install_harness.py \
  --scope project \
  --target /path/to/target-repo \
  --with-agent-templates
```

Validate this package:

```shell
python3 scripts/validate_codex_port.py
python3 -m unittest discover -v
```

## Plugin Structure

```
harness/
├── .agents/
│   └── skills/
│       └── harness/
│           ├── SKILL.md                # Main skill definition (6-Phase workflow)
│           └── references/
│               ├── agent-design-patterns.md
│               ├── orchestrator-template.md
│               ├── team-examples.md
│               ├── skill-writing-guide.md
│               ├── skill-testing-guide.md
│               └── qa-agent-guide.md
├── .codex/
│   └── agents/*.toml               # Codex custom agent templates
├── scripts/
│   ├── install_harness.py
│   └── validate_codex_port.py
└── AGENTS.md
```

## Usage

Trigger in Codex with prompts like:

```
Build a harness for this project
Design an agent team for this domain
Set up a harness
```

### Execution Modes

| Mode | Description | Recommended For |
|------|-------------|-----------------|
| **Parent-orchestrated team** (default) | Parent dispatch + follow-up + task plan | 2+ agents requiring collaboration |
| **Single subagent / parent direct** | One custom agent or parent execution | One-off tasks, no cross-agent exchange needed |

<p align="center">
  <img src="harness_team.png" alt="Harness Agent Team" width="500">
</p>

### Architecture Patterns

| Pattern | Description |
|---------|-------------|
| Pipeline | Sequential dependent tasks |
| Fan-out/Fan-in | Parallel independent tasks |
| Expert Pool | Context-dependent selective invocation |
| Producer-Reviewer | Generation followed by quality review |
| Supervisor | Central agent with dynamic task distribution |
| Hierarchical Delegation | Top-down recursive delegation |

## Output

Files generated by Harness:

```
your-project/
├── .codex/
│   └── agents/          # Agent definition files
│       ├── analyst.toml
│       ├── builder.toml
│       └── qa.toml
├── .agents/
│   └── skills/          # Skill files
│       ├── analyze/
│       │   └── SKILL.md
│       └── build/
│           ├── SKILL.md
│           └── references/
├── AGENTS.md            # Harness pointer and change history
└── _workspace/          # Handoff and validation artifacts
```

## Use Cases — Try These Prompts

Copy any prompt below into Codex after installing Harness:

**Deep Research**
```
Build a harness for deep research. I need an agent team that can investigate
any topic from multiple angles — web search, academic sources, community
sentiment — then cross-validate findings and produce a comprehensive report.
```

**Website Development**
```
Build a harness for full-stack website development. The team should handle
design, frontend (React/Next.js), backend (API), and QA testing in a
coordinated pipeline from wireframe to deployment.
```

**Webtoon / Comic Production**
```
Build a harness for webtoon episode production. I need agents for story
writing, character design prompts, panel layout planning, and dialogue
editing. They should review each other's work for style consistency.
```

**YouTube Content Planning**
```
Build a harness for YouTube content creation. The team should research
trending topics, write scripts, optimize titles/tags for SEO, and plan
thumbnail concepts — all coordinated by a supervisor agent.
```

**Code Review & Refactoring**
```
Build a harness for comprehensive code review. I want parallel agents
checking architecture, security vulnerabilities, performance bottlenecks,
and code style — then merging all findings into a single report.
```

**Technical Documentation**
```
Build a harness that generates API documentation from this codebase.
Agents should analyze endpoints, write descriptions, generate usage
examples, and review for completeness.
```

**Data Pipeline Design**
```
Build a harness for designing data pipelines. I need agents for schema
design, ETL logic, data validation rules, and monitoring setup that
delegate sub-tasks hierarchically.
```

**Marketing Campaign**
```
Build a harness for marketing campaign creation. The team should research
the target market, write ad copy, design visual concepts, and set up
A/B test plans with iterative quality review.
```

## Coexistence — Harness and Neighbors

Harness is not alone in the Codex / agent-framework ecosystem. The following repos live in adjacent layers; each is described in a parallel "X is …, Harness is …" form so you can pick the one that fits your need or combine several.

| Repo | Their position | Relationship to Harness |
|------|----------------|-------------------------|
| [coleam00/Archon](https://github.com/coleam00/Archon) | "harness builder" — deterministic, repeatable runtime configurations | **Same L3, neighbor sub-layer.** Archon is a Runtime-Configuration Factory, Harness is a Team-Architecture Factory. Pick Archon for runtime determinism, Harness for team architecture, or combine them. |
| [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) | Adjacent implementation of the same concept | **Same L3, adjacent runtime choices.** |
| [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) | "Agent harness performance & workflow layer" (sits on top of existing harnesses) | **Different layer.** ECC is a standardization layer across harnesses; Harness is a factory that generates harnesses. Serial combination possible. |
| [wshobson/agents](https://github.com/wshobson/agents) | Subagent / skill catalog (182 agents, 149 skills) | **Factory ↔ parts supply.** wshobson is a catalog to shop from; Harness designs the team. Absorb wshobson entries as parts inside a Harness-generated team. |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | State-graph orchestration, LLM-agnostic | **Different track.** LangGraph is for long-running, state-recoverable orchestration; Harness is for fast Codex-native team design. |

## Built with Harness

### Harness 100

**[revfactory/harness-100](https://github.com/revfactory/harness-100)** — 100 production-ready agent team harnesses across 10 domains, available in both English and Korean (200 packages total). Each harness ships with 4-5 specialist agents, an orchestrator skill, and domain-specific skills — all generated by this plugin. 1,808 markdown files covering content creation, software development, data/AI, business strategy, education, legal, health, and more.

### Research: A/B Testing Harness Effectiveness

**[revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)** — A controlled experiment across 15 software engineering tasks measuring the impact of structured pre-configuration on LLM code agent output quality.

| Metric | Without Harness | With Harness | Improvement |
|--------|:-:|:-:|:-:|
| Average Quality Score | 49.5 | 79.3 | **+60%** |
| Win Rate | — | — | **100%** (15/15) |
| Output Variance | — | — | **-32%** |

Key finding: effectiveness scales with task complexity — the harder the task, the greater the improvement (+23.8 Basic, +29.6 Advanced, +36.2 Expert).

**Exact phrasing to use everywhere:** +60% avg quality (49.5 → 79.3), 15/15 win-rate, −32% variance (n=15, author-measured A/B, third-party replications pending).

> Full paper: *Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality.*

## Requirements

- Python 3.11+ for installer and validation scripts
- Codex CLI or Codex app access to run generated harnesses

## FAQ

<details>
<summary><b>Q1. Isn't "+60%" oversold?</b></summary>

**A.** The +60% figure comes from an **author-measured A/B (n=15, 15 tasks, measured on the sister repo `claude-code-harness`)**. Every citation in this repo pairs the number with the disclosure "n=15, author-measured, third-party replications pending" in the same sentence. For adoption decisions, we recommend running a 2–4 week internal pilot and measuring your own numbers.

**Evidence:**
- Author A/B: [revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)
- Paper: *Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality*
</details>

<details>
<summary><b>Q2. Why "harness factory" and not "harness builder"? Isn't this competing with Archon?</b></summary>

**A.** Archon generates deterministic runtime configurations — it's a **Runtime-Configuration Factory**. Harness generates agent team architectures (team structure, message protocols, review gates) — it's a **Team-Architecture Factory**. They are **neighbor sub-layers of the same L3 Meta-Factory** and serve different needs. Pick Archon for runtime determinism, Harness for team-architecture patterns, or combine them (design architecture with Harness → deploy runtime with Archon).

**Evidence:**
- Archon self-definition: [clawfit docs/reference-levels.md](https://github.com/hongsw/clawfit/blob/main/docs/reference-levels.md)
- Sub-layer declaration: see the **Category — Where Harness Sits** section above
- Archon repo: [github.com/coleam00/Archon](https://github.com/coleam00/Archon)
</details>

<details>
<summary><b>Q3. Is this tied to one runtime?</b></summary>

**A.** This branch is the Codex-native port. It keeps the upstream Harness workflow while replacing runtime paths and coordination primitives with `.codex/agents/*.toml`, `.agents/skills/`, parent-mediated follow-up, and parent-owned final writes.

**Evidence:**
- Codex port: [github.com/SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness)
- Cross-runtime scaffolder: [github.com/Gizele1/harness-init](https://github.com/Gizele1/harness-init)
</details>

## License

Apache 2.0
