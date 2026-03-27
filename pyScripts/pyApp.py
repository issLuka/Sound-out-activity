from flask import Flask, request, jsonify, render_template
import os
import sys

#add scripts to path for import to soundout scipt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(app_dir)

app = Flask(__name__)

@app.route("/")
def home():
    return app.send_static_file("html/userInput.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json.get("text", "")

    # Save to file
    with open("txtFiles/SoundOutInput.txt", "w", encoding="utf-8") as f:
        f.write(data)

    # Run your existing script (optional)
    #subprocess.run(["python", "script.py"])

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)