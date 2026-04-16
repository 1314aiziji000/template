# Skill Validator Rules

## Official minimum vs V3 project standard

- Official minimum: `SKILL.md` is required; `agents/openai.yaml` is optional / recommended.
- V3 project standard: every custom skill must carry `agents/openai.yaml`.
- `SKILL.md` remains the primary contract; `openai.yaml` is only the UI / policy / dependencies enhancement layer.

## Validation layers

1. Official structural validation
   - Run the official `quick_validate.py`.
   - Validate YAML frontmatter, required fields, and naming rules only.
2. Official interface regeneration
   - Regenerate `interface` with the official `generate_openai_yaml.py`.
   - Compare only the generated `interface` keys.
   - Do not fail because `default_prompt` is missing.
3. V3 project enhancement validation
   - Require `policy.allow_implicit_invocation`.
   - Require narrow descriptions for meta / companion skills.
   - Reject legacy `.codex/skills` references and legacy routing headers.

## Policy map

- `project-bootstrap`: `false`
- `correction-recorder`: `false`
- `steering-runner`: `false`
- `user-dialogue-analyst`: `false`
- `skill-validator`: `false`
- `dev-planner`: `true`
- `dev-builder`: `true`
- `bug-fixer`: `true`
- `code-review`: `true`
- `release-builder`: `true`
- `context-handoff`: `true`
- `git-upload-logger`: `true`
