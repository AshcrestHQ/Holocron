# Contributing to Holocron

Thank you for your interest in contributing to Holocron! Holocron is designed so that adding a new lesson requires zero changes to the core CLI logic, making it an ideal first pull request for new contributors.

## How to Add a New Lesson

A lesson consists of three files inside `holocron/lessons/<track>/<slug>/`:

```text
holocron/lessons/<track>/<slug>/
├── lesson.yaml   # Metadata (title, track, xp, difficulty)
├── content.md    # Educational content displayed in terminal
└── check.py      # Python script containing check(answer: str) -> bool
```

### 1. `lesson.yaml`
Define lesson properties:

```yaml
slug: my-lesson-slug
title: "My Lesson Title"
track: security   # "security" or "dev"
xp: 15
difficulty: beginner   # beginner | intermediate | advanced
```

### 2. `content.md`
Write clear, markdown-formatted teaching material. Explain the concept, present the challenge, and tell the user what output or format is expected as an answer.

### 3. `check.py`
Implement a `check` function that validates the user's input string:

```python
def check(answer: str) -> bool:
    """Return True if answer satisfies the challenge requirements."""
    return answer.strip().lower() == "expected_solution"
```

---

## Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AshcrestHQ/Holocron.git
   cd Holocron
   ```

2. **Install in editable mode with development dependencies**:
   ```bash
   pip install -e . pytest
   ```

3. **Run the test suite**:
   ```bash
   pytest
   ```

---

## Pull Request Guidelines

1. **Branch Naming**: Use descriptive branch names like `feat/add-jwt-lesson` or `fix/cli-typo`.
2. **Commit Messages**: Follow standard imperative style commit messages (e.g., `Add CSRF defense lesson`).
3. **Test Coverage**: Ensure all existing tests pass and add unit tests in `tests/` if introducing core CLI changes.
4. **Documentation**: Keep documentation clear and concise.
