import soundOutTranslationScript
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import sys

#add scripts to path for import to soundout scipt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(app_dir)

app = Flask(__name__, static_folder=os.path.join(project_root), static_url_path="")

@app.route("/")
def home():
    return send_from_directory(project_root, "./frontend/welcomePage.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json(silent=True) or {}
        result = soundOutTranslationScript.processWordsWithLevels(data) #process the words with levels and get the kana and randomized words
        text = soundOutTranslationScript.formatTextOutput(result) #format the text output
        return jsonify({"status": "success", "output": text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)