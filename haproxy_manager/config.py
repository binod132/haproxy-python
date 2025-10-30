"""Configuration defaults for haproxy-python.

Keep simple defaults here so the scaffold can be run and tested without
access to a real HAProxy instance. Tests and production code should
override these values.
"""


# Default HAProxy socket (used by runtime-control helpers if implemented)
HAPROXY_SOCKET = '/var/run/haproxy.sock'

# For development and tests prefer a project-local config so we don't
# accidentally modify the system HAProxy config. Production code can
# override this constant or set it to the system path.
# For safe local testing we use a project-local copy of the system
# HAProxy config so the web UI can exercise edits without needing sudo.
# For local testing use a writable copy so the web UI can modify it without sudo.
# Production default would be "/etc/haproxy/haproxy.cfg" but we point to a test
# copy here so enable/disable flows can be exercised during development.
HAPROXY_CFG = "/etc/haproxy/haproxy.cfg"
