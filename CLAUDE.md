See [AGENTS.md](AGENTS.md) for project overview, setup, commands, and parser refresh workflow.

- When using Claude Code, pre-commit runs as a quality gate on Stop via [.claude/hooks/run-pre-commit.sh](.claude/hooks/run-pre-commit.sh) (configured in [.claude/settings.json](.claude/settings.json)).
- Use the **dbt-parser-refresh** skill when updating parsers: `.claude/skills/dbt-parser-refresh/SKILL.md` or invoke `/dbt-parser-refresh`.
