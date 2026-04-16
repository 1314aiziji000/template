#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

THRESHOLDS = {
    "rule-graduation": 3,
    "skill-adjustment": 3,
    "protocol-hardening": 3,
    "verify-hardening": 3,
    "new-skill-candidate": 5,
}

SIGNAL_OWNER_MAP = {
    "global-behavior": ("AGENTS.md", "AGENTS.md", "rule-graduation"),
    "boundary-drift": ("AGENTS.md", "AGENTS.md", "rule-graduation"),
    "project-boundary": ("PROJECT_RULES.md", "PROJECT_RULES.md", "rule-graduation"),
    "protocol-gap": ("docs/protocols/steering-lite.md", "docs/protocols/steering-lite.md", "protocol-hardening"),
    "verify-gap": ("scripts/verify.sh", "scripts/verify.sh", "verify-hardening"),
    "routing-gap": (".agents/skills/dev-planner/SKILL.md", ".agents/skills/dev-planner/SKILL.md", "skill-adjustment"),
    "new-skill-gap": (".agents/skills/", ".agents/skills/", "new-skill-candidate"),
}

SIGNAL_PATTERNS = {
    "boundary-drift": re.compile(r"边界|越权|scope|boundary", re.I),
    "protocol-gap": re.compile(r"protocol|字段|证据|gate", re.I),
    "verify-gap": re.compile(r"verify|验证|脚本缺口|未验证", re.I),
    "routing-gap": re.compile(r"路由|description|skill trigger", re.I),
    "new-skill-gap": re.compile(r"新 skill|new skill|无 owner", re.I),
    "global-behavior": re.compile(r"全局|global|常驻规则", re.I),
}


def parse_scalar(raw: str):
    value = raw.strip()
    if value == "":
        return ""
    if value.isdigit():
        return int(value)
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return value.strip('"').strip("'")


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    raw_meta = parts[0].splitlines()[1:]
    body = parts[1]
    meta: dict[str, object] = {}
    current_list_key: str | None = None
    for line in raw_meta:
        if line.startswith("  - ") and current_list_key:
            meta.setdefault(current_list_key, [])
            meta[current_list_key].append(parse_scalar(line[4:]))
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        parsed = parse_scalar(value)
        if parsed == "":
            meta[key] = []
            current_list_key = key
        else:
            meta[key] = parsed
    return meta, body


def detect_signal(meta: dict[str, object], body: str) -> str:
    explicit = meta.get("signal_type")
    if isinstance(explicit, str) and explicit:
        return explicit
    for signal, pattern in SIGNAL_PATTERNS.items():
        if pattern.search(body):
            return signal
    return "boundary-drift"


def derive_target(meta: dict[str, object], signal_type: str):
    owner = meta.get("target_owner") or meta.get("owner_target") or meta.get("target_owner_hint")
    path = meta.get("target_path") or meta.get("target_path_hint")
    proposal_type = meta.get("proposal_type")
    if owner and path and proposal_type:
        return str(owner), str(path), str(proposal_type)
    mapped_owner, mapped_path, mapped_type = SIGNAL_OWNER_MAP.get(
        signal_type, ("AGENTS.md", "AGENTS.md", "rule-graduation")
    )
    return str(owner or mapped_owner), str(path or mapped_path), str(proposal_type or mapped_type)


def read_records(paths: list[Path]):
    records = []
    for root in paths:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            if path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            meta, body = parse_frontmatter(text)
            signal_type = detect_signal(meta, body)
            target_owner, target_path, proposal_type = derive_target(meta, signal_type)
            source_skill = str(meta.get("source_skill", "N/A"))
            records.append(
                {
                    "path": str(path.as_posix()),
                    "signal_type": signal_type,
                    "target_owner": target_owner,
                    "target_path": target_path,
                    "proposal_type": proposal_type,
                    "source_skill": source_skill,
                    "summary": str(meta.get("summary", "")) or next((line.strip() for line in body.splitlines() if line.strip()), ""),
                }
            )
    return records


def build_proposals(records):
    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for record in records:
        key = (
            record["proposal_type"],
            record["signal_type"],
            record["target_owner"],
            record["target_path"],
        )
        grouped[key].append(record)

    proposals = []
    for key, items in grouped.items():
        proposal_type, signal_type, target_owner, target_path = key
        threshold = THRESHOLDS.get(proposal_type, 3)
        repeat_count = len(items)
        if repeat_count < threshold:
            continue
        source_records = [item["path"] for item in items]
        digest = hashlib.sha1("|".join(key).encode("utf-8")).hexdigest()[:10]
        proposals.append(
            {
                "id": f"{datetime.now(timezone.utc).date()}-{proposal_type}-{digest}",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "status": "proposed",
                "proposal_type": proposal_type,
                "signal_type": signal_type,
                "repeat_count": repeat_count,
                "target_owner": target_owner,
                "target_path": target_path,
                "source_records": source_records,
                "summary": items[0]["summary"] or f"{signal_type} repeated {repeat_count} times",
                "suggested_change": f"Promote the repeated {signal_type} pattern to {target_owner}.",
                "validation_plan": [
                    "update the target owner document",
                    "run verify.sh",
                    "confirm the incident does not recur in the validation sample",
                ],
            }
        )
    return proposals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--errors", default="runtime/errors")
    parser.add_argument("--logs", default="runtime/logs")
    parser.add_argument("--reviews", default="runtime/reviews")
    parser.add_argument("--format", choices=["json"], default="json")
    args = parser.parse_args()

    roots = [Path(args.errors), Path(args.logs), Path(args.reviews)]
    proposals = build_proposals(read_records(roots))
    print(json.dumps({"proposals": proposals}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
