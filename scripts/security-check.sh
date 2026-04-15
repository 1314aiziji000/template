#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

log() {
    printf '[security-check] %s\n' "$*"
}

warn() {
    printf '[security-check][warn] %s\n' "$*" >&2
}

die() {
    printf '[security-check][error] %s\n' "$*" >&2
    exit 1
}

has_command() {
    command -v "$1" >/dev/null 2>&1
}

target_dir="${1:-${ROOT_DIR}}"
[[ -d "${target_dir}" ]] || die "Target directory does not exist: ${target_dir}"

log "Running automated Security Lite checks in ${target_dir}"

disallowed_files=()
while IFS= read -r -d '' file; do
    case "$(basename "${file}")" in
        .env.example|.env.sample|.env.template)
            continue
            ;;
    esac
    disallowed_files+=("${file}")
done < <(
    find "${target_dir}" \
        \( -path '*/.git/*' -o -path '*/node_modules/*' -o -path '*/.venv/*' -o -path '*/.tox/*' -o -path '*/dist/*' -o -path '*/build/*' -o -path '*/out/*' -o -path '*/coverage/*' \) -prune \
        -o -type f \
        \( -name '.env' -o -name '.env.*' -o -name '*.pem' -o -name '*.key' -o -name '*.p12' -o -name '*.pfx' -o -name 'id_rsa' -o -name 'id_ed25519' \) \
        -print0
)

secret_hits=()
if has_command rg; then
    mapfile -t secret_hits < <(
        rg -n -I --hidden \
            --glob '!.git/**' \
            --glob '!node_modules/**' \
            --glob '!.venv/**' \
            --glob '!dist/**' \
            --glob '!build/**' \
            --glob '!out/**' \
            --glob '!coverage/**' \
            -e '(OPENAI_API_KEY|ANTHROPIC_API_KEY|GEMINI_API_KEY|AWS_SECRET_ACCESS_KEY)[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9_/\-]{8,}' \
            -e 'sk-[A-Za-z0-9_-]{20,}' \
            -e '-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----' \
            "${target_dir}" 2>/dev/null || true
    )
else
    warn "ripgrep not found; skipped content-based secret scanning."
fi

if [[ -f ".gitignore" ]]; then
    for required_pattern in '.env' '*.pem' '*.key'; do
        if ! grep -Fq "${required_pattern}" ".gitignore"; then
            warn ".gitignore is missing recommended sensitive pattern: ${required_pattern}"
        fi
    done
else
    log ".gitignore not found in the template root; add one in the real project if sensitive files or build outputs need ignoring."
fi

if (( ${#disallowed_files[@]} > 0 )); then
    printf '[security-check][error] Disallowed file found: %s\n' "${disallowed_files[@]}" >&2
fi

if (( ${#secret_hits[@]} > 0 )); then
    printf '[security-check][error] Secret-like content found: %s\n' "${secret_hits[@]}" >&2
fi

if (( ${#disallowed_files[@]} > 0 || ${#secret_hits[@]} > 0 )); then
    die "Automated Security Lite checks failed."
fi

log "Automated security checks passed."
log "Pair this script with docs/protocols/security-checklist.md for manual checks such as input validation, auth boundaries, and log redaction."
