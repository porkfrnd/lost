from flask import Flask
from threading import Thread
import os


app = Flask('')


@app.route('/')

def home():

    return f"<h1>😎I'm Awake Already!🔥</h1>"

def run():

 app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))



def keep_alive():  

    t = Thread(target=run)

    t.start()
