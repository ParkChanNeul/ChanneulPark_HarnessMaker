# Implementation Notes

Runtime-critical rules live inside `.agents/skills/harness/references/`. This directory is for maintainers of ChanneulPark HarnessMaker.

- Do not add `.codex/skills` mirrors.
- Do not commit `.harnessmaker-install.json` in the source tree.
- Keep the installer dependency-free and Python 3.11+ compatible.
- If optional config examples change, do not overwrite existing active Codex config files.
