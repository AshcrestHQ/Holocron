# Forge

Forge is AshcrestHQ's learn-by-doing CLI. It teaches two things side by side:

- **Security fundamentals** — the CyberHeaven-style teaching AshcrestHQ grew out of
- **Open source contribution skills** — git, commit messages, PR etiquette, code review

Both tracks share one XP and streak system. The goal isn't just "learn stuff" —
it's to get someone from zero to genuinely ready to open a real pull request
on Janus or Aegis.

## Install (local dev)

```bash
git clone https://github.com/AshcrestHQ/forge.git
cd forge
pip install -e .
```

## Usage

```bash
forge list                  # see all lessons
forge list --track security # filter by track
forge start caesar-cipher   # do a lesson by slug
forge status                # see your XP, level, and streak
forge sync                  # sync progress to leaderboard
```

Progress is stored locally at `~/.forge/progress.json`. 
You can use `forge sync` to sync your progress to the AshcrestHQ API and update your standing on the leaderboard. If you are hosting the backend yourself, please see the [FIREBASE_SETUP.md](../forge-api/FIREBASE_SETUP.md) guide in the `forge-api` repository.

## Adding a lesson

Forge is intentionally built so a new lesson is just three small files —
no changes to the CLI itself required. This makes it a genuinely easy
first PR for new contributors.

```
forge/lessons/<track>/<slug>/
    lesson.yaml   # metadata
    content.md    # the teaching content shown to the user
    check.py      # defines check(answer: str) -> bool
```

Example `lesson.yaml`:

```yaml
slug: my-new-lesson
title: "My New Lesson"
track: security   # or "dev"
xp: 15
difficulty: beginner   # beginner | intermediate | advanced
```

Then open a PR. See AshcrestHQ's general [contribution guidelines](https://ashcresthq-site.vercel.app/contribute.html)
for the full process — this repo follows the same rules as Aegis and Janus.

## License

MIT
