# Contributing to AOS

Thanks for your interest. AOS is early-stage. Here's how to help.

## Setup

```bash
git clone https://github.com/<your-username>/aos.git
cd aos
pip install -r mcp_server/python/requirements.txt
```

## Run Tests

```bash
python tests/test_aos_integration.py
```

All 12 tests must pass before submitting a PR.

## Code Style

- Python 3.10+
- Follow existing patterns in the file you're editing
- Add docstrings to new classes/methods
- Keep biological metaphor consistent (metabolism, endocrine, immune, motor, etc.)

## What's Welcome

- Bug fixes
- New MCP tools
- GUI improvements
- Documentation
- Integration tests
- New biological layer implementations

## What's Not Welcome

- Removing existing metaphor layers without discussion
- Adding external API dependencies without discussion
- Breaking changes to the physiology state schema

## Reporting Bugs

Open a GitHub Issue with:
1. What you did
2. What happened
3. What you expected
4. Your environment (OS, Python version)

## Feature Requests

Open a GitHub Issue labeled `enhancement`. Explain the use case, not just the implementation.

---

*This is a first-mover project in a new category. Be bold, be kind, ship fast.*
