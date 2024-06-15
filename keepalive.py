from flask import Flask
from celery import Celery
from threading import Thread
# Configure Celery (can be done outside the function)
app = Celery('tasks', broker='redis://localhost:6379')  # Replace with your Redis server address

# Flask app (can be defined outside the function)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return f"<h1>I'm Awake Already!</h1>"


@app.task
def background_task():
    # Your background task code here
    # This can be anything you want to run in the background,
    # like sending emails, processing data, etc.
    print("Background task running!")
    # ... your task logic ...


def start_worker():
    background_task.delay()  # Schedule the background task to run


def start_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


# Call these functions from your keep_alive() function or elsewhere
def keep_alive():
    # Start the background worker in a separate thread
    thread = Thread(target=start_worker)
    thread.start()

    # Start the Flask app in the main thread
    start_flask()

# Example usage (assuming keep_alive() is defined elsewhere)
# keep_alive()  # Call this function to start the app and worker
