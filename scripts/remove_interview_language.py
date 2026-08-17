#!/usr/bin/env python3
"""Remove interview-centric wording; rephrase to field/review language."""

from __future__ import annotations

import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

SKIP = {
    "AGENTS.md",
    "README.md",
    "INDEX.md",
    "WORKLOG.md",
}

# Order matters: specific patterns before broad word replacements.
TEXT_REPLACEMENTS: list[tuple[str, str]] = [
    ("## Interview Relevance", "## Why It Matters"),
    ("**Interview probes:**", "**Key signal:**"),
    ("**Interview probe:**", "**Key signal:**"),
    ("┬── Interview", "┬── Why it matters"),
    ("├── Interview", "├── Why it matters"),
    ("Interview Relevance", "Why It Matters"),
    ("interview prep", "study prep"),
    ("Interview prep", "Study prep"),
    ("interview-ready", "field-ready"),
    ("Interview-ready", "Field-ready"),
    ("Interview indexing notes", "Database indexing notes"),
    ("Interview indexing", "Database indexing"),
    ("interview indexing", "database indexing"),
    ("What strong React interviews probe", "What strong React depth checks cover"),
    ("React interviews reward", "React depth checks reward"),
    ("This note is the study map: expect", "This note is the study map — expect"),
    ("Database interviews almost always", "Database reviews almost always"),
    ("Tooling interviews care", "Tooling reviews care"),
    ("Interviewers/tooling screens:", "Reviewers on tooling screens:"),
    ("Interviewers (tooling/DX)", "Reviewers (tooling/DX)"),
    ("Interviewers ask", "Reviewers ask"),
    ("Interviewers want", "Reviewers want"),
    ("Interviewers expect", "Reviewers expect"),
    ("Interviewers check", "Reviewers check"),
    ("Interviewers like", "Reviewers like"),
    ("Interviewers probe", "Reviewers probe"),
    ("Interviewers care", "Reviewers care"),
    ("Interviewers rarely", "Reviewers rarely"),
    ("Interviewers (ops/SRE)", "Reviewers (ops/SRE)"),
    ("Interviewers (ops/", "Reviewers (ops/"),
    ("Interviewers hit", "Reviewers hit"),
    ("Interviewers test", "Reviewers test"),
    ("Interviewers still", "Reviewers still"),
    ("Interviewers and", "Reviewers and"),
    ("Interviewers ", "Reviewers "),
    ("interviewers ", "reviewers "),
    ("Pairing interviews and", "Pairing sessions and"),
    ("Ops interviews:", "Ops reviews:"),
    ("Editors ask", "Editors ask"),  # no change — anchor for context
    ("Ops and platform interviews", "Ops and platform reviews"),
    ("Staff-plus\" interviews", "Staff-plus\" reviews"),
    ("\"Staff-plus\" interviews", "\"Staff-plus\" reviews"),
    ("Staff and senior interviews", "Staff and senior reviews"),
    ("design reviews both reward", "design reviews reward"),
    (" interviews ", " reviews "),
    (" interviews.", " reviews."),
    (" interviews,", " reviews,"),
    (" interviews:", " reviews:"),
    (" interviews\"", " reviews\""),
    (" interviews'", " reviews'"),
    (" interviews—", " reviews—"),
    (" interviews;", " reviews;"),
    ("fail interviews on", "fail reviews on"),
    ("in interviews", "in reviews"),
    ("in an interview", "in a review"),
    ("for interviews", "for reviews"),
    ("an interview", "a review"),
    ("An interview", "A review"),
    ("the interview", "the review"),
    ("The interview", "The review"),
]

# Whole-line / title fixes for specific notes
NOTE_OVERRIDES: dict[str, dict[str, str]] = {
    "interview.md": {
        "# interview": "# Database indexing map",
        "> Interview indexing notes — functional dependency and the index types you'll be asked to compare under pressure.": "> Database indexing notes — functional dependency and the index types you compare under pressure.",
        "        interview ──┬── Why it matters": "        Database indexing ──┬── Why it matters",
    },
    "React/React interview.md": {
        "# React interview": "# React depth map",
        "> What strong React interviews probe — hooks rules, state placement, RSC boundaries, and debugging re-renders — with crisp trade-offs.": "> What strong React depth checks cover — hooks rules, state placement, RSC boundaries, and debugging re-renders.",
        "        React interview ──┬── Why it matters": "        React depth map ──┬── Why it matters",
    },
}


def transform_text(text: str, path: Path) -> str:
    rel = str(path.relative_to(VAULT)).replace("\\", "/")
    overrides = NOTE_OVERRIDES.get(rel, {})
    for old, new in overrides.items():
        text = text.replace(old, new)

    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)

    # Remaining standalone "interview" word (case variants)
    text = re.sub(r"\bInterview\b", "Review", text)
    text = re.sub(r"\binterview\b", "review", text)

    return text


def main() -> None:
    changed = 0
    for path in sorted(VAULT.rglob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        new = transform_text(text, path)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"changed={changed}")


if __name__ == "__main__":
    main()
