from flask import Flask, render_template, request, redirect, url_for, flash, session
from haproxy_manager.haproxy import toggle_server, reload_haproxy, parse_config

app = Flask(__name__)
# Secret key for session (flash). Replace with a secure value in production.
app.secret_key = "dev-secret"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        server = request.form["server"]
        action = request.form["action"]
        ok = toggle_server(server, comment=(action == "disable"))
        if ok:
            flash(f"Successfully {'disabled' if action == 'disable' else 'enabled'} {server}. Reload required.")
            session['reload_needed'] = True
        else:
            flash(f"Failed to {'disable' if action == 'disable' else 'enable'} {server} — check permissions or config path", "error")
        return redirect(url_for("index"))

    backends = parse_config()
    return render_template("index.html", backends=backends, reload_needed=session.get('reload_needed', False))


@app.route("/reload", methods=["POST"])
def reload():
    """Trigger HAProxy reload and clear the 'reload_needed' flag."""
    ok = reload_haproxy()
    if ok:
        flash("HAProxy reloaded successfully.")
        session['reload_needed'] = False
    else:
        flash("HAProxy reload failed or requires elevated permissions.", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
