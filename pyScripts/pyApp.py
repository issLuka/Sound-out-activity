import os, sys
#adds scripts to path for import to soundout scipt - MUST be before other imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import soundOutTranslationScript, addToPNGScript
from flask import Flask, request, jsonify, send_from_directory, send_file
import logging

app_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(app_dir)

app = Flask(__name__, static_folder=os.path.join(project_root), static_url_path="")

logger = logging.getLogger("soundOutApp")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler (file_handler)
def processEdited(editedWords):
    processed = {
        "level1":{
            "kana":[],
            "randomizedWords":[]},
        "level2":{
            "kana":[],
            "randomizedWords":[]},
        "level3":{
            "kana":[],
            "randomizedWords":[]},
        "level4":{
            "kana":[],
            "randomizedWords":[]},
        "level5":{
            "kana":[],
            "randomizedWords":[]}
        }
    
    lines  = editedWords.strip().split("\n")
    currentLevel = None

    for line in lines:
        line = line.strip()

        if line.startswith("Level"):
            if "1" in line:
                currentLevel = "level1"
            elif "2" in line:
                currentLevel = "level2"
            elif "3" in line:
                currentLevel = "level3"
            elif "4" in line:
                currentLevel = "level4"
            elif "5" in line:
                currentLevel = "level5"
            continue

        if not line:
            continue

        if " - " in line and currentLevel:
            kana, word = line.split(" - ", 1)
            processed[currentLevel]["kana"].append(kana.strip())
            processed[currentLevel]["randomizedWords"].append(word.strip())
    #print(processed)
    return processed

@app.route("/")
def home():
    return send_from_directory(project_root, "./frontend/welcomePage.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data   = request.get_json(silent=True) or {}
        result = soundOutTranslationScript.processWordsWithLevels(data)
        text   = soundOutTranslationScript.formatTextOutput(result)
        return jsonify({"status": "success", "output": text, "processed": result})
    except Exception as e:
        logger.error(f"/submit failed for data: {data} | Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/generatePNG", methods=["POST"]) #TO FINISH: come back when figure out logic for drawing text
def design():
    try:
        data = request.get_json(silent = True) or {}
        designChoice = data.get("design")
        processed = data.get("processed")
        editedText = data.get("editedWorksheet")
        print(editedText)
        if not designChoice or not processed:
            return jsonify({"status": "error", "message": "Missing design or processed data"}), 400

        if editedText:
            processed = processEdited(editedText)
            imageGen = addToPNGScript.imageGeneration(designChoice, processed)   
            print(processed)
        imageGen = addToPNGScript.imageGeneration(designChoice, processed) 


        return send_file(
            imageGen,
            mimetype = "image/png",
            as_attachment=False,
            download_name = "soundout_activity.png"
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host = "127.0.0.1", port = 5000)