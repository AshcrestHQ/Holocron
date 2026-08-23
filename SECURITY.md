# Security Policy

AshcrestHQ takes the security of our tools and software seriously. Holocron is an educational CLI designed to teach cybersecurity concepts and open-source contribution practices.

## Reporting a Vulnerability

If you discover a potential security vulnerability within Holocron or the backend sync service, please report it privately:

- **Email**: [security@ashcresthq.com](mailto:security@ashcresthq.com)
- **Response Time**: We aim to acknowledge receipt within 48 hours and provide updates every 5 business days until resolution.

Please **do not** open public GitHub issues or discussions for undisclosed security vulnerabilities.

## Scope & Threat Model

Holocron is a terminal-based CLI tool. Key security considerations include:

1. **Local Lesson Execution (`check.py`)**: Lesson answer checking relies on python modules loaded dynamically from local lesson directories. Avoid executing lessons from untrusted third-party pull requests or unverified local branches.
2. **API Authentication (`holocron link` / `holocron sync`)**: Authentication tokens are stored locally in `~/.holocron/config.json`. Do not check in your configuration file or commit tokens to version control.
3. **Progress Storage (`~/.holocron/progress.json`)**: Progress tracking is stored locally on your machine.
