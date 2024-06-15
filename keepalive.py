from flask import Flask
from threading import Thread

# Flask app (can be defined outside the function)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return f"<h1>I'm Awake Already!</h1>"



def start_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


# Call these functions from your keep_alive() function or elsewhere
def keep_alive():
    # Start the background worker in a separate thread
    thread = Thread(target=start_flask)
    thread.start()

# Example usage (assuming keep_alive() is defined elsewhere)
# keep_alive()  # Call this function to start the app and worker
