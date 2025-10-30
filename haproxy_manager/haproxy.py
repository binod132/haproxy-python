"""Minimal HAProxy control helpers for the scaffold.

These are lightweight stubs so the Flask app can import them during
development. Replace with real implementations that use the HAProxy
Runtime API or file editing as needed.
"""

from typing import Any

def toggle_server(server: str, comment: Any = False) -> None:
    """Stub: toggle a server's enabled/disabled state.

    In a real implementation this would call the HAProxy runtime socket
    or edit configuration files. Keep the function signature stable so
    callers (e.g., `app.py`) can be unit tested.
    """
    # No-op for scaffold
    return None


def reload_haproxy() -> None:
    """Stub: reload HAProxy config.

    Real code should call systemctl / service control or the binary with
    proper flags. Keep the operation isolated so tests can stub it.
    """
    return None

def parse_config():
    """Parse HAProxy config to find backends and their servers."""
    import importlib
    from . import config as _config
    importlib.reload(_config)
    HAPROXY_CFG = _config.HAPROXY_CFG

    backends = {}
    current_backend = None

    try:
        with open(HAPROXY_CFG, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("backend"):
                    current_backend = line.split()[1]
                    backends[current_backend] = []
                elif line.startswith("server") and current_backend:
                    server_name = line.split()[1]
                    backends[current_backend].append(server_name)
    except (FileNotFoundError, IndexError):
        # Return empty dict if config is missing or malformed
        return {}

    return backends

import re
import subprocess

def toggle_server(server_name, comment=True):
    """Comment or uncomment a server line in HAProxy config."""
    # Import and reload config at call-time so changes to
    # `haproxy_manager/config.py` on disk are picked up without
    # restarting the running Flask process.
    import importlib
    from . import config as _config
    importlib.reload(_config)
    HAPROXY_CFG = _config.HAPROXY_CFG
    try:
        with open(HAPROXY_CFG, "r") as f:
            lines = f.readlines()

        new_lines = []
        server_pattern = re.compile(rf"^\s*(#\s*)?server\s+{server_name}\b")

        for line in lines:
            m = server_pattern.match(line)
            if m:
                # preserve original indentation when commenting/uncommenting
                # capture leading whitespace and the rest of the line
                indent_match = re.match(r"^(\s*)(#\s*)?(.*)$", line)
                if indent_match:
                    indent = indent_match.group(1) or ""
                    rest = indent_match.group(3) or ""
                    if comment:
                        # if already commented (after indentation), leave as-is
                        if not rest.lstrip().startswith("#"):
                            line = f"{indent}# {rest.rstrip()}\n"
                        else:
                            line = f"{indent}{rest.rstrip()}\n"
                    else:
                        # uncomment: remove a leading '#' after indentation if present
                        # rest may start with '# ' or '#'
                        uncommented = re.sub(r"^#\s*", "", rest)
                        line = f"{indent}{uncommented.rstrip()}\n"
                else:
                    # fallback: simple strip as before
                    if comment:
                        if not line.strip().startswith("#"):
                            line = "# " + line
                    else:
                        line = line.lstrip("# ").rstrip() + "\n"
            new_lines.append(line)

        # Try to write back; if permission denied, log and return False
        with open(HAPROXY_CFG, "w") as f:
            f.writelines(new_lines)
        print(f"{'Commented' if comment else 'Uncommented'} {server_name}")
        return True
    except PermissionError:
        # In development environments the HAProxy config may be owned by root.
        # Don't raise an unhandled exception from the web UI; return False and
        # let the caller handle user-facing messaging.
        print(f"Permission denied when trying to modify {HAPROXY_CFG}")
        return False
    except FileNotFoundError:
        print(f"HAProxy config not found at {HAPROXY_CFG}")
        return False

def reload_haproxy():
    """Reload HAProxy safely."""
    try:
        subprocess.run(["sudo", "systemctl", "reload", "haproxy"], check=True)
        return True
    except Exception as e:
        # If reload fails (no sudo, not a systemd system, etc.) log and return False
        print(f"Failed to reload haproxy: {e}")
        return False
