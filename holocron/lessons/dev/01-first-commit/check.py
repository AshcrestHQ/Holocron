import re

VALID_TYPES = {"fix", "feat", "docs", "refactor", "test", "chore"}


def check(answer: str) -> bool:
    answer = answer.strip()
    match = re.match(r"^(\w+):\s*(.+)$", answer)
    if not match:
        return False
    commit_type, summary = match.groups()
    if commit_type.lower() not in VALID_TYPES:
        return False
    if len(summary) < 10:
        return False
    keywords = ("env", "config", "missing", "crash", "startup")
    return any(kw in summary.lower() for kw in keywords)
