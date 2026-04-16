#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    meta = {}
    current_key = None
    for line in parts[0].splitlines()[1:]:
        if line.startswith("  - ") and current_key:
            meta.setdefault(current_key, [])
            meta[current_key].append(line[4:].strip())
            continue
        current_key = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            meta[key] = int(value) if value.isdigit() else value
        else:
            meta[key] = []
            current_key = key
    return meta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract-dir", required=True)
    parser.add_argument("--month", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest-dir", default="")
    args = parser.parse_args()

    extract_dir = Path(args.extract_dir)
    extracts = []
    total_chars = 0
    total_turns = 0
    topics = []
    for path in sorted(extract_dir.glob(f"{args.month}*.md")):
        meta = parse_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
        total_chars += int(meta.get("effective_chars", 0))
        total_turns += int(meta.get("effective_turns", 0))
        extracts.append(path.as_posix())
        topics.append(path.stem)

    micro_due = total_chars >= 400 or total_turns >= 4
    periodic_due = total_chars >= 1200 or total_turns >= 10

    lines = [
        "---",
        f"batch_id: {args.month}-batch-001",
        f"month: {args.month}",
        "source_extracts:",
    ]
    for item in extracts:
        lines.append(f"  - {item}")
    lines.extend(
        [
            f"total_effective_chars: {total_chars}",
            f"total_effective_turns: {total_turns}",
            "report_due:",
            f"  micro: {'true' if micro_due else 'false'}",
            f"  periodic: {'true' if periodic_due else 'false'}",
            "---",
            "",
            f"# batch {args.month}",
            "",
            "## topics",
        ]
    )
    for topic in topics[:5] or [""]:
        lines.append(f"- {topic}")
    lines.extend(
        [
            "",
            "## repeated_patterns",
            "- 需要结合 extract 进一步分析",
            "",
            "## friction_clusters",
            "- 需要结合 extract 进一步分析",
            "",
            "## good_patterns",
            "- 需要结合 extract 进一步分析",
            "",
            "## next_report_focus",
            "- 关注最近的边界描述、纠正与反复请求",
            "",
        ]
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")

    if args.manifest_dir:
        manifest_dir = Path(args.manifest_dir)
        for extract in extracts:
            manifest_path = manifest_dir / f"{Path(extract).stem}.json"
            if not manifest_path.exists():
                continue
            text = manifest_path.read_text(encoding="utf-8")
            data = json.loads(text)
            refs = data.setdefault("included_in_batch", [])
            if output_path.as_posix() not in refs:
                refs.append(output_path.as_posix())
            manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_path.as_posix())


if __name__ == "__main__":
    main()
