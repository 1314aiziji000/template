#!/usr/bin/env python3
"""Validate V3 owner-document contracts with section-aware checks."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
RETIRED_PATTERNS = (
    re.compile(r"V3落地方案"),
    re.compile(r"项目初始书\.md"),
)
LEGACY_RECORD_PATTERNS = (
    re.compile(r"`docs/errors/`"),
    re.compile(r"`docs/logs/`"),
)
SKILL_REQUIRED_SECTIONS = (
    "## 作用",
    "## 输入",
    "## 硬规则",
    "## 输出",
    "## 正式落点",
    "## 退出条件",
)


@dataclass
class MarkdownDoc:
    path: Path
    text: str
    sections: dict[str, list[str]]

    def section_text(self, heading: str) -> str:
        return "\n".join(self.sections.get(heading, []))

    def has_heading(self, heading: str) -> bool:
        return heading in self.sections

    def bullet_keys(self, heading: str) -> set[str]:
        keys: set[str] = set()
        for line in self.sections.get(heading, []):
            stripped = line.strip()
            if not stripped.startswith("- "):
                continue
            content = stripped[2:]
            key = ""
            if content.startswith("`"):
                match = re.match(r"`([^`]+)`", content)
                if match:
                    key = match.group(1).strip()
            if not key:
                match = re.match(r"(.+?)(?:\s+负责|\s+只负责|\s+不负责|\s+仍属|[：:])", content)
                if match:
                    key = match.group(1).strip().strip("`")
            if not key:
                key = re.split(r"[：:]", content, maxsplit=1)[0].strip().strip("`")
            if key:
                keys.add(key)
        return keys


class ContractVerifier:
    def __init__(self, root: Path):
        self.root = root
        self.failures: list[str] = []

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def ok(self, name: str) -> None:
        print(f"[verify-contracts] PASS {name}")

    def load_doc(self, relative_path: str) -> MarkdownDoc:
        path = self.root / relative_path
        text = path.read_text(encoding="utf-8")
        sections: dict[str, list[str]] = {}
        current = "__root__"
        sections[current] = []
        for line in text.splitlines():
            match = HEADING_RE.match(line)
            if match:
                current = match.group(2).strip()
                sections.setdefault(current, [])
                continue
            sections.setdefault(current, []).append(line)
        return MarkdownDoc(path=path, text=text, sections=sections)

    def ensure_headings(self, doc: MarkdownDoc, headings: tuple[str, ...]) -> None:
        for heading in headings:
            if not doc.has_heading(heading):
                self.fail(f"{doc.path.relative_to(self.root)} is missing heading `{heading}`.")

    def ensure_section_tokens(
        self,
        doc: MarkdownDoc,
        heading: str,
        token_groups: tuple[tuple[str, ...], ...],
    ) -> None:
        text = doc.section_text(heading)
        if not text:
            self.fail(f"{doc.path.relative_to(self.root)} is missing content under `{heading}`.")
            return
        for tokens in token_groups:
            if all(token in text for token in tokens):
                continue
            joined = " + ".join(tokens)
            self.fail(
                f"{doc.path.relative_to(self.root)} `{heading}` is missing contract tokens: {joined}."
            )

    def ensure_bullet_keys(
        self,
        doc: MarkdownDoc,
        heading: str,
        expected_keys: tuple[str, ...],
    ) -> None:
        keys = doc.bullet_keys(heading)
        for key in expected_keys:
            if key not in keys:
                self.fail(
                    f"{doc.path.relative_to(self.root)} `{heading}` is missing owner key `{key}`."
                )

    def ensure_text_tokens(self, path: str, token_groups: tuple[tuple[str, ...], ...]) -> None:
        doc = self.load_doc(path)
        for tokens in token_groups:
            if all(token in doc.text for token in tokens):
                continue
            joined = " + ".join(tokens)
            self.fail(f"{path} is missing contract tokens: {joined}.")

    def ensure_text_absent(self, path: str, forbidden_tokens: tuple[str, ...]) -> None:
        doc = self.load_doc(path)
        for token in forbidden_tokens:
            if token in doc.text:
                self.fail(f"{path} should not contain `{token}`.")

    def verify_root_readme(self) -> None:
        doc = self.load_doc("README.md")
        self.ensure_headings(
            doc,
            ("定位", "适用范围", "双态", "开始方式", "日常主链", "分层", "可选目录"),
        )
        self.ensure_section_tokens(
            doc,
            "日常主链",
            (
                ("AGENTS", "skill", "runtime"),
                ("description",),
                ("docs/workflows/intake.md",),
                ("docs/protocols/",),
                ("schemas/",),
                ("runtime/",),
                ("correction-recorder", "skill-validator"),
            ),
        )
        self.ensure_bullet_keys(
            doc,
            "分层",
            (
                "README.md",
                "AGENTS.md",
                "PROJECT_RULES.md",
                ".agents/skills/",
                "docs/workflows/",
                "docs/protocols/",
                "schemas/",
                "runtime/",
            ),
        )
        self.ensure_section_tokens(
            doc,
            "可选目录",
            (
                ("仅在当前存在或已启用时",),
                ("me/self-memory/", "不进入默认正式真相源"),
                ("workspaces/self-memory-staging/",),
            ),
        )
        self.ok("root-readme")

    def verify_agents(self) -> None:
        doc = self.load_doc("AGENTS.md")
        self.ensure_headings(
            doc,
            ("作用", "真相源", "bootstrap 守卫", "全局硬规则", "完成标准", "记录守卫"),
        )
        self.ensure_section_tokens(
            doc,
            "全局硬规则",
            (
                ("agents/openai.yaml", "不是必需件"),
                ("init_skill.py",),
                ("quick_validate.py",),
                ("SKILL.md", "主契约"),
                ("description", "policy.allow_implicit_invocation"),
                ("runtime/evolution/proposals/",),
                (".codex/skills",),  # legacy residual guard
            ),
        )
        self.ensure_section_tokens(
            doc,
            "记录守卫",
            (
                ("runtime/logs/",),
                ("runtime/evolution/",),
                ("明白", "不明白"),
                ("真实 Git 结果",),
            ),
        )
        self.ensure_text_absent(
            "AGENTS.md",
            ("## 默认路由", "Size + Risk", "Accept / Hold / Reject", "Release Card"),
        )
        self.ok("agents")

    def verify_project_rules(self) -> None:
        doc = self.load_doc("PROJECT_RULES.md")
        self.ensure_headings(
            doc,
            (
                "作用",
                "文档分类规则",
                "文档 owner 规则",
                "当前分类",
                "目录边界",
                "Bootstrap-only Assets",
                "Optional Packs 与辅助目录",
                "runtime 对象",
                "改动联动",
            ),
        )
        self.ensure_section_tokens(
            doc,
            "文档分类规则",
            (
                ("人看文档",),
                ("AI 执行文档",),
                ("混合文档",),
                ("AI 约束优先",),
            ),
        )
        self.ensure_bullet_keys(
            doc,
            "文档 owner 规则",
            (
                "AGENTS.md",
                "PROJECT_RULES.md",
                ".agents/skills/*/SKILL.md",
                ".agents/skills/*/agents/openai.yaml",
                "docs/workflows/*.md",
                "docs/protocols/*.md",
                "runtime/*.md",
            ),
        )
        self.ensure_bullet_keys(
            doc,
            "目录边界",
            (
                "README.md",
                "AGENTS.md",
                ".agents/skills/",
                "docs/workflows/",
                "docs/protocols/",
                "schemas/",
                "runtime/",
                "scripts/",
            ),
        )
        self.ensure_section_tokens(
            doc,
            "目录边界",
            (
                ("src/", "tests/"),
            ),
        )
        self.ensure_section_tokens(
            doc,
            "Optional Packs 与辅助目录",
            (
                ("仅当对象当前存在或已启用时",),
                (".codex/skills",),  # legacy residual guard
            ),
        )
        self.ensure_section_tokens(
            doc,
            "runtime 对象",
            (
                ("runtime/logs/",),
                ("runtime/evolution/",),
            ),
        )
        self.ok("project-rules")

    def verify_docs_readme(self) -> None:
        doc = self.load_doc("docs/README.md")
        self.ensure_headings(doc, ("放什么", "不放什么"))
        self.ensure_section_tokens(
            doc,
            "放什么",
            (
                ("workflows/",),
                ("protocols/",),
                ("integrations/",),
                ("ui/",),
            ),
        )
        self.ensure_section_tokens(
            doc,
            "不放什么",
            (
                ("不承担 skill 的路由契约", "description"),
                ("schemas/",),
                ("runtime/",),
                ("正式记录和正式计划不写在这里",),
            ),
        )
        self.ok("docs-readme")

    def verify_workflows(self) -> None:
        readme = self.load_doc("docs/workflows/README.md")
        self.ensure_headings(readme, ("当前范围", "workflow 停笔规则"))
        self.ensure_section_tokens(
            readme,
            "当前范围",
            (
                ("bootstrap.md",),
                ("intake.md",),
                ("build-verify-review.md",),
                ("release-retro.md",),
            ),
        )
        self.ensure_section_tokens(
            readme,
            "workflow 停笔规则",
            (
                ("阶段顺序", "进入条件", "必备产物", "下一跳"),
                ("intake.md", "不拥有 skill 内部规则"),
                ("description",),
                ("不新增 companion workflow", "context-handoff", "git-upload-logger"),
            ),
        )
        if "context-handoff" in self.load_doc("docs/workflows/build-verify-review.md").text:
            self.fail("docs/workflows/build-verify-review.md should not own companion skill routing details.")
        if "git-upload-logger" in self.load_doc("docs/workflows/build-verify-review.md").text:
            self.fail("docs/workflows/build-verify-review.md should not own companion skill routing details.")

        intake = self.load_doc("docs/workflows/intake.md")
        self.ensure_headings(
            intake,
            (
                "作用",
                "进入前检查",
                "特殊入口",
                "常规接入",
                "`Size + Risk`",
                "抬级规则",
                "常见下一跳",
                "本阶段必须产出",
                "退出去向",
            ),
        )
        self.ensure_section_tokens(
            intake,
            "特殊入口",
            (
                ("下一个窗口", "下一窗口", "context-handoff"),
                ("git add", "commit", "push", "git-upload-logger"),
                ("开始", "project-bootstrap"),
            ),
        )
        self.ensure_section_tokens(
            intake,
            "常见下一跳",
            (
                ("dev-planner",),
                ("dev-builder",),
                ("bug-fixer",),
                ("code-review",),
                ("release-builder",),
                ("docs/protocols/",),
            ),
        )

        for relative_path in (
            "docs/workflows/bootstrap.md",
            "docs/workflows/build-verify-review.md",
            "docs/workflows/release-retro.md",
        ):
            doc = self.load_doc(relative_path)
            self.ensure_headings(doc, ("定位", "进入条件", "本阶段必须产出", "退出去向"))
        self.ok("workflows")

    def verify_protocols(self) -> None:
        readme = self.load_doc("docs/protocols/README.md")
        self.ensure_headings(readme, ("当前范围", "protocol 停笔规则"))
        self.ensure_section_tokens(
            readme,
            "protocol 停笔规则",
            (
                ("最低检查", "固定字段", "证据要求"),
                ("不承担路由契约", "description"),
                ("不负责分流",),
                ("不讲完整流程",),
                ("schemas/",),
                ("runtime/",),
            ),
        )

        steering = self.load_doc("docs/protocols/steering-lite.md")
        self.ensure_headings(
            steering,
            (
                "固定对象",
                "proposal 状态机",
                "proposal 类型",
                "初始阈值",
                "证据回链",
                "owner 毕业规则",
                "meta skill 触发门槛",
                "self-memory 与 raw 清理规则",
                "上传固定节点门控",
            ),
        )
        self.ensure_section_tokens(
            steering,
            "proposal 状态机",
            (
                ("proposed",),
                ("confirmed",),
                ("graduated",),
                ("rejected",),
                ("superseded",),
                ("expired",),
            ),
        )
        self.ensure_section_tokens(
            steering,
            "proposal 类型",
            (
                ("rule-graduation",),
                ("skill-adjustment",),
                ("protocol-hardening",),
                ("verify-hardening",),
                ("new-skill-candidate",),
            ),
        )
        self.ensure_section_tokens(
            steering,
            "初始阈值",
            (
                ("verify-hardening", "3"),
                ("new-skill-candidate", "5"),
            ),
        )
        self.ensure_section_tokens(
            steering,
            "owner 毕业规则",
            (
                ("AGENTS.md",),
                ("PROJECT_RULES.md",),
                (".agents/skills/*/SKILL.md",),
                ("docs/protocols/*.md",),
                ("scripts/verify.sh",),
            ),
        )
        self.ensure_section_tokens(
            steering,
            "meta skill 触发门槛",
            (
                ("correction-recorder", "release-retro"),
                ("steering-runner", "release-retro"),
                ("user-dialogue-analyst", "阈值"),
            ),
        )
        self.ensure_section_tokens(
            steering,
            "self-memory 与 raw 清理规则",
            (
                ("workspaces/self-memory-staging/raw/",),
                ("72", "purge"),
                ("raw_id", "source_date", "hash", "counts", "extract_refs", "report_refs", "purged_at"),
            ),
        )
        self.ensure_section_tokens(
            steering,
            "上传固定节点门控",
            (
                ("400",),
                ("1200",),
                ("10", "有效任务轮次"),
            ),
        )
        self.ok("protocols")

    def verify_steering_contract_fields(self) -> None:
        field_targets = (
            (
                "runtime/evolution/proposals/README.md",
                (("target_owner", "source_records", "status"),),
            ),
            (
                ".agents/skills/steering-runner/templates/evolution-proposal-template.md",
                (("target_owner", "source_records", "status"),),
            ),
            (
                "schemas/steering/evolution-proposal.schema.json",
                (("target_owner", "source_records", "status"),),
            ),
            (
                "runtime/evolution/memory/README.md",
                (("evidence_links", "graduated_from", "owner_target", "last_verified_at"),),
            ),
            (
                ".agents/skills/steering-runner/templates/evolution-memory-template.md",
                (("evidence_links", "graduated_from", "owner_target", "last_verified_at"),),
            ),
            (
                "schemas/steering/evolution-memory.schema.json",
                (("evidence_links", "graduated_from", "owner_target", "last_verified_at"),),
            ),
        )
        for path, token_groups in field_targets:
            self.ensure_text_tokens(path, token_groups)
        self.ok("steering-contract-fields")

    def verify_runtime_and_schema_docs(self) -> None:
        runtime_doc = self.load_doc("runtime/README.md")
        self.ensure_headings(runtime_doc, ("作用", "当前对象", "边界"))
        self.ensure_section_tokens(
            runtime_doc,
            "当前对象",
            (
                ("PLANS.md",),
                ("code_review.md",),
                ("logs/",),
                ("evolution/",),
            ),
        )
        self.ensure_section_tokens(
            runtime_doc,
            "边界",
            (
                ("不定义任务怎么跑",),
                ("runtime/logs/",),
                ("runtime/evolution/",),
            ),
        )

        schema_doc = self.load_doc("schemas/README.md")
        self.ensure_headings(schema_doc, ("作用", "边界", "联动"))
        self.ensure_section_tokens(
            schema_doc,
            "边界",
            (
                ("docs/protocols/",),
                ("schemas/", "结构契约"),
                ("不放叙述性设计说明",),
                ("不放运行记录",),
            ),
        )
        self.ensure_section_tokens(
            schema_doc,
            "联动",
            (
                ("docs/protocols/",),
                ("docs/integrations/",),
                ("src/", "tests/", "evals/"),
                ("schemas/steering/",),
            ),
        )
        self.ok("runtime-and-schema-docs")

    def verify_optional_docs(self) -> None:
        optional_phrase_targets = (
            "docs/integrations/README.md",
            "prompts/README.md",
            "evals/README.md",
        )
        for relative_path in optional_phrase_targets:
            path = self.root / relative_path
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            if "仅在当前存在或已启用时" not in text:
                self.fail(f"{relative_path} should describe existence/enabled gating.")

        me_doc = self.load_doc("me/README.md")
        self.ensure_section_tokens(
            me_doc,
            "维护规则",
            (
                ("正式文件冲突", "正式文件为准"),
                ("self-memory/", "不自动进入 AI 侧默认真相源"),
            ),
        )

        workspaces_doc = self.load_doc("workspaces/README.md")
        self.ensure_headings(workspaces_doc, ("当前约定", "边界"))
        if "不是正式真相源" not in workspaces_doc.text:
            self.fail("workspaces/README.md should keep the non-truth-source boundary.")
        self.ensure_section_tokens(
            workspaces_doc,
            "边界",
            (
                ("workspaces/self-memory-staging/",),
                ("purge", "最小 manifest"),
            ),
        )

        self.ensure_text_tokens(
            "me/self-memory/README.md",
            (
                ("不进入 AI 侧默认正式真相源",),
                ("不保存长期 raw 原文",),
            ),
        )

        root_gitignore = (self.root / ".gitignore").read_text(encoding="utf-8")
        staging_gitignore = (self.root / "workspaces/self-memory-staging/.gitignore").read_text(
            encoding="utf-8"
        )
        for token in ("workspaces/self-memory-staging/raw/", "workspaces/self-memory-staging/manifests/"):
            if token not in root_gitignore:
                self.fail(f".gitignore is missing `{token}`.")
        for token in ("raw/**", "manifests/**"):
            if token not in staging_gitignore:
                self.fail(f"workspaces/self-memory-staging/.gitignore is missing `{token}`.")
        self.ok("optional-docs")

    def verify_bootstrap_brief(self) -> None:
        brief_path = self.root / "项目说明书.md"
        if not brief_path.exists():
            self.ok("bootstrap-brief")
            return
        text = brief_path.read_text(encoding="utf-8")
        for token in ("项目名称", "初始化模式", "用户确认区"):
            if token not in text:
                self.fail(f"项目说明书.md is missing `{token}`.")
        self.ok("bootstrap-brief")

    def verify_skill_structure(self) -> None:
        skills_root = self.root / ".agents/skills"
        for skill_file in sorted(skills_root.glob("*/SKILL.md")):
            text = skill_file.read_text(encoding="utf-8")
            if "## 何时使用" in text:
                self.fail(
                    f"{skill_file.relative_to(self.root)} contains legacy routing heading `## 何时使用`."
                )
            if not re.search(r"^name:\s+", text, flags=re.MULTILINE):
                self.fail(f"{skill_file.relative_to(self.root)} is missing frontmatter `name`.")
            if not re.search(r"^description:\s+", text, flags=re.MULTILINE):
                self.fail(f"{skill_file.relative_to(self.root)} is missing frontmatter `description`.")
            for heading in SKILL_REQUIRED_SECTIONS:
                if heading not in text:
                    self.fail(
                        f"{skill_file.relative_to(self.root)} is missing required section `{heading}`."
                    )
        self.ok("skill-structure")

    def verify_legacy_regressions(self) -> None:
        scan_targets = [
            self.root / "README.md",
            self.root / "AGENTS.md",
            self.root / "PROJECT_RULES.md",
            self.root / "docs",
            self.root / ".agents",
            self.root / "runtime",
        ]
        files: list[Path] = []
        for target in scan_targets:
            if target.is_file():
                files.append(target)
                continue
            files.extend(path for path in target.rglob("*.md") if ".git" not in path.parts)

        for path in files:
            text = path.read_text(encoding="utf-8", errors="ignore")
            relative_path = path.relative_to(self.root)
            for pattern in RETIRED_PATTERNS:
                if pattern.search(text):
                    self.fail(f"{relative_path} contains retired wording `{pattern.pattern}`.")
            if relative_path.as_posix() in {"README.md", "AGENTS.md", "PROJECT_RULES.md"} or relative_path.parts[:1] == ("docs",):
                for pattern in LEGACY_RECORD_PATTERNS:
                    if pattern.search(text):
                        self.fail(
                            f"{relative_path} contains legacy record sink reference `{pattern.pattern}`."
                        )
        self.ok("legacy-regressions")

    def run(self) -> int:
        self.verify_root_readme()
        self.verify_agents()
        self.verify_project_rules()
        self.verify_docs_readme()
        self.verify_workflows()
        self.verify_protocols()
        self.verify_steering_contract_fields()
        self.verify_runtime_and_schema_docs()
        self.verify_optional_docs()
        self.verify_bootstrap_brief()
        self.verify_skill_structure()
        self.verify_legacy_regressions()

        if self.failures:
            print("[verify-contracts] FAIL", file=sys.stderr)
            for failure in self.failures:
                print(f"  - {failure}", file=sys.stderr)
            return 1

        print("[verify-contracts] All document contracts passed.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate V3 document contracts.")
    parser.add_argument("--workspace-root", default=".", help="Workspace root. Defaults to current directory.")
    args = parser.parse_args()

    root = Path(args.workspace_root).resolve()
    verifier = ContractVerifier(root)
    return verifier.run()


if __name__ == "__main__":
    raise SystemExit(main())
