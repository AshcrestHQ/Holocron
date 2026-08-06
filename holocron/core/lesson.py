"""
Lesson loading and data model.

A lesson is a folder like:

    lessons/security/01-caesar-cipher/
        lesson.yaml      <- metadata: title, track, xp, difficulty
        content.md       <- the actual teaching content, shown before the challenge
        check.py         <- must define a function: check(answer: str) -> bool

This keeps lessons dead simple to write and review in a PR, since a new
lesson is just three small files, no code changes to the CLI itself needed.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Lesson:
    slug: str
    title: str
    track: str          # "security" or "dev"
    xp: int
    difficulty: str      # "beginner" | "intermediate" | "advanced"
    path: Path

    @property
    def content_path(self) -> Path:
        return self.path / "content.md"

    @property
    def check_path(self) -> Path:
        return self.path / "check.py"

    def read_content(self) -> str:
        return self.content_path.read_text(encoding="utf-8")

    def check(self, answer: str) -> bool:
        """Dynamically load check.py and call its check() function."""
        spec = importlib.util.spec_from_file_location(f"holocron_check_{self.slug}", self.check_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        if not hasattr(module, "check"):
            raise ValueError(f"Lesson '{self.slug}' has no check(answer) function in check.py")
        return bool(module.check(answer))


def discover_lessons(lessons_dir: Path) -> list[Lesson]:
    """Walk lessons_dir/<track>/<slug>/lesson.yaml and build Lesson objects."""
    lessons: list[Lesson] = []
    if not lessons_dir.exists():
        return lessons

    for track_dir in sorted(lessons_dir.iterdir()):
        if not track_dir.is_dir():
            continue
        for lesson_dir in sorted(track_dir.iterdir()):
            meta_path = lesson_dir / "lesson.yaml"
            if not meta_path.exists():
                continue
            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
            lessons.append(
                Lesson(
                    slug=meta["slug"],
                    title=meta["title"],
                    track=meta.get("track", track_dir.name),
                    xp=int(meta.get("xp", 10)),
                    difficulty=meta.get("difficulty", "beginner"),
                    path=lesson_dir,
                )
            )
    return lessons
