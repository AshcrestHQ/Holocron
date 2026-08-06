"""
Local progress tracking, stored as plain JSON in ~/.holocron/progress.json.

Deliberately simple (no DB) so the tool works offline with zero setup.
A sync-to-AshcrestHQ-leaderboard command can be layered on top of this
later without changing the local storage format.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

PROGRESS_PATH = Path.home() / ".holocron" / "progress.json"


@dataclass
class Progress:
    xp: int = 0
    completed: list[str] = field(default_factory=list)
    streak_days: int = 0
    last_active: str | None = None  # ISO date string

    def to_dict(self) -> dict:
        return {
            "xp": self.xp,
            "completed": self.completed,
            "streak_days": self.streak_days,
            "last_active": self.last_active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Progress":
        return cls(
            xp=data.get("xp", 0),
            completed=data.get("completed", []),
            streak_days=data.get("streak_days", 0),
            last_active=data.get("last_active"),
        )


def load_progress() -> Progress:
    if not PROGRESS_PATH.exists():
        return Progress()
    data = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    return Progress.from_dict(data)


def save_progress(progress: Progress) -> None:
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(json.dumps(progress.to_dict(), indent=2), encoding="utf-8")


def _update_streak(progress: Progress) -> None:
    today = date.today().isoformat()
    if progress.last_active == today:
        return  # already logged today
    if progress.last_active:
        last = datetime.fromisoformat(progress.last_active).date()
        gap = (date.today() - last).days
        progress.streak_days = progress.streak_days + 1 if gap == 1 else 1
    else:
        progress.streak_days = 1
    progress.last_active = today


def record_completion(progress: Progress, slug: str, xp: int) -> Progress:
    if slug not in progress.completed:
        progress.completed.append(slug)
        progress.xp += xp
    _update_streak(progress)
    save_progress(progress)
    return progress
