//handles all fetch between front end

// called from userInput
function submitWords() {

    const payload = {
        level1: document.getElementById("level1").value,
        level2: document.getElementById("level2").value,
        level3: document.getElementById("level3").value,
        level4: document.getElementById("level4").value,
        level5: document.getElementById("level5").value,
    };


    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(payload)
    })
    .then((res) => res.json())
    .then((data) => {
        if (data.status !== "success") {
            alert("Error: " + data.message);
            return;
        }
        sessionStorage.setItem("worksheet", data.output || "");
        sessionStorage.setItem("processed", JSON.stringify(data.processed));
        location.href = "/frontend/resultsPage.html";
    })
    .catch((err) => alert("Error generating worksheet: " + err));
}

//called from resultsPage
function generatePNG() {
    const design = document.querySelector("input[name='design']:checked")?.value;
    const processed = JSON.parse(sessionStorage.getItem("processed") || "null");
    const editedWorksheet = hasEdits ? document.getElementById("worksheetContent").textContent : null;

    console.log("DEBUG: hasEdits =", hasEdits);
    console.log("DEBUG: editedWorksheet =", editedWorksheet);

    if (!design){
        alert("Please select a design.");
        return;
    }
    if (!processed){
        alert("No worksheet data found. Please go back and generate a worksheet");
        return;
    }

    const button = document.getElementById("generateBtn");
    if (button){
        button.textContent = "Generating..."; button.disabled = true;
    }

    fetch("/generatePNG", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ design, processed, editedWorksheet }),
    })
    .then((res) => {
        if (!res.ok) return res.json().then(d => Promise.reject(d.message));
        return res.blob();
    })
    .then((blob) => {
        const url = URL.createObjectURL(blob);
        sessionStorage.setItem("pngBlobURL", url);
        location.href = "/frontend/pngDisplay.html";
    })
    .catch((err) => {
        alert("Error generating PNG: " + err);
        if (button) {
            button.textContent = "Generate PNG";
            button.disabled = false;
        }
    });
}