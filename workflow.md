
## **Simplified Approach**

## **The Workflow (Text-Based, No PNG Yet)**

```
1. User enters words (one per line in textarea)
2. Click "Generate"
3. Backend processes → returns formatted TEXT
4. Display on page:
   
   Level 1
   1. カタ ・ c a t
   2. ドッグ ・ d o g
   ...
   
5. User can:
   - Edit katakana (just click and type)
   - Regenerate (re-randomize spelling)
   - Download as .txt file
```

---

## **Why Text-Based is Better Than PNG (For Now)**

| Approach | Pros | Cons |
|---|---|---|
| **Text Display** (now) | Easy to edit, instant regenerate, simple to download | Looks basic |
| **PNG with text** (later) | Pretty printable worksheets | Hard to edit in browser, complex rendering |

Smart move: Get the logic working first, then make it pretty with a separate PNG tool.

---

## **What to Build (In Order)**

### **Step 1: Update Python Script**
Make it a function that returns text (not file-based):

```python
def generate_worksheet(words_list):
    """
    Input: list of words (each is just a string, not tab-separated)
    Output: formatted text string of the worksheet
    """
    # Process words
    # Organize into 5 levels
    # Return formatted text (not write to file)
    return formatted_output
```

### **Step 2: Create 3 Basic Pages (No Styling)**

**inputPage.html** — Just ask for words:
```html
<form id="inputForm">
    <label>Enter words (one per line):</label>
    <textarea id="wordInput" rows="15" cols="50"></textarea>
    <button type="button" onclick="submitWords()">Generate</button>
    <button type="button" onclick="location.href='welcomePage.html'">Back</button>
</form>
```

**resultsPage.html** — Show text + simple edit:
```html
<h1>Generated Worksheet</h1>
<pre id="worksheetDisplay"></pre>

<h2>Edit Katakana</h2>
<textarea id="editText" rows="15" cols="50"></textarea>
<button onclick="regenerate()">Update</button>
<button onclick="downloadText()">Download</button>
<button onclick="location.href='inputPage.html'">Back</button>
```

### **Step 3: Flask Route**
```python
@app.route('/api/generate', methods=['POST'])
def generate():
    words = request.json.get('words', '')
    word_list = words.split('\n')  # Split by line
    output = generate_worksheet(word_list)
    return jsonify({'output': output})
```

### **Step 4: JavaScript to Connect It**
```javascript
// inputHandler.js
function submitWords() {
    const words = document.getElementById('wordInput').value;
    
    fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({words: words})
    })
    .then(r => r.json())
    .then(data => {
        sessionStorage.setItem('worksheet', data.output);
        location.href = 'resultsPage.html';
    });
}

// resultsHandler.js
window.onload = function() {
    const worksheet = sessionStorage.getItem('worksheet');
    document.getElementById('worksheetDisplay').textContent = worksheet;
};

function downloadText() {
    const text = document.getElementById('editText').value || document.getElementById('worksheetDisplay').textContent;
    const blob = new Blob([text], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'worksheet.txt';
    a.click();
}
```

---

## **Key Points for Your Simple Version**

✅ **Do this:**
- Display as plain text in `<pre>` tags (preserves formatting)
- Let users edit the textarea directly
- Download as `.txt` file
- Skip CSS/styling for now

❌ **Skip for now:**
- PNG generation
- Complex editing UI
- Styling/layout

---

## **Questions to Confirm:**

1. **Words input format:** Just one word per line? (No tab-separated English phonetic + anything else?)
2. **Difficulty grouping:** Auto-assign first 4 as Level 1, etc? Or should user specify?
3. **Edit functionality:** Just a textarea where they can manually edit the text, then download? Or do they need a "per-word" editor?

Once you clarify these, you're ready to start building!

### ----------------------------------------------------------------------------------------

Perfect! Now I have the complete picture. Here's the exact structure and code you need to build:

---

## **The Three Pages You Need**

### **Page 1: Home (welcomePage.html)** — You have this
Just ensure the button links to inputPage.html

### **Page 2: Input (inputPage.html)** — New
5 separate text boxes, one for each level:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Sound Out Activity - Input Words</title>
</head>
<body>
    <h1>Enter English Words by Level</h1>
    <form id="inputForm">
        
        <h3>Level 1 (4 words)</h3>
        <textarea id="level1" rows="3" cols="40" placeholder="cat dog house bird"></textarea>
        
        <h3>Level 2 (4 words)</h3>
        <textarea id="level2" rows="3" cols="40" placeholder="elephant tiger monkey"></textarea>
        
        <h3>Level 3 (4 words)</h3>
        <textarea id="level3" rows="3" cols="40"></textarea>
        
        <h3>Level 4 (4 words)</h3>
        <textarea id="level4" rows="3" cols="40"></textarea>
        
        <h3>Level 5 (2 words)</h3>
        <textarea id="level5" rows="2" cols="40"></textarea>
        
        <br><br>
        <button type="button" onclick="submitWords()">Generate Worksheet</button>
        <button type="button" onclick="location.href='welcomePage.html'">Back</button>
    </form>

    <script src="/jsScripts/inputHandler.js"></script>
</body>
</html>
```

### **Page 3: Results (resultsPage.html)** — New
Display generated text + editing textarea:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Sound Out Activity - Results</title>
</head>
<body>
    <h1>Generated Worksheet</h1>
    
    <h2>Preview:</h2>
    <pre id="worksheetDisplay" style="border: 1px solid #ccc; padding: 10px; background: #f9f9f9;"></pre>
    
    <h2>Edit Katakana (if needed):</h2>
    <textarea id="editText" rows="20" cols="60"></textarea>
    
    <br><br>
    <button onclick="downloadText()">Download Text</button>
    <button onclick="regenerate()">Regenerate (re-randomize)</button>
    <button onclick="location.href='inputPage.html'">Back</button>

    <script src="/jsScripts/resultsHandler.js"></script>
</body>
</html>
```

---

## **Python Backend: Refactor Your Script**

Your soundOutTranslationScipt.py needs to become **function-based** instead of running directly. Here's what you need:

```python
# soundOutTranslationScipt.py (refactored)

from e2k import P2K
from g2p_en import G2p
import random

p2k = P2K()
g2p = G2p()

def randomSpelling(word):
    """Randomize spelling of a single word"""
    return ''.join(random.sample(word, len(word)))

def get_katakana(word):
    """Convert English word to katakana"""
    phonemes = g2p(word)
    katakana = p2k(phonemes)
    return katakana

def generate_worksheet(level_words_dict):
    """
    Input: Dictionary with keys "level1" through "level5"
           Each value is a list of English words
    
    Output: Formatted string ready for display
    """
    output = ""
    level_counter = 0
    
    for level in range(1, 6):
        level_key = f"level{level}"
        words = level_words_dict.get(level_key, [])
        
        if not words:
            continue
        
        output += f"Level {level} words:\n"
        level_counter = 0
        
        for word in words:
            level_counter += 1
            katakana = get_katakana(word)
            randomized = randomSpelling(word)
            randomized_spaced = " ".join(randomized)  # Space out letters
            output += f"{level_counter}. {katakana} ・ {randomized_spaced}\n"
        
        output += "\n"
    
    return output
```

---

## **Flask Backend (pyApp.py)**

Add this route:

```python
from flask import Flask, request, jsonify, render_template
from pyScripts.soundOutTranslationScipt import generate_worksheet

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("welcomePage.html")

@app.route("/inputPage.html")
def input_page():
    return render_template("inputPage.html")

@app.route("/resultsPage.html")
def results_page():
    return render_template("resultsPage.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    """Receive words from frontend, generate worksheet"""
    data = request.json
    
    # Organize into levels
    level_words_dict = {}
    for level in range(1, 6):
        level_key = f"level{level}"
        words_text = data.get(level_key, "")
        # Split by spaces or newlines, filter empty
        words = [w.strip().lower() for w in words_text.replace('\n', ' ').split() if w.strip()]
        level_words_dict[level_key] = words
    
    # Generate worksheet
    worksheet = generate_worksheet(level_words_dict)
    
    return jsonify({"output": worksheet})

if __name__ == "__main__":
    app.run(debug=True)
```

---

## **JavaScript: inputHandler.js**

```javascript
function submitWords() {
    // Get words from all 5 levels
    const data = {
        level1: document.getElementById('level1').value,
        level2: document.getElementById('level2').value,
        level3: document.getElementById('level3').value,
        level4: document.getElementById('level4').value,
        level5: document.getElementById('level5').value,
    };
    
    // Send to backend
    fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(result => {
        // Store the worksheet and go to results page
        sessionStorage.setItem('worksheet', result.output);
        location.href = 'resultsPage.html';
    })
    .catch(err => alert('Error: ' + err));
}
```

---

## **JavaScript: resultsHandler.js**

```javascript
window.onload = function() {
    // Load the generated worksheet
    const worksheet = sessionStorage.getItem('worksheet');
    document.getElementById('worksheetDisplay').textContent = worksheet;
    document.getElementById('editText').value = worksheet;
};

function downloadText() {
    // User can download the edited version
    const text = document.getElementById('editText').value;
    const blob = new Blob([text], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'sound-out-worksheet.txt';
    a.click();
    URL.revokeObjectURL(url);
}

function regenerate() {
    // Clear and reload original
    const worksheet = sessionStorage.getItem('worksheet');
    document.getElementById('editText').value = worksheet;
}
```

---

## **Folder Structure**

```
html/
  welcomePage.html
  inputPage.html      (NEW)
  resultsPage.html    (NEW)
jsScripts/
  inputHandler.js     (NEW)
  resultsHandler.js   (NEW)
pyScripts/
  soundOutTranslationScript.py (REFACTOR - convert to functions)
  pyApp.py (UPDATE - add routes)
```

---

## **Next Steps**

1. Update soundOutTranslationScript.py to use the function structure
2. Create the 3 HTML pages
3. Create the 2 JavaScript files
4. Update pyApp.py with the new routes
5. Test locally: `python pyApp.py` → Visit `http://localhost:5000`

Does this match what you're envisioning?

### --------------------------------------------------------------------------------------------------------------------------------------------------------

## 🎉 Excellent progress — full file set ready ✅

You asked for “all files in one response.”  
Below is the complete minimal working copy for your local web app.

---

## 1) soundOutTranslationScipt.py (refactor)

```python
# pyScripts/soundOutTranslationScipt.py
from e2k import P2K
from g2p_en import G2p
import random

p2k = P2K()
g2p = G2p()

def random_spelling(word: str) -> str:
    if len(word) <= 1:
        return word
    return ''.join(random.sample(word, len(word)))

def get_katakana(word: str) -> str:
    phonemes = g2p(word)
    return p2k(phonemes)

def generate_worksheet(level_words: dict) -> str:
    output_lines = []
    for level in range(1, 6):
        key = f"level{level}"
        words = level_words.get(key, [])
        if not words:
            continue
        output_lines.append(f"Level {level} words:")
        for idx, w in enumerate(words, start=1):
            w_clean = w.strip()
            if not w_clean:
                continue
            kana = get_katakana(w_clean)
            scrambled = random_spelling(w_clean)
            scrambled_spaced = " ".join(scrambled)
            output_lines.append(f"{idx}. {kana} ・ {scrambled_spaced}")
        output_lines.append("")  # blank line
    return "\n".join(output_lines).strip()

if __name__ == "__main__":
    # quick manual test
    sample = {
        "level1": ["cat", "dog", "fish", "book"],
        "level2": ["train", "plane", "ship", "house"],
        "level3": ["apple", "banana", "orange", "grape"],
        "level4": ["teacher", "friend", "window", "pencil"],
        "level5": ["jungle", "monster"]
    }
    print(generate_worksheet(sample))
```

---

## 2) pyApp.py (Flask routes)

```python
# pyScripts/pyApp.py
from flask import Flask, request, jsonify, render_template
from pyScripts.soundOutTranslationScipt import generate_worksheet

app = Flask(__name__, template_folder="../html", static_folder="../")

@app.route("/")
def home():
    return render_template("welcomePage.html")

@app.route("/inputPage.html")
def input_page():
    return render_template("inputPage.html")

@app.route("/resultsPage.html")
def results_page():
    return render_template("resultsPage.html")

@app.route("/api/generate", methods=["POST"])
def api_generate():
    payload = request.json or {}
    level_words = {}

    for level in range(1, 6):
        key = f"level{level}"
        raw = payload.get(key, "")
        words = [w.strip() for w in raw.replace("\n", " ").split() if w.strip()]
        level_words[key] = words

    worksheet_text = generate_worksheet(level_words)
    return jsonify({"output": worksheet_text})

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 3) welcomePage.html

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Sound Out Activity Maker - Home</title>
</head>
<body>
  <h1>Sound Out Activity Maker</h1>
  <p>Choose an activity:</p>

  <button onclick="location.href='inputPage.html'">Sound Out Activity</button>
  <button disabled>Sentence Mix (Coming Soon)</button>
</body>
</html>
```

---

## 4) `html/inputPage.html`

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Sound Out Input</title>
</head>
<body>
  <h1>Enter English Words by Level</h1>

  <div>
    <h4>Level 1 (up to 4 words)</h4>
    <textarea id="level1" rows="2" cols="50" placeholder="cat dog fish book"></textarea>
  </div>
  <div>
    <h4>Level 2 (up to 4 words)</h4>
    <textarea id="level2" rows="2" cols="50" placeholder="train plane ship house"></textarea>
  </div>
  <div>
    <h4>Level 3 (up to 4 words)</h4>
    <textarea id="level3" rows="2" cols="50"></textarea>
  </div>
  <div>
    <h4>Level 4 (up to 4 words)</h4>
    <textarea id="level4" rows="2" cols="50"></textarea>
  </div>
  <div>
    <h4>Level 5 (up to 2 words)</h4>
    <textarea id="level5" rows="1" cols="50"></textarea>
  </div>

  <button type="button" onclick="submitWords()">Generate Worksheet</button>
  <button type="button" onclick="location.href='welcomePage.html'">Back</button>

  <script src="/jsScripts/inputHandler.js"></script>
</body>
</html>
```

---

## 5) `html/resultsPage.html`

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Sound Out Results</title>
</head>
<body>
  <h1>Generated Worksheet</h1>
  <pre id="worksheetDisplay" style="border:1px solid #ccc; padding:10px; background:#fafafa;"></pre>

  <h2>Edit Text</h2>
  <textarea id="editText" rows="20" cols="80"></textarea>

  <br><br>
  <button onclick="downloadText()">Download .txt</button>
  <button onclick="regenerate()">Reset (original output)</button>
  <button onclick="location.href='inputPage.html'">Back</button>

  <script src="/jsScripts/resultsHandler.js"></script>
</body>
</html>
```

---

## 6) `jsScripts/inputHandler.js`

```javascript
// jsScripts/inputHandler.js
function submitWords() {
    const payload = {
        level1: document.getElementById("level1").value,
        level2: document.getElementById("level2").value,
        level3: document.getElementById("level3").value,
        level4: document.getElementById("level4").value,
        level5: document.getElementById("level5").value,
    };

    fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    })
    .then((res) => res.json())
    .then((data) => {
        sessionStorage.setItem("worksheet", data.output || "");
        location.href = "resultsPage.html";
    })
    .catch((err) => alert("Error generating worksheet: " + err));
}
```

---

## 7) `jsScripts/resultsHandler.js`

```javascript
// jsScripts/resultsHandler.js
window.addEventListener("DOMContentLoaded", () => {
    const worksheet = sessionStorage.getItem("worksheet") || "";
    document.getElementById("worksheetDisplay").textContent = worksheet;
    document.getElementById("editText").value = worksheet;
});

function downloadText() {
    const text = document.getElementById("editText").value || "";
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "sound_out_worksheet.txt";
    anchor.click();
    URL.revokeObjectURL(url);
}

function regenerate() {
    const worksheet = sessionStorage.getItem("worksheet") || "";
    document.getElementById("worksheetDisplay").textContent = worksheet;
    document.getElementById("editText").value = worksheet;
}
```

---

## 8) `requirements.txt`

```
Flask>=2.0
e2k
g2p-en
```

---

## ✅ How to run locally tomorrow

1. Open command prompt in project root.
2. `python -m venv venv`
3. `.\venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `python pyScripts/pyApp.py`
6. Browser: `http://localhost:5000`
7. Use home → input → generate → edit → download

---

## 📝 Optional: workflow note file

workflow.md can include:
- “Build this UI”
- “Refactor function in script”
- “Hook `/api/generate`”
- “Test end-to-end”
- “Next: rasterize to PNG”

---

## 🚀 You’re set

This is full, copy/paste-ready.  
Next time, open your project, paste these files, and run.  
Ask again if you want “PNG generation script that uses Pillow after edit” as the next enhancement.

### -----------------------------------------------------

## 🎉 Great news: you can do this with a small UI addition and static serving

Fantastic progress: your `userInput.html` is already set up nicely and we can safely add radio buttons + preview images from png.  
Next step: show chosen design thumbnail from the png folder before submission.

---

## 1) Add the design selector HTML (radio + preview area)

In userInput.html, add this block before "Generate Worksheet":

```html
<h3>Select worksheet style:</h3>
<div>
  <label>
    <input type="radio" name="design" value="style1" checked
      onchange="setDesignPreview('style1.png')">
    Style 1
  </label>
  <label>
    <input type="radio" name="design" value="style2"
      onchange="setDesignPreview('style2.png')">
    Style 2
  </label>
  <label>
    <input type="radio" name="design" value="style3"
      onchange="setDesignPreview('style3.png')">
    Style 3
  </label>
</div>

<div id="designPreviewWrapper" style="margin: 10px 0;">
  <p>Preview:</p>
  <img id="designPreview" src="/png/style1.png" alt="Sheet style preview"
       style="max-width: 400px; border:1px solid #ccc;">
</div>
```

- Change `"style1.png"`/`style2.png`/`style3.png` to actual file names in your png folder.
- `src="/png/...` assumes your server serves static files from root and your PNGs are directly available as `/png/filename.png`.

---

## 2) Add JS helper function in `inputHandler.js`

At top (or bottom) of inputHandler.js:

```javascript
function setDesignPreview(imageName) {
    const img = document.getElementById("designPreview");
    img.src = `/png/${imageName}`;
}
```

This updates the preview image when a radio button is selected.

---

## 3) Include selected design in the payload POST

In `submitWords()` (inputHandler.js) add:

```javascript
const design = document.querySelector('input[name="design"]:checked').value;

const payload = {
    level1: ...,
    ...,
    level5: ...,
    design: design
};
```

Then in Flask route (`/api/generate`) you'll get `data["design"]` for later use (e.g., render PNG from selected template or just track style).

---

## 4) Back-end static files config (Flask)

Make sure Flask can serve png:

- Either using `static_folder` in app creation:

```python
app = Flask(__name__, template_folder="../html", static_folder="../")
```

Then `/png/your.png` works (since your root has png).

- OR explicit route (if needed):

```python
from flask import send_from_directory

@app.route("/png/<path:filename>")
def png(filename):
    return send_from_directory("png", filename)
```

---

## 5) Option: display selected design in `resultsPage.html`

If you want the output screen to show the chosen base style:

- Add a placeholder:

```html
<h3>Selected Style</h3>
<img id="selectedStyle" style="max-width:300px; border:1px solid #ccc;">
```

- Populate in `resultsHandler.js`:

```javascript
const selectedStyle = sessionStorage.getItem("sheetDesign");
if (selectedStyle) {
    document.getElementById("selectedStyle").src = `/png/${selectedStyle}`;
}
```

And in `inputHandler.js` after `/api/generate`:

```javascript
sessionStorage.setItem("sheetDesign", design);
```

---

## ✅ Summary

- Add radio inputs and preview image in `userInput.html`
- Add `setDesignPreview()` in `inputHandler.js`
- Send `design` with payload to Flask
- Ensure Flask static PNG route works
- (optional) show style on results page

You’re set for UI and flow. If you want, I can next show how to generate a PNG “worksheet page” from the text+style using Pillow (Python) after edit.



## ------------------------------------------------------------------------------------
### 3/30/2026 
- got mostly working really roughly only locally, can go from home page, to enter info, to display simple text results. Results buttons are mostly not functional
    - want to (for now) set up the edit button to work to edit the output text, add button to generate PNG (need to figure out png pasting)
    add back to entering text, move the picture selection to the text results page - add another result page to display generated PNG. 
    ## ASAP ADDS
    - Result page: buttons for going back to enter text and edit results
    - Input page: make it a limit so the user can ONLY enter 4 words (levels1-4) and 2 words(level5)

    use seperate fonts for ENglish and Japanese

    make so user can paste in a list of words already made and it will enter in sections of 4 per text box
    
    want to use https://www.kfstudio.net/font/kfhimaji/ font, but awaiting permission