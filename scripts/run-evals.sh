#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

log() {
    printf '[run-evals] %s\n' "$*"
}

die() {
    printf '[run-evals][error] %s\n' "$*" >&2
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

ai_pack_active=0
for path in "evals" "prompts" "configs/models"; do
    if [[ -d "${path}" ]] && find "${path}" -type f ! -name 'README.md' -print -quit | grep -q .; then
        ai_pack_active=1
        break
    fi
done

if [[ -n "${V3_EVAL_COMMAND:-}" ]]; then
    log "Running custom command from V3_EVAL_COMMAND"
    bash -lc "${V3_EVAL_COMMAND}"
    exit 0
fi

if (( ai_pack_active == 0 )); then
    log "No active AI Pack material detected under evals/, prompts/ or configs/models/. Nothing to run."
    exit 0
fi

package_manager="$(detect_package_manager || true)"
if [[ -n "${package_manager}" ]]; then
    for script_name in evals eval test:eval; do
        if package_script_exists "${script_name}"; then
            run_package_script "${package_manager}" "${script_name}"
            exit 0
        fi
    done
fi

if [[ -f "evals/run.sh" ]]; then
    log "Running evals/run.sh"
    bash "evals/run.sh"
    exit 0
fi

if [[ -f "evals/run.py" ]] && has_command python; then
    log "Running evals/run.py"
    python "evals/run.py"
    exit 0
fi

if [[ -f "evals/run.js" ]] && has_command node; then
    log "Running evals/run.js"
    node "evals/run.js"
    exit 0
fi

die "AI Pack material detected, but no eval runner is configured. Set V3_EVAL_COMMAND or add package.json script eval/evals/test:eval or evals/run.{sh,py,js}."
