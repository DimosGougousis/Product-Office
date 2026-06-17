#!/usr/bin/env python3
"""
Validate a YUUP agent file's frontmatter against the required schema.

Usage:
  python scripts/yuup-validate-agent.py .claude/agents/<agent-name>.md

Checks:
  - File exists and is readable
  - YAML frontmatter is valid
  - Required keys: name, description, tools
  - name is lowercase-kebab (matches filename stem)
  - tools is a valid pipe-delimited list
  - model is one of: sonnet, haiku, opus (if set)

Exit 0 = valid. Non-zero = validation error (printed to stderr).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
VALID_MODELS = {"sonnet", "haiku", "opus"}
VALID_TOOLS = {
    # VS Code Claude extension tool vocabulary
    "read_file", "write_to_file", "run_terminal", "grep", "glob",
    "list_files", "search_files", "runSubagent", "vscode_askQuestions",
    "semantic_search", "fetch_webpage", "github_text_search",
    "run_playwright_code",
    # Claude Code CLI / Anthropic Agent runtime tool vocabulary (dual-target)
    "Read", "Write", "Edit", "Bash", "Grep", "Glob",
    "WebSearch", "WebFetch", "Task", "TodoWrite", "NotebookEdit",
}


def parse_frontmatter(text: str) -> tuple[dict | None, str | None]:
    """Extract frontmatter and return (parsed_dict, raw_yaml_string)."""
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None, None
    raw = m.group(1)
    try:
        return yaml.safe_load(raw) or {}, raw
    except yaml.YAMLError as e:
        return None, str(e)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/yuup-validate-agent.py <path-to-agent-file>", file=sys.stderr)
        return 2

    agent_path = Path(sys.argv[1])
    if not agent_path.exists():
        print(f"ERROR: File not found: {agent_path}", file=sys.stderr)
        return 1

    text = agent_path.read_text(encoding="utf-8")
    fm, parse_err = parse_frontmatter(text)
    if fm is None:
        print(f"ERROR: No valid YAML frontmatter: {parse_err or 'Missing --- delimiters'}", file=sys.stderr)
        return 1

    errors = []

    # Required keys
    for key in ("name", "description", "tools"):
        if key not in fm:
            errors.append(f"Missing required key: '{key}'")

    # Name check
    if "name" in fm:
        name = fm["name"]
        if name != name.lower():
            errors.append(f"name '{name}' is not lowercase")
        if "_" in name or " " in name:
            errors.append(f"name '{name}' must be lowercase-kebab (use hyphens, not underscores or spaces)")
        expected_stem = agent_path.stem
        if name != expected_stem:
            errors.append(f"name '{name}' does not match filename stem '{expected_stem}'")

    # Model check
    if "model" in fm and fm["model"] not in VALID_MODELS:
        errors.append(f"model '{fm['model']}' not in valid models: {sorted(VALID_MODELS)}")

    # Tools check
    if "tools" in fm:
        tools_raw = fm["tools"]
        if isinstance(tools_raw, list):
            tools_list = tools_raw
        elif isinstance(tools_raw, str):
            # Split on commas or pipes (handles both delimiters)
            import re as _re
            tools_list = [t.strip() for t in _re.split(r'[,|]', tools_raw) if t.strip()]
        else:
            errors.append(f"tools must be a string or list, got {type(tools_raw).__name__}")
            tools_list = []

        for tool in tools_list:
            # Allow wildcards (mcp__*, mcp_jcodemunch*)
            if tool.endswith("*"):
                continue
            if tool not in VALID_TOOLS and not tool.startswith("mcp__"):
                errors.append(f"Unknown tool: '{tool}' (not in known tools, not an mcp__ prefix)")

    if errors:
        for err in errors:
            print(f"VALIDATION ERROR: {err}", file=sys.stderr)
        return 1

    print(f"OK: {agent_path} — name={fm.get('name')}, model={fm.get('model', 'default')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
