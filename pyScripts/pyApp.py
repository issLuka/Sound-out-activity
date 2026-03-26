from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json.get("text", "")

    # Save to file
    with open("txtFiles/SoundOutInput.txt", "w", encoding="utf-8") as f:
        f.write(data)

    # Run your existing script (optional)
    subprocess.run(["python", "script.py"])

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)