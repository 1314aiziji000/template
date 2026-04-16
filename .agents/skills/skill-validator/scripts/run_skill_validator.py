#!/usr/bin/env python3
"""Validate V3 skill packs against official and project-specific rules."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import yaml

POLICY_MAP = {
    "project-bootstrap": False,
    "correction-recorder": False,
    "steering-runner": False,
    "user-dialogue-analyst": False,
    "skill-validator": False,
    "dev-planner": True,
    "dev-builder": True,
    "bug-fixer": True,
    "code-review": True,
    "release-builder": True,
    "context-handoff": True,
    "git-upload-logger": True,
}

DESCRIPTION_RULES = {
    "project-bootstrap": (r"项目说明书", r"开始|初始化", r"一次性"),
    "context-handoff": (r"下一个窗口|下一窗口", r"明白", r"不明白"),
    "git-upload-logger": (r"git add", r"commit", r"push", r"上传批次"),
    "correction-recorder": (r"runtime/errors/", r"手动触发|release-retro"),
    "steering-runner": (r"runtime/evolution/", r"release-retro", r"只提议"),
    "user-dialogue-analyst": (r"self-memory", r"raw/", r"上传前|阈值"),
    "skill-validator": (r"skill-creator", r"openai.yaml", r"手动触发"),
}

LEGACY_REPO_PATTERNS = (".codex/skills",)
LEGACY_SKILL_HEADERS = ("## 何时使用",)
LEGACY_ALLOW_HINTS = ("旧", "残留", "legacy", "不允许", "reject", "scan", "校验")


@dataclass
class SkillReport:
    name: str
    passed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.passed = False
        self.errors.append(message)


def default_codex_home() -> Path:
    override = os.environ.get("CODEX_HOME")
    if override:
        return Path(override)
    return Path.home() / ".codex"


def official_script_path(script_name: str) -> Path:
    path = default_codex_home() / "skills" / ".system" / "skill-creator" / "scripts" / script_name
    if not path.exists():
        raise FileNotFoundError(f"Official skill-creator script not found: {path}")
    return path


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def extract_description(skill_md: Path) -> str:
    frontmatter = []
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return ""
    for line in lines[1:]:
        if line == "---":
            break
        frontmatter.append(line)
    data = yaml.safe_load("\n".join(frontmatter))
    if isinstance(data, dict):
        value = data.get("description", "")
        return value if isinstance(value, str) else ""
    return ""


def run_quick_validate(skill_dir: Path, script_path: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(script_path), str(skill_dir)],
        check=False,
        capture_output=True,
        text=True,
    )
    output = (result.stdout or result.stderr).strip()
    return result.returncode == 0, output


def regenerate_interface(skill_dir: Path, script_path: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix="skill-validator-") as temp_dir:
        temp_skill = Path(temp_dir) / skill_dir.name
        temp_skill.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_dir / "SKILL.md", temp_skill / "SKILL.md")
        result = subprocess.run(
            [sys.executable, str(script_path), str(temp_skill)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            output = (result.stdout or result.stderr).strip()
            raise RuntimeError(f"Failed to regenerate interface for {skill_dir.name}: {output}")
        generated_yaml = load_yaml(temp_skill / "agents" / "openai.yaml")
        return generated_yaml.get("interface", {})


def compare_interface(report: SkillReport, actual_interface: dict, generated_interface: dict) -> None:
    if not isinstance(actual_interface, dict):
        report.fail("`agents/openai.yaml` is missing a valid `interface` mapping.")
        return
    for key, expected in generated_interface.items():
        if key not in actual_interface:
            report.fail(f"`interface.{key}` is missing from `agents/openai.yaml`.")
            continue
        if actual_interface[key] != expected:
            report.fail(
                f"`interface.{key}` is not reproducible from the official generator. "
                f"expected={expected!r} actual={actual_interface[key]!r}"
            )


def validate_policy(report: SkillReport, data: dict) -> None:
    policy = data.get("policy")
    if not isinstance(policy, dict):
        report.fail("`agents/openai.yaml` is missing the project-required `policy` mapping.")
        return
    if "allow_implicit_invocation" not in policy:
        report.fail("`policy.allow_implicit_invocation` is missing.")
        return
    value = policy["allow_implicit_invocation"]
    if not isinstance(value, bool):
        report.fail("`policy.allow_implicit_invocation` must be a boolean.")
        return
    expected = POLICY_MAP.get(report.name)
    if expected is not None and value != expected:
        report.fail(
            f"`policy.allow_implicit_invocation` should be {expected!r} for `{report.name}`."
        )


def validate_description(report: SkillReport, description: str) -> None:
    rules = DESCRIPTION_RULES.get(report.name)
    if not rules:
        return
    for pattern in rules:
        if not re.search(pattern, description):
            report.fail(f"`description` is missing the required boundary signal: `{pattern}`.")


def scan_legacy_workspace_patterns(workspace_root: Path) -> list[str]:
    findings: list[str] = []
    for path in workspace_root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if ".agents" in path.parts and "skill-validator" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern in LEGACY_REPO_PATTERNS:
                if pattern not in line:
                    continue
                if any(hint in line for hint in LEGACY_ALLOW_HINTS):
                    continue
                findings.append(
                    f"{path.relative_to(workspace_root)}:{line_number} contains legacy pattern `{pattern}`."
                )
    return findings


def scan_legacy_skill_headers(skill_files: Iterable[Path], workspace_root: Path) -> list[str]:
    findings: list[str] = []
    for skill_file in skill_files:
        text = skill_file.read_text(encoding="utf-8")
        for header in LEGACY_SKILL_HEADERS:
            if header in text:
                findings.append(f"{skill_file.relative_to(workspace_root)} contains legacy header `{header}`.")
    return findings


def build_markdown_report(
    reports: list[SkillReport],
    legacy_findings: list[str],
    workspace_root: Path,
    skills_root: Path,
) -> str:
    passed = sum(1 for item in reports if item.passed)
    lines = [
        "# 07-skills-officialization",
        "",
        "## 范围",
        "",
        f"- 工作区：`{workspace_root}`",
        f"- skills 根目录：`{skills_root}`",
        "",
        "## 汇总",
        "",
        f"- 总 skill 数：`{len(reports)}`",
        f"- 通过：`{passed}`",
        f"- 失败：`{len(reports) - passed}`",
        f"- 旧口径残留：`{len(legacy_findings)}`",
        "",
        "## 逐项结果",
        "",
        "| Skill | 结果 | 备注 |",
        "| --- | --- | --- |",
    ]
    for item in reports:
        notes = item.errors or item.warnings or ["通过"]
        lines.append(f"| `{item.name}` | {'通过' if item.passed else '失败'} | {'; '.join(notes)} |")
    lines.extend(["", "## 旧口径扫描", ""])
    if legacy_findings:
        lines.extend([f"- {finding}" for finding in legacy_findings])
    else:
        lines.append("- 未发现 `.codex/skills` 或旧 skill 路由头残留。")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate V3 skill packs.")
    parser.add_argument("--workspace-root", default=".", help="Workspace root. Defaults to current directory.")
    parser.add_argument("--skills-root", default=".agents/skills", help="Skills root relative to workspace root.")
    parser.add_argument("--report", help="Optional markdown report output path.")
    args = parser.parse_args()

    workspace_root = Path(args.workspace_root).resolve()
    skills_root = (workspace_root / args.skills_root).resolve()
    quick_validate = official_script_path("quick_validate.py")
    generate_openai_yaml = official_script_path("generate_openai_yaml.py")

    if not skills_root.exists():
        print(f"[skill-validator][error] Skills root not found: {skills_root}", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    reports: list[SkillReport] = []
    skill_files: list[Path] = []

    for skill_dir in skill_dirs:
        report = SkillReport(name=skill_dir.name)
        skill_md = skill_dir / "SKILL.md"
        skill_files.append(skill_md)
        valid, output = run_quick_validate(skill_dir, quick_validate)
        if not valid:
            report.fail(f"official quick_validate failed: {output}")

        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            report.fail("`agents/openai.yaml` is missing.")
            reports.append(report)
            continue

        data = load_yaml(openai_yaml)
        actual_interface = data.get("interface", {})
        try:
            generated_interface = regenerate_interface(skill_dir, generate_openai_yaml)
        except RuntimeError as exc:
            report.fail(str(exc))
            generated_interface = {}

        compare_interface(report, actual_interface, generated_interface)
        validate_policy(report, data)
        validate_description(report, extract_description(skill_md))
        reports.append(report)

    legacy_findings = scan_legacy_workspace_patterns(workspace_root)
    legacy_findings.extend(scan_legacy_skill_headers(skill_files, workspace_root))

    if args.report:
        report_path = Path(args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            build_markdown_report(reports, legacy_findings, workspace_root, skills_root),
            encoding="utf-8",
        )

    for item in reports:
        status = "PASS" if item.passed else "FAIL"
        print(f"[skill-validator] {status} {item.name}")
        for message in item.errors:
            print(f"  - {message}")
        for message in item.warnings:
            print(f"  - warning: {message}")

    if legacy_findings:
        print("[skill-validator] FAIL legacy-scan")
        for finding in legacy_findings:
            print(f"  - {finding}")

    return 0 if all(item.passed for item in reports) and not legacy_findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
