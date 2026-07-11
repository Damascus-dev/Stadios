"""
checkpoint.py — Automatic persistence engine for StadiumOS AI.

Usage:
    python docs/checkpoint.py --action <action> [options]

Actions:
    status              Show current session state and doc health
    checkpoint          Quick persist (updates resume context + build history)
    milestone           Full milestone checkpoint (updates all docs + build log)
    renew               Generate compact resume pack for new session
    compact             Auto-generate SESSION_CONTEXT.md for agent handoff (auto-triggered at ~85% context, end of session, before architecture changes, before phase switches)

Options:
    --session N         Session number (auto-detected if omitted)
    --phase "name"      Current phase (e.g. "Phase 7 — Foundation Stabilization")
    --changes "list"    Semicolon-separated list of changes
    --decisions "list"  Semicolon-separated decisions
    --blockers "text"   Current blockers
    --next "text"       Next priority
    --adr "text"        New ADR entry (for --action milestone)
    --quiet             Suppress output

Environment:
    RUNNING_IN_OPENSEE  set if called from OpenSee agent (suppresses some output)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

DOCS = Path(__file__).parent.resolve()
REPO = DOCS.parent


def log(msg):
    if not os.environ.get("RUNNING_IN_OPENSEE"):
        print(f"  [OK] {msg}")


def warn(msg):
    if not os.environ.get("RUNNING_IN_OPENSEE"):
        print(f"  [!] {msg}")


def read_file(path):
    p = Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def write_file(path, content):
    Path(path).write_text(content, encoding="utf-8")


def append_file(path, content):
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def auto_session():
    """Auto-detect next session number from BUILD_HISTORY.md."""
    content = read_file(DOCS / "BUILD_HISTORY.md")
    matches = re.findall(r"Session (\d+)", content)
    if matches:
        return max(int(m) for m in matches) + 1
    return 1


def auto_phase():
    """Auto-detect current phase from PROJECT_STATE.md."""
    content = read_file(DOCS / "PROJECT_STATE.md")
    m = re.search(r"\*\*(Phase \d+.*?)\*\*", content)
    return m.group(1) if m else "Unknown"


def auto_adr_number():
    """Auto-detect next ADR number from DECISIONS.md."""
    content = read_file(DOCS / "DECISIONS.md")
    matches = re.findall(r"ADR-(\d+)", content)
    return max(int(m) for m in matches) + 1 if matches else 1


def update_resume_context(changes, decisions, blockers, next_priority):
    """Update the Resume Context section of PROJECT_STATE.md."""
    path = DOCS / "PROJECT_STATE.md"
    content = read_file(path)
    if not content:
        warn("PROJECT_STATE.md not found")
        return

    today = date.today().isoformat()
    prefix = f">{today}"
    if decisions:
        prefix += f" | decisions: {decisions[:120]}"

    resume_entry = f"\n> {prefix}\n\n**Changes this session**:\n"
    if changes:
        for c in changes.split(";"):
            c = c.strip()
            if c:
                resume_entry += f"- {c}\n"
    else:
        resume_entry += "- (no changes recorded)\n"

    if decisions:
        resume_entry += "\n**Decisions**:\n"
        for d in decisions.split(";"):
            d = d.strip()
            if d:
                resume_entry += f"- {d}\n"

    if blockers:
        resume_entry += f"\n**Blockers**: {blockers}\n"

    if next_priority:
        resume_entry += f"\n**Next**: {next_priority}\n"

    resume_entry += "\n"

    # Replace existing resume context section
    if "## Resume Context" in content:
        before = content.split("## Resume Context")[0]
        after_marker = "---\n\n> Last updated:"
        if after_marker in content:
            after_part = content.split("## Resume Context")[1]
            after = after_marker + after_part.split(after_marker)[1] if after_marker in after_part else ""
        else:
            after = ""
        new_content = before + "## Resume Context\n\n" + resume_entry + "\n" + after
    else:
        new_content = content + "\n## Resume Context\n\n" + resume_entry

    # Update last updated date
    new_content = re.sub(
        r"> Last updated:.*",
        f"> Last updated: {today}",
        new_content,
    )

    write_file(path, new_content)
    log(f"PROJECT_STATE.md updated")


def append_build_history(session, phase, changes, decisions, blockers):
    """Append to BUILD_HISTORY.md."""
    path = DOCS / "BUILD_HISTORY.md"
    today = date.today().isoformat()

    entry = f"\n## {today} — Session {session:03d}: Checkpoint\n\n"
    entry += f"**Phase**: {phase}\n\n"

    if changes:
        for c in changes.split(";"):
            c = c.strip()
            if c:
                entry += f"- {c}\n"

    if decisions:
        entry += "\n**Decisions**:\n"
        for d in decisions.split(";"):
            d = d.strip()
            if d:
                entry += f"- {d}\n"

    if blockers:
        entry += f"\n**Blockers**: {blockers}\n"

    entry += "\n---\n"
    append_file(path, entry)
    log(f"BUILD_HISTORY.md appended")


def create_build_log(session, phase, changes, decisions, blockers):
    """Create a build log file for the session."""
    path = DOCS / "build_logs" / f"session_{session:03d}.md"
    today = date.today().isoformat()

    Path(DOCS / "build_logs").mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Session {session:03d} — Auto Checkpoint",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| **Date** | {today} |",
        f"| **Phase** | {phase} |",
        "",
        "## What Was Done",
    ]

    if changes:
        for c in changes.split(";"):
            c = c.strip()
            if c:
                lines.append(f"- {c}")

    if decisions:
        lines.extend(["", "## Decisions Made"])
        for d in decisions.split(";"):
            d = d.strip()
            if d:
                lines.append(f"- {d}")

    if blockers:
        lines.extend(["", f"## Blockers", blockers])

    write_file(path, "\n".join(lines) + "\n")
    log(f"build_logs/session_{session:03d}.md created")


def update_todo(completed, added):
    """Update TODO.md — mark items complete, add new items."""
    path = DOCS / "TODO.md"
    content = read_file(path)
    if not content:
        warn("TODO.md not found")
        return

    today = date.today().isoformat()

    if completed:
        for item in completed.split(";"):
            item = item.strip()
            if item:
                content = content.replace(f"- [ ] {item}", f"- [x] {item}  # {today}")

    if added:
        for item in added.split(";"):
            item = item.strip()
            if item and f"- [ ] {item}" not in content:
                content += f"\n- [ ] {item}"

    write_file(path, content)
    log(f"TODO.md updated")


def append_decision(decision_text):
    """Append a new ADR to DECISIONS.md."""
    path = DOCS / "DECISIONS.md"
    content = read_file(path)
    if not content:
        warn("DECISIONS.md not found")
        return

    adr_num = auto_adr_number()
    today = date.today().isoformat()

    entry = (
        f"\n## ADR-{adr_num:03d}\n\n"
        f"**Date**: {today}\n\n"
        f"**Decision**: {decision_text}\n\n"
        f"**Status**: Accepted\n"
        f"\n---\n"
    )

    append_file(path, entry)
    log(f"ADR-{adr_num:03d} added to DECISIONS.md")


def _get_git_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=REPO, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else "main"
    except Exception:
        return "main"


def _get_dir_tree(path: Path, prefix: str = "", max_depth: int = 2) -> str:
    """Get a compact directory tree representation."""
    if max_depth < 0:
        return ""
    lines = []
    try:
        entries = sorted([e for e in path.iterdir() if not e.name.startswith((".", "__pycache__", "node_modules", ".venv", ".next")) and e.is_dir()])
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry.name}/")
            lines.append(_get_dir_tree(entry, prefix + ("    " if is_last else "│   "), max_depth - 1))
    except PermissionError:
        pass
    return "\n".join(lines)


def _list_files(pattern: str, root: Path = None) -> list[str]:
    """List files matching a glob pattern, relative to root."""
    root = root or REPO
    try:
        result = []
        for p in root.rglob(pattern):
            if not any(part.startswith((".", "__pycache__", "node_modules", ".venv")) for part in p.parts):
                rel = p.relative_to(REPO)
                result.append(str(rel))
        return sorted(result)
    except Exception:
        return []


def generate_session_context(session: int, phase: str, changes: str, decisions: str, blockers: str, next_task: str):
    """Generate SESSION_CONTEXT.md — canonical one-file agent handoff document."""
    today = date.today().isoformat()
    branch = _get_git_branch()

    # Read supporting docs
    state_content = read_file(DOCS / "PROJECT_STATE.md")
    todo_content = read_file(DOCS / "TODO.md")
    build_content = read_file(DOCS / "BUILD_HISTORY.md")

    # Extract open TODOs
    open_todos = re.findall(r"- \[ \] (.+)", todo_content)
    open_decisions = []
    if "## Open Decisions" in state_content:
        od_section = state_content.split("## Open Decisions")[1].split("##")[0]
        open_decisions = [l.strip("- ") for l in od_section.strip().split("\n") if l.strip().startswith("- ")]

    # Extract known issues
    known_issues = []
    if "## Known Issues" in state_content:
        ki_section = state_content.split("## Known Issues")[1].split("##")[0]
        known_issues = [l.strip("- ") for l in ki_section.strip().split("\n") if l.strip().startswith("- ")]

    # Get key file lists
    py_files = _list_files("*.py")[:30]
    ts_files = _list_files("*.ts") + _list_files("*.tsx")
    ts_files = [f for f in ts_files if not f.startswith("node_modules")][:30]

    # Architecture snapshot
    arch_snapshot = ""
    if read_file(DOCS / "ARCHITECTURE.md"):
        arch_lines = read_file(DOCS / "ARCHITECTURE.md").split("\n")
        # Extract first meaningful section about data flow
        in_data_flow = False
        data_flow_lines = []
        for line in arch_lines:
            if "## Data Flow" in line:
                in_data_flow = True
                continue
            if in_data_flow:
                if line.startswith("## "):
                    break
                data_flow_lines.append(line)
        arch_snapshot = "\n".join(data_flow_lines).strip() if data_flow_lines else "See ARCHITECTURE.md"

    # Build change lines
    change_items = []
    if changes:
        for c in changes.split(";"):
            c = c.strip()
            if c:
                change_items.append(c)

    context = f"""# StadiumOS AI — Session Context

> Auto-generated by `docs/checkpoint.py --action compact`.
> **Single source of truth for AI agent handoff.** Read this immediately after BOOTSTRAP.md.

---

## Session

| Field | Value |
|---|---|
| **Session** | {session} |
| **Date** | {today} |
| **Phase** | {phase} |
| **Branch** | `{branch}` |

---

## Current Goal

{next_task or "See TODO.md for active tasks."}

---

## Completed This Session

"""
    if change_items:
        for c in change_items:
            context += f"- {c}\n"
    else:
        context += "- (no changes recorded in this compaction)\n"

    context += f"""
---

## Active Tasks

"""
    if open_todos:
        for t in open_todos[:15]:
            context += f"- [ ] {t}\n"
    else:
        context += "- No open tasks.\n"

    context += f"""
---

## Blockers

{blockers if blockers else "None"}

---

## Open Decisions / Pending ADRs

"""
    if open_decisions:
        for d in open_decisions:
            context += f"- {d}\n"
    else:
        context += "- No open decisions.\n"

    context += f"""
---

## Known Issues

"""
    if known_issues:
        for i in known_issues:
            context += f"- {i}\n"
    else:
        context += "- None reported.\n"

    context += f"""
---

## Architecture Snapshot

{arch_snapshot}

---

## Key Files (New/Modified)

**Python:**
"""
    for f in py_files[:15]:
        context += f"- `{f}`\n"

    context += """
**TypeScript/TSX:**
"""
    for f in ts_files[:15]:
        context += f"- `{f}`\n"

    context += f"""
---

## API Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | /api/health | Health check |
| GET | /api/dashboard/ | Full dashboard snapshot |
| POST | /api/navigation/route | Route planning |
| GET | /api/navigation/zones | List navigable zones |
| GET | /api/alerts/ | List alerts |
| POST | /api/alerts/{{id}}/acknowledge | Acknowledge alert |
| POST | /api/agents/{{agent_type}} | Agent query |
| POST | /api/agents/detect-intent | Intent classification |

---

## Agent Handoff Notes

**Do NOT modify without explicit approval:**
- API contracts (existing Pydantic schemas)
- Folder structure
- Dashboard layout (8 tiles)
- Three-tier fallback architecture
- Provider abstraction interface
- Operations/dashboard engine interface

**Auto-compaction triggers** (run `python docs/checkpoint.py --action compact`):
- When context reaches ~85-90% utilization
- Before ending any coding session
- Before major architecture changes
- Before switching implementation phases
- At end of every completed phase

**Phase completion checklist** (end of every phase):
1. Update PROJECT_STATE.md
2. Update BUILD_HISTORY.md
3. Update TODO.md
4. Update DECISIONS.md (if architecture changed)
5. Regenerate SESSION_CONTEXT.md (`--action compact`)

---

## Next Immediate Task

{next_task or "See TODO.md"}

---

> Last regenerated: {today}
"""

    write_file(DOCS / "SESSION_CONTEXT.md", context)
    log(f"SESSION_CONTEXT.md regenerated for Session {session}")


def cmd_compact(args):
    """Auto-generate SESSION_CONTEXT.md for agent handoff."""
    session = args.session or auto_session()
    phase = args.phase or auto_phase()
    changes = args.changes or ""
    decisions = args.decisions or ""
    blockers = args.blockers or ""
    next_task = args.next or ""

    generate_session_context(session, phase, changes, decisions, blockers, next_task)

    if not args.quiet:
        log(f"Session context compacted (Session {session})")
        log("docs/SESSION_CONTEXT.md — ready for next agent handoff")


def generate_renewal_pack(session, phase):
    """Generate compact resume text for a new agent session."""
    state = read_file(DOCS / "PROJECT_STATE.md")
    todo = read_file(DOCS / "TODO.md")
    build = read_file(DOCS / "BUILD_HISTORY.md")
    arch = read_file(DOCS / "ARCHITECTURE.md")

    # Extract resume context
    resume = ""
    if "## Resume Context" in state:
        resume = state.split("## Resume Context")[1].split("---")[0].strip()

    # Extract open TODO items
    open_todos = re.findall(r"- \[ \] (.+)", todo)

    # Extract most recent build entry
    recent = ""
    entries = re.split(r"\n---\n", build)
    if entries:
        recent = entries[-1].strip()

    pack = f"""# StadiumOS AI — Session Renewal Pack

> Auto-generated for session continuity. Covers: {session}.

---

## Resume Context

{resume}

---

## Open Tasks

"""
    for t in open_todos[:10]:
        pack += f"- [ ] {t}\n"

    pack += f"""
---

## Most Recent Activity

{recent}

---

## Architecture Snapshot (key details)

"""
    # Extract architecture key points from ARCHITECTURE.md
    if "## Data Flow" in arch:
        pack += arch.split("## Data Flow")[1].split("##")[0].strip() + "\n"

    pack += f"""
---

## Key Files
- `docs/PROJECT_STATE.md` — single source of truth
- `docs/TODO.md` — active tasks
- `docs/ARCHITECTURE.md` — system architecture
- `docs/BUILD_HISTORY.md` — chronological log
- `docs/DECISIONS.md` — architecture decisions
- `docs/build_logs/session_{session:03d}.md` — most recent detail log
- `docs/planning/appendix_c.md` — persistence protocol
"""

    write_file(DOCS / "renewal_pack.md", pack)
    log(f"renewal_pack.md generated")


def cmd_status(args):
    """Show current session state and document health."""
    session = auto_session()
    phase = auto_phase()
    today = date.today().isoformat()

    docs_status = {}
    for name in ["PROJECT_STATE.md", "BUILD_HISTORY.md", "DECISIONS.md", "TODO.md", "ARCHITECTURE.md", "SESSION_CONTEXT.md"]:
        p = DOCS / name
        docs_status[name] = "[OK]" if p.exists() else "[MISSING]"

    print(f"\n=== Persistence Status ===")
    print(f"Date:    {today}")
    print(f"Session: {session}")
    print(f"Phase:   {phase}")
    print()
    print("Documents:")
    for name, status in docs_status.items():
        print(f"  {status} {name}")
    print(f"\nNext session number: {session}")
    print(f"Next ADR number:    {auto_adr_number()}")
    print()


def cmd_checkpoint(args):
    """Quick persist — resume context + build history."""
    session = args.session or auto_session()
    phase = args.phase or auto_phase()
    changes = args.changes or ""
    decisions = args.decisions or ""
    blockers = args.blockers or ""
    next_priority = args.next or ""

    update_resume_context(changes, decisions, blockers, next_priority)
    append_build_history(session, phase, changes, decisions, blockers)

    if not args.quiet:
        log(f"Checkpoint complete (Session {session})")


def cmd_milestone(args):
    """Full milestone checkpoint — all docs + build log."""
    session = args.session or auto_session()
    phase = args.phase or auto_phase()
    changes = args.changes or ""
    decisions = args.decisions or ""
    blockers = args.blockers or ""
    next_priority = args.next or ""
    adr_text = args.adr or ""

    update_resume_context(changes, decisions, blockers, next_priority)
    append_build_history(session, phase, changes, decisions, blockers)
    create_build_log(session, phase, changes, decisions, blockers)

    if adr_text:
        append_decision(adr_text)

    if args.completed_todo or args.added_todo:
        update_todo(args.completed_todo, args.added_todo)

    if not args.quiet:
        log(f"Milestone checkpoint complete (Session {session})")


def cmd_renew(args):
    """Generate compact resume pack for new session."""
    session = args.session or auto_session()
    phase = args.phase or auto_phase()
    generate_renewal_pack(session, phase)

    if not args.quiet:
        log(f"Renewal pack generated for Session {session}")
        log("docs/renewal_pack.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="StadiumOS AI Persistence Engine")
    parser.add_argument("--action", required=True, choices=["status", "checkpoint", "milestone", "renew", "compact"])
    parser.add_argument("--session", type=int, default=None)
    parser.add_argument("--phase", default=None)
    parser.add_argument("--changes", default="")
    parser.add_argument("--decisions", default="")
    parser.add_argument("--blockers", default="")
    parser.add_argument("--next", default="")
    parser.add_argument("--adr", default="")
    parser.add_argument("--completed-todo", default="")
    parser.add_argument("--added-todo", default="")
    parser.add_argument("--quiet", action="store_true")

    args = parser.parse_args()

    actions = {
        "status": cmd_status,
        "checkpoint": cmd_checkpoint,
        "milestone": cmd_milestone,
        "renew": cmd_renew,
        "compact": cmd_compact,
    }

    actions[args.action](args)
