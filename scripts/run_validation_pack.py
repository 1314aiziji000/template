#!/usr/bin/env python3
"""Run the V3 validation-pack automation gates."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class CaseResult:
    case_id: str
    passed: bool = True
    details: list[str] = field(default_factory=list)
    command: list[str] | None = None

    def fail(self, message: str) -> None:
        self.passed = False
        self.details.append(message)

    def note(self, message: str) -> None:
        self.details.append(message)


def run_command(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        command,
        cwd=cwd,
        env=merged_env,
        text=True,
        capture_output=True,
        check=False,
    )


def require(condition: bool, report: CaseResult, message: str) -> None:
    if not condition:
        report.fail(message)


def handle_command_case(case: dict[str, object], root: Path) -> CaseResult:
    report = CaseResult(case_id=str(case["id"]))
    workdir = (root / str(case.get("workdir", "."))).resolve()
    command = [str(part) for part in case["command"]]
    report.command = command
    result = run_command(command, cwd=workdir, env={str(k): str(v) for k, v in dict(case.get("env", {})).items()})
    expected_exit = int(case.get("expect_exit_code", 0))
    require(result.returncode == expected_exit, report, f"expected exit code {expected_exit}, got {result.returncode}")
    if result.stdout.strip():
        report.note(result.stdout.strip().splitlines()[-1])
    if result.stderr.strip():
        report.note(result.stderr.strip().splitlines()[-1])
    return report


def handle_scenario_coverage(case: dict[str, object], root: Path) -> CaseResult:
    report = CaseResult(case_id=str(case["id"]))
    skills_root = (root / str(case["skills_dir"])).resolve()
    scenarios_dir = (root / str(case["scenarios_dir"])).resolve()
    required_sections = [str(item) for item in case.get("required_sections", [])]
    extra_scenarios = [str(item) for item in case.get("extra_scenarios", [])]

    skill_names = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
    scenario_map: dict[str, Path] = {}
    for path in sorted(scenarios_dir.glob("*.md")):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if not lines:
            report.fail(f"{path.relative_to(root)} is empty")
            continue
        first_line = lines[0].strip()
        if first_line.startswith("# Scenario: "):
            scenario_map[first_line.removeprefix("# Scenario: ").strip()] = path

    missing = [skill for skill in skill_names if skill not in scenario_map]
    require(not missing, report, f"missing scenario files for skills: {', '.join(missing)}")

    for name in skill_names:
        scenario_path = scenario_map.get(name)
        if not scenario_path:
            continue
        text = scenario_path.read_text(encoding="utf-8", errors="ignore")
        for section in required_sections:
            require(section in text, report, f"{scenario_path.relative_to(root)} is missing `{section}`")

    for name in extra_scenarios:
        scenario_path = scenario_map.get(name)
        require(scenario_path is not None, report, f"missing extra scenario `{name}`")

    covered = len(skill_names) - len(missing)
    report.note(f"{covered}/{len(skill_names)} skills have positive/negative scenario coverage.")
    return report


def handle_skill_validator(case: dict[str, object], root: Path) -> CaseResult:
    report = CaseResult(case_id=str(case["id"]))
    script_path = (root / str(case.get("script", ".agents/skills/skill-validator/scripts/run_skill_validator.py"))).resolve()
    report_path = (root / str(case["report"])).resolve()
    expected_skill_count = int(case["expected_skill_count"])
    command = [
        sys.executable,
        str(script_path),
        "--workspace-root",
        str(root),
        "--report",
        str(report_path),
    ]
    report.command = command
    result = run_command(command, cwd=root)
    require(result.returncode == 0, report, "skill-validator exited non-zero")
    require(report_path.exists(), report, f"expected report not found: {report_path.relative_to(root)}")
    if report_path.exists():
        text = report_path.read_text(encoding="utf-8", errors="ignore")
        require(f"- 总 skill 数：`{expected_skill_count}`" in text, report, "skill count summary does not match")
        require("- 失败：`0`" in text, report, "skill-validator report still contains failures")
        report.note(report_path.relative_to(root).as_posix())
    return report


def handle_steering_scan(case: dict[str, object], root: Path) -> CaseResult:
    report = CaseResult(case_id=str(case["id"]))
    script_path = (root / "scripts/scan-steering-signals.py").resolve()
    errors_dir = (root / str(case["errors_dir"])).resolve()
    expected = dict(case.get("expected", {}))
    rejected_types = [str(item) for item in case.get("rejected_proposal_types", [])]

    with tempfile.TemporaryDirectory(prefix="v3-steering-empty-") as temp_dir:
        temp_root = Path(temp_dir)
        logs_dir = temp_root / "empty-logs"
        reviews_dir = temp_root / "empty-reviews"
        logs_dir.mkdir(parents=True, exist_ok=True)
        reviews_dir.mkdir(parents=True, exist_ok=True)
        command = [
            sys.executable,
            str(script_path),
            "--errors",
            str(errors_dir),
            "--logs",
            str(logs_dir),
            "--reviews",
            str(reviews_dir),
        ]
        report.command = command
        result = run_command(command, cwd=root)
        require(result.returncode == 0, report, "scan-steering-signals.py exited non-zero")
        data = json.loads(result.stdout or "{}")
        proposals = list(data.get("proposals", []))
        require(len(proposals) == int(expected.get("proposal_count", 0)), report, "proposal count mismatch")
        if proposals:
            proposal = proposals[0]
            for key in ("proposal_type", "signal_type", "repeat_count", "target_owner", "target_path"):
                if key in expected:
                    require(
                        proposal.get(key) == expected[key],
                        report,
                        f"expected `{key}`={expected[key]!r}, got {proposal.get(key)!r}",
                    )
            for rejected_type in rejected_types:
                require(
                    proposal.get("proposal_type") != rejected_type,
                    report,
                    f"unexpected proposal type `{rejected_type}` was produced",
                )
            report.note(
                f"{proposal.get('proposal_type')} -> {proposal.get('target_owner')} with repeat_count={proposal.get('repeat_count')}"
            )
    return report


def handle_self_memory_flow(case: dict[str, object], root: Path) -> CaseResult:
    report = CaseResult(case_id=str(case["id"]))
    raw_source_dir = (root / str(case["raw_dir"])).resolve()
    expected = dict(case.get("expected", {}))
    month = str(case["month"])
    report_mode = str(case.get("report_mode", "periodic"))

    extract_script = (root / ".agents/skills/user-dialogue-analyst/scripts/extract_dialogue.py").resolve()
    batch_script = (root / ".agents/skills/user-dialogue-analyst/scripts/roll_batch.py").resolve()
    report_script = (root / ".agents/skills/user-dialogue-analyst/scripts/build_report.py").resolve()
    purge_script = (root / ".agents/skills/user-dialogue-analyst/scripts/purge_raw.py").resolve()

    with tempfile.TemporaryDirectory(prefix="v3-self-memory-") as temp_dir:
        temp_root = Path(temp_dir)
        staging_raw_dir = temp_root / "workspaces/self-memory-staging/raw"
        manifest_dir = temp_root / "workspaces/self-memory-staging/manifests"
        extract_dir = temp_root / "me/self-memory/extracts" / month
        batch_dir = temp_root / "me/self-memory/batches"
        report_dir = temp_root / "me/self-memory/reports" / report_mode

        for directory in (staging_raw_dir, manifest_dir, extract_dir, batch_dir, report_dir):
            directory.mkdir(parents=True, exist_ok=True)

        raw_files = sorted(path for path in raw_source_dir.iterdir() if path.is_file())
        for raw_file in raw_files:
            target_raw = staging_raw_dir / raw_file.name
            shutil.copy2(raw_file, target_raw)
            extract_output = extract_dir / raw_file.name
            manifest_output = manifest_dir / f"{raw_file.stem}.json"
            command = [
                sys.executable,
                str(extract_script),
                "--input",
                str(target_raw),
                "--output",
                str(extract_output),
                "--manifest",
                str(manifest_output),
            ]
            result = run_command(command, cwd=root)
            require(result.returncode == 0, report, f"extract failed for {raw_file.name}")

        batch_path = batch_dir / f"{month}-batch-001.md"
        batch_result = run_command(
            [
                sys.executable,
                str(batch_script),
                "--extract-dir",
                str(extract_dir),
                "--month",
                month,
                "--output",
                str(batch_path),
                "--manifest-dir",
                str(manifest_dir),
            ],
            cwd=root,
        )
        require(batch_result.returncode == 0, report, "roll_batch.py exited non-zero")

        report_path = report_dir / f"{month}-batch-001-{report_mode}.md"
        report_result = run_command(
            [
                sys.executable,
                str(report_script),
                "--batch",
                str(batch_path),
                "--mode",
                report_mode,
                "--output",
                str(report_path),
                "--manifest-dir",
                str(manifest_dir),
            ],
            cwd=root,
        )
        require(report_result.returncode == 0, report, "build_report.py exited non-zero")

        purge_result = run_command(
            [
                sys.executable,
                str(purge_script),
                "--manifest-dir",
                str(manifest_dir),
                "--force",
            ],
            cwd=root,
        )
        require(purge_result.returncode == 0, report, "purge_raw.py exited non-zero")

        extract_count = len(list(extract_dir.glob("*.md")))
        batch_count = len(list(batch_dir.glob("*.md")))
        report_count = len(list(report_dir.glob("*.md")))
        purged_raw_count = len(list(staging_raw_dir.glob("*.md"))) + len(list(staging_raw_dir.glob("*.txt")))
        require(extract_count == int(expected["extracts"]), report, "extract count mismatch")
        require(batch_count == int(expected["batches"]), report, "batch count mismatch")
        require(report_count == int(expected["reports"]), report, "report count mismatch")
        require(purged_raw_count == 0, report, "raw files were not purged")

        manifest_keys = [str(item) for item in expected.get("manifest_keys", [])]
        for manifest_path in sorted(manifest_dir.glob("*.json")):
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            require(
                sorted(data.keys()) == sorted(manifest_keys),
                report,
                f"{manifest_path.name} does not keep the minimal manifest shape",
            )
            counts = data.get("counts", {})
            require(isinstance(counts, dict), report, f"{manifest_path.name} is missing `counts` object")
            require(
                {"raw_turn_count", "raw_effective_chars"} <= set(counts.keys()),
                report,
                f"{manifest_path.name} `counts` is missing expected fields",
            )

        report.note(
            f"{extract_count} extracts, {batch_count} batch, {report_count} {report_mode} report, raw purged"
        )
    return report


def build_markdown_report(results: list[CaseResult], manifest_path: Path) -> str:
    passed = sum(1 for result in results if result.passed)
    lines = [
        "# 08-validation-pack-automation",
        "",
        "## 范围",
        "",
        f"- manifest：`{manifest_path.as_posix()}`",
        "",
        "## 汇总",
        "",
        f"- 总 case 数：`{len(results)}`",
        f"- 通过：`{passed}`",
        f"- 失败：`{len(results) - passed}`",
        "",
        "## 逐项结果",
        "",
        "| Case | 结果 | 备注 |",
        "| --- | --- | --- |",
    ]
    for result in results:
        note = "; ".join(result.details) if result.details else "通过"
        lines.append(f"| `{result.case_id}` | {'通过' if result.passed else '失败'} | {note} |")
    return "\n".join(lines) + "\n"


def run_case(case: dict[str, object], root: Path) -> CaseResult:
    case_type = str(case["type"])
    if case_type == "command":
        return handle_command_case(case, root)
    if case_type == "scenario_coverage":
        return handle_scenario_coverage(case, root)
    if case_type == "skill_validator":
        return handle_skill_validator(case, root)
    if case_type == "steering_scan":
        return handle_steering_scan(case, root)
    if case_type == "self_memory_flow":
        return handle_self_memory_flow(case, root)
    result = CaseResult(case_id=str(case["id"]), passed=False)
    result.fail(f"unsupported case type `{case_type}`")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run V3 validation-pack automation.")
    parser.add_argument("--workspace-root", default=".", help="Workspace root. Defaults to current directory.")
    parser.add_argument(
        "--manifest",
        default="workspaces/v3-validation-pack/acceptance.manifest.yaml",
        help="Validation-pack manifest path relative to workspace root.",
    )
    parser.add_argument(
        "--report",
        default="workspaces/v3-validation-pack/reports/08-validation-pack-automation.md",
        help="Markdown report path relative to workspace root.",
    )
    args = parser.parse_args()

    root = Path(args.workspace_root).resolve()
    manifest_path = (root / args.manifest).resolve()
    report_path = (root / args.report).resolve()

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    cases = list(manifest.get("cases", []))
    results = [run_case(case, root) for case in cases]

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_markdown_report(results, manifest_path.relative_to(root)), encoding="utf-8")

    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[validation-pack] {status} {result.case_id}")
        for detail in result.details:
            print(f"  - {detail}")

    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
