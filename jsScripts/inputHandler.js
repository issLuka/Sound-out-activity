//handles input from userInput
function setDesignPreview(imageName) {
    const img = document.getElementById("designPreview");
    img.src = `/png/${imageName}`;
}
function submitWords() {
    const design = document.querySelector('input[name="design"]:checked').value;

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