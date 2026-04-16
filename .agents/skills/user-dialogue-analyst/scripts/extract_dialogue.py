#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

NOISE_PREFIXES = (
    "## Active file:",
    "## Open tabs:",
    "# Context from my IDE setup:",
    "Context from my IDE setup:",
    "```",
)


def normalize_lines(text: str):
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(stripped.startswith(prefix) for prefix in NOISE_PREFIXES):
            continue
        lines.append(stripped)
    return lines


def pick(lines, keywords, limit=5):
    found = []
    for line in lines:
        lowered = line.lower()
        if any(keyword in line or keyword in lowered for keyword in keywords):
            if line not in found:
                found.append(line)
        if len(found) >= limit:
            break
    return found


def build_extract(lines, raw_path: Path):
    effective_chars = sum(len(line) for line in lines)
    effective_turns = len(lines)
    topics = lines[:5]
    constraints = pick(lines, ["必须", "不要", "只", "不能", "边界", "固定", "default"])
    corrections = pick(lines, ["不对", "搞错", "不是", "先判断", "不要", "别"])
    decision_changes = pick(lines, ["现在", "改成", "最终", "定位", "定稿", "先", "后"])
    repeated = []
    seen = {}
    for line in lines:
        seen[line] = seen.get(line, 0) + 1
    for line, count in seen.items():
        if count > 1:
            repeated.append(f"{line} x{count}")
    friction = pick(lines, ["风险", "误", "漏", "返工", "卡", "不稳", "冲突"])
    good = pick(lines, ["完整", "流程", "框架", "细节", "先判断", "边界", "报告"])
    next_points = constraints[:2] + corrections[:2]
    summary = f"本次 extract 覆盖 {effective_turns} 条有效内容，共 {effective_chars} 字。"
    return {
        "window_id": raw_path.stem,
        "source_date": raw_path.stem[:10] if len(raw_path.stem) >= 10 else "",
        "effective_chars": effective_chars,
        "effective_turns": effective_turns,
        "source_raw": raw_path.as_posix(),
        "main_topics": topics,
        "hard_constraints": constraints,
        "user_corrections": corrections,
        "decision_changes": decision_changes,
        "repeated_requests": repeated[:5],
        "friction_points": friction,
        "good_patterns": good,
        "next_attention_points": next_points[:5],
        "summary": summary,
    }


def render_extract(data):
    sections = [
        ("main_topics", data["main_topics"]),
        ("hard_constraints", data["hard_constraints"]),
        ("user_corrections", data["user_corrections"]),
        ("decision_changes", data["decision_changes"]),
        ("repeated_requests", data["repeated_requests"]),
        ("friction_points", data["friction_points"]),
        ("good_patterns", data["good_patterns"]),
        ("next_attention_points", data["next_attention_points"]),
        ("summary", [data["summary"]]),
    ]
    lines = [
        "---",
        f"window_id: {data['window_id']}",
        f"source_date: {data['source_date']}",
        f"effective_chars: {data['effective_chars']}",
        f"effective_turns: {data['effective_turns']}",
        f"source_raw: {data['source_raw']}",
        "---",
        "",
        f"# extract {data['window_id']}",
        "",
    ]
    for title, items in sections:
        lines.append(f"## {title}")
        if items:
            for item in items:
                lines.append(f"- {item}")
        else:
            lines.append("- ")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    raw_path = Path(args.input)
    lines = normalize_lines(raw_path.read_text(encoding="utf-8", errors="ignore"))
    data = build_extract(lines, raw_path)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_extract(data), encoding="utf-8")

    manifest = {
        "raw_id": raw_path.stem,
        "source_date": data["source_date"],
        "raw_exists": raw_path.exists(),
        "raw_hash": hashlib.sha1(raw_path.read_bytes()).hexdigest(),
        "raw_turn_count": len(lines),
        "raw_effective_chars": data["effective_chars"],
        "extract_status": "extracted",
        "extract_file": output_path.as_posix(),
        "extract_hash": hashlib.sha1(output_path.read_bytes()).hexdigest(),
        "included_in_batch": [],
        "included_in_report": [],
        "purged_at": None,
    }
    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"extract": output_path.as_posix(), "manifest": manifest_path.as_posix()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
