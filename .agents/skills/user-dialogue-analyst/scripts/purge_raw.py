#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def should_purge(manifest: dict, raw_path: Path, hours: int, force: bool):
    if force:
        return True
    if manifest.get("purged_at"):
        return False
    if not manifest.get("included_in_report"):
        return False
    if not raw_path.exists():
        return False
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    modified = datetime.fromtimestamp(raw_path.stat().st_mtime, tz=timezone.utc)
    return modified <= cutoff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-dir", required=True)
    parser.add_argument("--hours", type=int, default=72)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    manifest_dir = Path(args.manifest_dir)
    purged = []
    for path in sorted(manifest_dir.glob("*.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        raw_id = manifest.get("raw_id")
        extract_file = manifest.get("extract_file")
        raw_path = Path(extract_file).parents[4] / "workspaces" / "self-memory-staging" / "raw" / f"{raw_id}.md"
        if not raw_path.exists():
            raw_path = raw_path.with_suffix(".txt")
        if not should_purge(manifest, raw_path, args.hours, args.force):
            continue
        if raw_path.exists():
            raw_path.unlink()
        minimal_manifest = {
            "raw_id": manifest.get("raw_id"),
            "source_date": manifest.get("source_date"),
            "hash": manifest.get("raw_hash"),
            "counts": {
                "raw_turn_count": manifest.get("raw_turn_count"),
                "raw_effective_chars": manifest.get("raw_effective_chars"),
            },
            "extract_refs": [manifest.get("extract_file")],
            "report_refs": manifest.get("included_in_report", []),
            "purged_at": datetime.now(timezone.utc).isoformat(),
        }
        path.write_text(json.dumps(minimal_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        purged.append(raw_id)
    print(json.dumps({"purged": purged}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
