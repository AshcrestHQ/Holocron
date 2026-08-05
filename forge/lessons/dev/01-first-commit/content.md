# Write a Real Commit Message

A good commit message follows a simple shape used across almost every
serious open source project:

    <type>: <short, present-tense summary>

    <optional longer explanation of WHY, not just what>

Common types: `fix`, `feat`, `docs`, `refactor`, `test`, `chore`.

Bad: `fixed stuff`
Bad: `update file.py`
Good: `fix: prevent crash when config file is missing`

**Your task:** you just fixed a bug where Aegis crashed on startup if the
`.env` file was missing. Write a properly formatted commit message's first
line (just the first line, following the `<type>: <summary>` shape above).
