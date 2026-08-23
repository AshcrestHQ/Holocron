from unittest.mock import patch
from holocron.core.progress import Progress, load_progress, save_progress, record_completion

def test_progress_dataclass():
    p = Progress(xp=50, completed=["caesar-cipher"], streak_days=2)
    d = p.to_dict()
    assert d["xp"] == 50
    assert d["completed"] == ["caesar-cipher"]
    assert d["streak_days"] == 2

    p2 = Progress.from_dict(d)
    assert p2.xp == 50
    assert p2.completed == ["caesar-cipher"]
    assert p2.streak_days == 2

def test_record_completion(tmp_path):
    progress_file = tmp_path / "progress.json"
    with patch("holocron.core.progress.PROGRESS_PATH", progress_file):
        p = load_progress()
        assert p.xp == 0
        assert p.completed == []

        p = record_completion(p, "caesar-cipher", 15)
        assert p.xp == 15
        assert "caesar-cipher" in p.completed
        assert p.streak_days == 1

        # Duplicate completion should not grant extra XP
        p = record_completion(p, "caesar-cipher", 15)
        assert p.xp == 15
