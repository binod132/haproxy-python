# HAProxy Backend Manager

A simple web-based UI to enable and disable backend servers in an HAProxy configuration file. This tool dynamically reads your `haproxy.cfg` file, allowing you to manage server states without manual edits.

## Workflow

1.  **View Server Status:** The main page displays all backends and their servers discovered from your HAProxy configuration. Each server is shown with its current status ("enabled" or "disabled") in a colored box.
2.  **Change Server State:**
    *   Click **Disable** to comment out an active server in the `haproxy.cfg` file.
    *   Click **Enable** to uncomment a disabled server.
3.  **Apply Changes:** After you make a change, the **Reload HAProxy** button will pulse green, indicating that a reload is required to apply your changes. Clicking this button will execute the `sudo systemctl reload haproxy` command.

## How to Run the Application

### 1. Prerequisites

*   Python 3 and `pip`
*   A running HAProxy instance
*   `sudo` access

### 2. Installation

Clone the repository and create a virtual environment:

```bash
git clone <repository-url>
cd haproxy-manager
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Sudoers Configuration

This application requires permission to modify the `/etc/haproxy/haproxy.cfg` file and to reload the HAProxy service. You must configure passwordless `sudo` for the user that will run the application.

**Create a new sudoers file:**

```bash
sudo visudo -f /etc/sudoers.d/haproxy-manager
```

**Add the following line.** Replace `your-user` with the username of the user that will run the web application (e.g., `www-data` or your own username).

```
your-user ALL=(ALL) NOPASSWD: /bin/cp /tmp/* /etc/haproxy/haproxy.cfg, /bin/systemctl reload haproxy
```

Save and exit the editor. This configuration is secure as it only allows the specified user to run these two exact commands without a password.

### 4. Running the App

To start the Flask development server:

```bash
source .venv/bin/activate
python app.py
```

The application will be available at `http://0.0.0.0:5000`.
