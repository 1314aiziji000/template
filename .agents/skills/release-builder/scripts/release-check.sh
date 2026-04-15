#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"

log() {
    printf '[release-check] %s\n' "$*"
}

warn() {
    printf '[release-check][warn] %s\n' "$*" >&2
}

die() {
    printf '[release-check][error] %s\n' "$*" >&2
    exit 1
}

has_command() {
    command -v "$1" >/dev/null 2>&1
}

usage() {
    cat <<'EOF'
Usage: release-check.sh [--project-root PATH] [--release-card PATH] [--allow-dirty] [--strict]

Options:
  --project-root PATH   Override the project root to inspect.
  --release-card PATH   Explicitly choose the release record to validate.
  --allow-dirty         Do not fail on a dirty git worktree.
  --strict              Require a release record instead of skipping when none exists.
  -h, --help            Show this help text.
EOF
}

project_root="${ROOT_DIR}"
release_card=""
allow_dirty=0
strict_mode=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --project-root)
            [[ $# -ge 2 ]] || die "--project-root requires a path"
            project_root="$2"
            shift 2
            ;;
        --release-card)
            [[ $# -ge 2 ]] || die "--release-card requires a path"
            release_card="$2"
            shift 2
            ;;
        --allow-dirty)
            allow_dirty=1
            shift
            ;;
        --strict)
            strict_mode=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            die "Unknown argument: $1"
            ;;
    esac
done

cd "${project_root}"

if [[ -z "${release_card}" ]] && [[ -d "runtime/releases" ]]; then
    release_card="$(find "runtime/releases" -maxdepth 1 -type f -name '*.md' ! -name 'README.md' | sort | tail -n 1 || true)"
fi

if [[ -z "${release_card}" ]]; then
    if (( strict_mode == 1 )); then
        die "No release record detected. Provide --release-card or create runtime/releases/*.md."
    fi
    log "No release record detected under runtime/releases/. Release gate is not active; skipping."
    exit 0
fi

[[ -f "${release_card}" ]] || die "Release record not found: ${release_card}"

if (( allow_dirty == 0 )) && has_command git && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if [[ -n "$(git status --short)" ]]; then
        die "Git worktree is dirty. Re-run with --allow-dirty only when this is intentional."
    fi
fi

[[ -f "runtime/code_review.md" ]] || warn "runtime/code_review.md is missing."
[[ -f "runtime/README.md" ]] || warn "runtime/README.md is missing."

missing_fields=()
for field in "Target" "Smoke checks" "Rollback" "Notes"; do
    if ! grep -Eq "^([[:space:]]*[-*][[:space:]]*|[[:space:]]*#{1,6}[[:space:]]*)${field}\b" "${release_card}"; then
        missing_fields+=("${field}")
    fi
done

if grep -Eiq 'TBD|TODO|待补充|待确定|placeholder' "${release_card}"; then
    die "Release record still contains placeholder content: ${release_card}"
fi

if (( ${#missing_fields[@]} > 0 )); then
    printf '[release-check][error] Missing required field: %s\n' "${missing_fields[@]}" >&2
    die "Release record is incomplete."
fi

if [[ -f "package.json" ]] && ! grep -Eq '"version"[[:space:]]*:[[:space:]]*"[0-9]+\.[0-9]+\.[0-9]+' "package.json"; then
    warn "package.json exists, but no obvious semver version was detected."
fi

log "Validated release record: ${release_card}"
log "Release gate checks completed."
