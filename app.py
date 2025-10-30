from flask import Flask, render_template, request, redirect, url_for, flash
from haproxy_manager.config import BACKENDS
from haproxy_manager.haproxy import toggle_server, reload_haproxy

app = Flask(__name__)
# Secret key for session (flash). Replace with a secure value in production.
app.secret_key = "dev-secret"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        server = request.form["server"]
        action = request.form["action"]
        # toggle_server returns True on success, False on failure (permission, missing file)
        ok = toggle_server(server, comment=(action == "disable"))
        if ok:
            flash(f"Successfully {'disabled' if action == 'disable' else 'enabled'} {server}")
        else:
            flash(f"Failed to {'disable' if action == 'disable' else 'enable'} {server} — check permissions or config path", "error")
        # We DO NOT reload HAProxy automatically here. Reload is a separate action/button.
        return redirect(url_for("index"))

    # Render the main UI page. Keep route logic thin and delegate HAProxy operations to `haproxy_manager`.
    return render_template("index.html", backends=BACKENDS)


@app.route("/reload", methods=["POST"])
def reload():
    """Trigger HAProxy reload. Currently attempts to run reload_haproxy and
    reports success/failure. In many environments this requires sudo and will
    fail unless configured. We keep reload separate from edits so it can be
    controlled independently.
    """
    ok = reload_haproxy()
    if ok:
        flash("HAProxy reload requested successfully")
    else:
        flash("HAProxy reload failed or requires elevated permissions", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
