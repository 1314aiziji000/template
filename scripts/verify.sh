#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

log() {
    printf '[verify] %s\n' "$*"
}

warn() {
    printf '[verify][warn] %s\n' "$*" >&2
}

die() {
    printf '[verify][error] %s\n' "$*" >&2
    exit 1
}

has_command() {
    command -v "$1" >/dev/null 2>&1
}

PYTHON_CMD=()

detect_python_command() {
    if has_command python; then
        PYTHON_CMD=(python)
        return 0
    fi
    if has_command python3; then
        PYTHON_CMD=(python3)
        return 0
    fi
    if has_command py; then
        PYTHON_CMD=(py -3)
        return 0
    fi
    return 1
}

detect_package_manager() {
    if [[ -f "pnpm-lock.yaml" ]] && has_command pnpm; then
        printf 'pnpm'
        return 0
    fi
    if [[ -f "yarn.lock" ]] && has_command yarn; then
        printf 'yarn'
        return 0
    fi
    if [[ ( -f "bun.lock" || -f "bun.lockb" ) ]] && has_command bun; then
        printf 'bun'
        return 0
    fi
    if [[ -f "package.json" ]] && has_command npm; then
        printf 'npm'
        return 0
    fi
    return 1
}

package_script_exists() {
    local script_name="$1"
    [[ -f "package.json" ]] || return 1
    grep -Eq "\"${script_name}\"[[:space:]]*:" "package.json"
}

run_package_script() {
    local package_manager="$1"
    local script_name="$2"

    log "Running ${package_manager} script: ${script_name}"
    case "${package_manager}" in
        pnpm) pnpm run "${script_name}" ;;
        yarn) yarn "${script_name}" ;;
        bun) bun run "${script_name}" ;;
        npm) npm run "${script_name}" ;;
        *) die "Unsupported package manager: ${package_manager}" ;;
    esac
}

bootstrap_brief="项目说明书.md"
bootstrap_skill_file=".agents/skills/project-bootstrap/SKILL.md"
bootstrap_template_file=".agents/skills/project-bootstrap/templates/bootstrap-checklist.md"
bootstrap_workflow="docs/workflows/bootstrap.md"
skill_validator_dir=".agents/skills/skill-validator"
skill_validator_script="${skill_validator_dir}/scripts/run_skill_validator.py"
contract_validator_script="scripts/verify_contracts.py"
validation_pack_runner_script="scripts/run_validation_pack.py"
validation_pack_manifest="workspaces/v3-validation-pack/acceptance.manifest.yaml"
validation_pack_report="workspaces/v3-validation-pack/reports/08-validation-pack-automation.md"

log "Checking V3 core structure"
required_paths=(
    "README.md"
    "AGENTS.md"
    "PROJECT_RULES.md"
    ".gitignore"
    ".agents/skills"
    ".agents/skills/context-handoff/SKILL.md"
    ".agents/skills/context-handoff/templates/handoff-template.md"
    ".agents/skills/correction-recorder/SKILL.md"
    ".agents/skills/correction-recorder/templates/error-record-template.md"
    ".agents/skills/dev-planner/SKILL.md"
    ".agents/skills/dev-planner/templates/plans-template.md"
    ".agents/skills/dev-builder/SKILL.md"
    ".agents/skills/bug-fixer/SKILL.md"
    ".agents/skills/code-review/SKILL.md"
    ".agents/skills/code-review/templates/review-template.md"
    ".agents/skills/git-upload-logger/SKILL.md"
    ".agents/skills/git-upload-logger/templates/upload-log-template.md"
    ".agents/skills/release-builder/SKILL.md"
    ".agents/skills/release-builder/templates/release-card-template.md"
    ".agents/skills/release-builder/scripts/release-check.sh"
    ".agents/skills/skill-validator/SKILL.md"
    ".agents/skills/skill-validator/agents/openai.yaml"
    ".agents/skills/skill-validator/references/validation-rules.md"
    ".agents/skills/skill-validator/scripts/run_skill_validator.py"
    ".agents/skills/steering-runner/SKILL.md"
    ".agents/skills/steering-runner/templates/evolution-proposal-template.md"
    ".agents/skills/steering-runner/templates/evolution-memory-template.md"
    ".agents/skills/steering-runner/references/strategy-map.md"
    ".agents/skills/steering-runner/scripts/run-steering-scan.py"
    ".codex/config.toml"
    "docs"
    "docs/README.md"
    "docs/workflows/README.md"
    "${bootstrap_workflow}"
    "docs/workflows/intake.md"
    "docs/workflows/build-verify-review.md"
    "docs/workflows/release-retro.md"
    "docs/protocols/README.md"
    "docs/protocols/security-lite.md"
    "docs/protocols/ai-eval-gate.md"
    "docs/protocols/adr-lite.md"
    "docs/protocols/release-gate.md"
    "docs/protocols/steering-lite.md"
    "schemas"
    "schemas/README.md"
    "schemas/steering/README.md"
    "schemas/steering/error-record.schema.json"
    "schemas/steering/evolution-proposal.schema.json"
    "schemas/steering/evolution-memory.schema.json"
    "runtime"
    "runtime/README.md"
    "runtime/PLANS.md"
    "runtime/code_review.md"
    "runtime/evolution"
    "runtime/evolution/README.md"
    "runtime/evolution/proposals/README.md"
    "runtime/evolution/archive/README.md"
    "runtime/evolution/memory/README.md"
    "runtime/evolution/memory/lessons/README.md"
    "runtime/evolution/memory/strategies/README.md"
    "runtime/logs"
    "runtime/logs/README.md"
    "resources"
    "resources/README.md"
    "scripts"
    "scripts/verify_contracts.py"
    "scripts/run_validation_pack.py"
    "scripts/scan-steering-signals.py"
    "scripts/verify.sh"
    "scripts/security-check.sh"
    "scripts/run-evals.sh"
    "src"
    "src/README.md"
    "tests"
    "tests/README.md"
    "workspaces"
    "workspaces/README.md"
)

missing_paths=()
for path in "${required_paths[@]}"; do
    if [[ ! -e "${path}" ]]; then
        missing_paths+=("${path}")
    fi
done

for skill_dir in .agents/skills/*; do
    [[ -d "${skill_dir}" ]] || continue
    if [[ ! -e "${skill_dir}/agents/openai.yaml" ]]; then
        missing_paths+=("${skill_dir}/agents/openai.yaml")
    fi
done

if (( ${#missing_paths[@]} > 0 )); then
    printf '[verify][error] Missing required path: %s\n' "${missing_paths[@]}" >&2
    die "Core structure checks failed."
fi

log "Core structure checks passed"

bootstrap_assets_seen=0
if [[ -e "${bootstrap_brief}" || -e "${bootstrap_skill_file}" || -e "${bootstrap_template_file}" ]]; then
    bootstrap_assets_seen=1
    if [[ -e "${bootstrap_brief}" && -e "${bootstrap_skill_file}" && -e "${bootstrap_template_file}" ]]; then
        log "Detected bootstrap-ready template mode"
    else
        die "Bootstrap assets are partially present. Keep 项目说明书.md and project-bootstrap skill in sync."
    fi
else
    log "Detected initialized project mode"
fi

# Optional packs / auxiliary paths: validate only if present.
optional_paths=(
    "docs/integrations/README.md"
    "docs/ui/README.md"
    "prompts/README.md"
    "evals/README.md"
    "me/README.md"
    "me/self-memory/README.md"
    ".agents/skills/user-dialogue-analyst/SKILL.md"
    "workspaces/self-memory-staging/README.md"
)
for path in "${optional_paths[@]}"; do
    if [[ -e "${path}" ]]; then
        log "Optional path present: ${path}"
    fi
done

self_memory_enabled=0
if [[ -e "me/self-memory/README.md" || -e ".agents/skills/user-dialogue-analyst/SKILL.md" || -e "workspaces/self-memory-staging/README.md" ]]; then
    self_memory_enabled=1
    self_memory_required_paths=(
        "me/self-memory/README.md"
        "me/self-memory/extracts/README.md"
        "me/self-memory/batches/README.md"
        "me/self-memory/reports/README.md"
        "me/self-memory/reports/micro/README.md"
        "me/self-memory/reports/periodic/README.md"
        "me/self-memory/profile/README.md"
        "me/self-memory/archive/README.md"
        ".agents/skills/user-dialogue-analyst/SKILL.md"
        ".agents/skills/user-dialogue-analyst/templates/extract-template.md"
        ".agents/skills/user-dialogue-analyst/templates/batch-template.md"
        ".agents/skills/user-dialogue-analyst/templates/report-template.md"
        ".agents/skills/user-dialogue-analyst/references/analysis-rubric.md"
        ".agents/skills/user-dialogue-analyst/scripts/extract_dialogue.py"
        ".agents/skills/user-dialogue-analyst/scripts/roll_batch.py"
        ".agents/skills/user-dialogue-analyst/scripts/build_report.py"
        ".agents/skills/user-dialogue-analyst/scripts/purge_raw.py"
        "workspaces/self-memory-staging/README.md"
        "workspaces/self-memory-staging/.gitignore"
    )
    for path in "${self_memory_required_paths[@]}"; do
        [[ -e "${path}" ]] || die "Self-memory pack is partially present. Missing: ${path}"
    done
fi

if ! detect_python_command; then
    die "Python is required to run official skill validation."
fi

log "Running official and project skill-pack validation"
"${PYTHON_CMD[@]}" "${skill_validator_script}" --workspace-root "${ROOT_DIR}"

log "Running owner-document contract validation"
"${PYTHON_CMD[@]}" "${contract_validator_script}" --workspace-root "${ROOT_DIR}"

if [[ -f "${validation_pack_manifest}" && "${V3_SKIP_VALIDATION_PACK:-0}" != "1" ]]; then
    log "Running validation-pack automation"
    "${PYTHON_CMD[@]}" "${validation_pack_runner_script}" \
        --workspace-root "${ROOT_DIR}" \
        --manifest "${validation_pack_manifest}" \
        --report "${validation_pack_report}"
elif [[ -f "${validation_pack_manifest}" ]]; then
    log "Skipping validation-pack automation because V3_SKIP_VALIDATION_PACK=1"
else
    log "Validation-pack automation manifest not present. Skipping."
fi

ran_any=0

if [[ -n "${V3_VERIFY_COMMANDS:-}" ]]; then
    log "Running custom commands from V3_VERIFY_COMMANDS"
    bash -lc "${V3_VERIFY_COMMANDS}"
    ran_any=1
fi

if [[ -f "package.json" ]]; then
    package_manager="$(detect_package_manager || true)"
    if [[ -n "${package_manager}" ]]; then
        for script_name in lint typecheck test build; do
            if package_script_exists "${script_name}"; then
                run_package_script "${package_manager}" "${script_name}"
                ran_any=1
            fi
        done
    else
        warn "package.json detected, but no supported package manager is available."
    fi
fi

if [[ -f "pyproject.toml" || -f "requirements.txt" || -f "requirements-dev.txt" ]]; then
    if has_command pytest && find "tests" -type f \( -name 'test_*.py' -o -name '*_test.py' \) -print -quit | grep -q .; then
        log "Running pytest"
        pytest
        ran_any=1
    else
        warn "Python project hints detected, but no runnable pytest suite was found."
    fi
fi

if [[ -f "Cargo.toml" ]]; then
    if has_command cargo; then
        log "Running cargo test"
        cargo test
        ran_any=1
    else
        warn "Cargo project detected, but cargo is not available."
    fi
fi

if [[ -f "go.mod" ]]; then
    if has_command go; then
        log "Running go test ./..."
        go test ./...
        ran_any=1
    else
        warn "Go project detected, but go is not available."
    fi
fi

if (( ran_any == 0 )); then
    log "No stack-specific verification command detected. Structure-only verification passed."
else
    log "Verification commands completed successfully."
fi
