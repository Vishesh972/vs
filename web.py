from flask import Flask


# ── Flask setup ───────────────────────────────
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Bot is running ✅"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)


"""
FOR HOSTING ON RENDER/KOYEB:
1. Create web.py and paste the above code in it.
2. Add below imports to your main file.
    ```py
    import threading
    from web import run_flask
    ```
3. Paste below code where your app/bot starts:
    ```py
        # Start Flask in a background thread
        threading.Thread(target=run_flask, daemon=True).start()
        print("Flask server started on port 8000")
    ```

"""