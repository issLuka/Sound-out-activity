//handles input from userInput

function submitWords() {
    const design = document.querySelector('input[name="design"]:checked').value;

    const payload = {
        level1: document.getElementById("level1").value,
        level2: document.getElementById("level2").value,
        level3: document.getElementById("level3").value,
        level4: document.getElementById("level4").value,
        level5: document.getElementById("level5").value,
    };

    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json"     
        },
        body: JSON.stringify(payload),
    })
    .then((res) => res.json())
    .then((data) => {
        sessionStorage.setItem("worksheet", data.output || "");
        location.href = "/frontend/resultsPage.html";
    })
    .catch((err) => alert("Error generating worksheet: " + err));
}