<!-- .github/copilot-instructions.md - guidance for AI coding agents in this repo -->
# Copilot / AI agent instructions — haproxy-python

This repo is a small Flask-based utility that manages HAProxy configuration through a local Python package at `haproxy_manager/` and a web UI (`app.py`, `templates/`, `static/`). Many implementation files are currently empty; treat this as a lightweight scaffold.

Key locations
- `app.py` — intended entrypoint / Flask app. If present it should expose the HTTP routes and start the server. Look here for request routing and app factory patterns.
- `haproxy_manager/` — core logic for interacting with HAProxy. Expect two primary modules:
  - `haproxy_manager/config.py` — configuration loaders/parsers and constants
  - `haproxy_manager/haproxy.py` — HAProxy control and manipulation functions
- `templates/` and `static/` — Flask templates and assets for the UI; `templates/index.html` is the main page.
- `requirements.txt` — pinned dependency list (currently includes Flask==2.3.3).

Big picture / architecture
- The app is a single-process Flask server that provides a web UI and uses the `haproxy_manager` package to read/write or control HAProxy configuration. Treat `haproxy_manager` as the service boundary for backend logic — keep web-routing thin and push logic into that package.
- Data flow: HTTP request -> `app.py` route handler -> call into `haproxy_manager` -> update files or call system commands -> return response / render template.

Agent coding conventions for this repo
- Keep web/UI and backend logic separated: handlers in `app.py` or `app` package; business logic and file/system operations belong in `haproxy_manager/*`.
- Prefer pure-Python implementations with small helper functions in `haproxy_manager`. Unit-testable functions should avoid side-effects; expose thin wrapper functions that perform the actual system calls.
- Configuration and constants belong in `haproxy_manager/config.py` (e.g., default file paths, HAProxy socket path).

How to run locally (discoverable steps)
- Create a venv and install requirements:
  - python3 -m venv .venv
  - . .venv/bin/activate
  - pip install -r requirements.txt
- Run the Flask app (two common options; inspect `app.py` for chosen pattern):
  - If `app.py` defines an app and a `if __name__ == '__main__':` block, run `python3 app.py`.
  - Otherwise use the Flask runner: `export FLASK_APP=app.py` then `flask run --host=127.0.0.1`.

Project-specific notes and assumptions (explicit)
- Many implementation files are empty in the current scaffold. When adding behavior, prefer to:
  1. Add unit tests under a `tests/` directory (not present yet).
  2. Keep public/higher-level functions documented and small.
- The repo currently uses Flask (see `requirements.txt`). Do not add conflicting web frameworks.

Integration points & external dependencies
- HAProxy itself is an external dependency. Expect the code in `haproxy_manager` to either edit HAProxy configuration files or use the HAProxy Runtime API / UNIX socket. If implementing runtime control, follow these patterns:
  - Provide pure-Python helpers that accept socket/file-path parameters (so tests can inject fakes).
  - Separate logic that formats configuration from code that writes to disk or restarts HAProxy.

Examples to reference while coding
- When adding a new route render `templates/index.html` and serve static files from `static/`.
- Add configuration defaults to `haproxy_manager/config.py` (e.g., HAPROXY_SOCKET = '/var/run/haproxy.sock') so callers can override them in tests.

Testing & debugging guidance for agents
- There are no tests present — before adding new behavior, create a small unit test for the core function you implement.
- For quick local smoke tests: after installing requirements, run the app and visit `http://127.0.0.1:5000/` (default Flask port) to confirm the server serves the template.

Merging/Editing rules for AI agents
- If `.github/copilot-instructions.md` already exists, preserve any human-written notes and append or replace only the parts that are stale. This repo currently has no existing file, so create a concise version focused on the points above.
- Avoid adding new global dependencies unless necessary; prefer writing small, testable Python helpers.

When in doubt
- If a file is empty or behavior is ambiguous, open a PR with small, well-scoped changes (one feature per PR) and include tests and a short README or inline docstring explaining the expected behavior.

Contact / follow-ups
- Ask the repo owner for HAProxy access expectations (edit files vs. runtime API) when implementing changes that will touch system components.

If anything in this file is unclear or missing for your task, tell me what you need (e.g., sample HAProxy config, expected API routes, or a preferred socket path) and I will iterate.
