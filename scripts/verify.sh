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

log "Checking V3 core structure"
required_paths=(
    "README.md"
    "AGENTS.md"
    "PROJECT_RULES.md"
    ".agents/skills"
    "docs"
    "docs/workflows/intake.md"
    "runtime"
    "runtime/code_review.md"
    "scripts"
    "src"
    "tests"
    "workspaces"
)

missing_paths=()
for path in "${required_paths[@]}"; do
    if [[ ! -e "${path}" ]]; then
        missing_paths+=("${path}")
    fi
done

if (( ${#missing_paths[@]} > 0 )); then
    printf '[verify][error] Missing required path: %s\n' "${missing_paths[@]}" >&2
    die "Core structure checks failed."
fi

log "Core structure checks passed"

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
