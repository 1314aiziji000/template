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
    parser.add_argument("--batch", required=True)
    parser.add_argument("--mode", choices=["micro", "periodic"], required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest-dir", default="")
    args = parser.parse_args()

    batch_path = Path(args.batch)
    meta = parse_frontmatter(batch_path.read_text(encoding="utf-8", errors="ignore"))
    total_chars = int(meta.get("total_effective_chars", 0))
    total_turns = int(meta.get("total_effective_turns", 0))

    lines = [
        "---",
        f"report_id: {batch_path.stem}-{args.mode}",
        f"report_type: {args.mode}",
        f"generated_at: {batch_path.stem}",
        f"source_batch: {batch_path.as_posix()}",
        f"effective_chars: {total_chars}",
        f"effective_turns: {total_turns}",
        "---",
        "",
        f"# {args.mode} report",
        "",
        "## 这段时间你主要在做什么",
        f"- 累计处理了约 {total_turns} 条有效任务内容，共 {total_chars} 字。",
        "",
        "## 最有效的提问模式",
        "- 直接给目标、边界和交付物时，协作阻力最低。",
        "",
        "## 最容易引发误解的表达",
        "- 当边界和不做项没有一次写清时，更容易出现范围漂移。",
        "",
        "## 最近反复出现的协作摩擦",
        "- 需要在开始前先锁定边界、触发条件和真相源优先级。",
        "",
        "## 已经变好的地方",
        "- 更频繁地要求先判断，再描述，再落地。",
        "",
        "## 下次最值得试的 3 条改进动作",
        "- 开头先写目标、范围、非目标。",
        "- 对需要保留或排除的对象直接点路径。",
        "- 在进入执行前明确说明是否需要验证、提交或上传。",
        "",
    ]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")

    if args.manifest_dir:
        manifest_dir = Path(args.manifest_dir)
        for extract in meta.get("source_extracts", []):
            manifest_path = manifest_dir / f"{Path(extract).stem}.json"
            if not manifest_path.exists():
                continue
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            refs = data.setdefault("included_in_report", [])
            if output_path.as_posix() not in refs:
                refs.append(output_path.as_posix())
            manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_path.as_posix())


if __name__ == "__main__":
    main()
