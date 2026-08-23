from pathlib import Path
from holocron.core.lesson import Lesson, discover_lessons

def test_discover_lessons():
    lessons_dir = Path(__file__).parent.parent / "holocron" / "lessons"
    lessons = discover_lessons(lessons_dir)
    assert len(lessons) > 0

    slugs = [l.slug for l in lessons]
    assert "caesar-cipher" in slugs
    assert "first-commit" in slugs

def test_lesson_check_logic(tmp_path):
    lesson_dir = tmp_path / "security" / "test-lesson"
    lesson_dir.mkdir(parents=True)

    yaml_content = """
slug: test-lesson
title: Test Lesson
track: security
xp: 20
difficulty: beginner
"""
    (lesson_dir / "lesson.yaml").write_text(yaml_content, encoding="utf-8")
    (lesson_dir / "content.md").write_text("# Test content", encoding="utf-8")
    
    check_code = """
def check(answer: str) -> bool:
    return answer.strip().lower() == "secret"
"""
    (lesson_dir / "check.py").write_text(check_code, encoding="utf-8")

    discovered = discover_lessons(tmp_path)
    assert len(discovered) == 1
    lesson = discovered[0]
    
    assert lesson.slug == "test-lesson"
    assert lesson.read_content() == "# Test content"
    assert lesson.check("secret") is True
    assert lesson.check("wrong") is False
