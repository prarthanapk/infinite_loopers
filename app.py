# app.py
from flask import Flask, render_template, jsonify
import subprocess
import os
import sys
import random
import useless_math  # <-- Import our file

app = Flask(__name__)
WINDOWS = os.name == 'nt'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/wave")
def wave():
    gesture_script = os.path.join(os.getcwd(), "gesture_control.py")
    if WINDOWS:
        subprocess.Popen([sys.executable, gesture_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen([sys.executable, gesture_script])
    return render_template("running.html", title="Gesture Control Running", emoji="🖐", message="Gesture Control Running...")

@app.route("/type_scream")
def type_scream():
    script = os.path.join(os.getcwd(), "scream_to_type.py")
    if WINDOWS:
        subprocess.Popen([sys.executable, script], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen([sys.executable, script])
    return render_template("running.html", title="Scream-to-Type Running", emoji="🎤", message="Scream detection started...")

@app.route("/useless_math")
def useless_math_page():
    return render_template("useless_math.html")

# ✅ API endpoint for JS fetch
@app.route("/api/useless-math")
def api_useless_math():
    calculation = useless_math.generate_useless_calculation()
    facts = useless_math.get_useless_facts()
    stats = {
        "problems_solved": random.randint(1, 999),
        "bananas_divided": random.randint(1, 500),
        "teachers_crying": random.randint(0, 10)
    }
    return jsonify({
        "calculation": calculation,
        "facts": facts,
        "stats": stats
    })

# Compliments
compliments = [
    "You are absolutely amazing! 💖",
    "Your smile can light up a whole room! 😊",
    "You have an incredible mind! 🧠",
    "You are stronger than you think! 💪",
    "You make the world a better place! 🌍",
    "Your kindness is contagious! 🌸",
    "You are a masterpiece! 🎨",
    "You inspire everyone around you! ✨",
    "You are loved more than you know! ❤️",
    "You have a heart of gold! 🏅"
]

@app.route("/self_love")
def self_love_page():
    return render_template("compliment.html", compliments=compliments)

@app.route("/api/get_compliment")
def api_get_compliment():
    return jsonify({"compliment": random.choice(compliments)})

if __name__ == "__main__":
    app.run(debug=True)
