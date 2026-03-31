//handles the design choice to pass into addToPNG

function getSelectedDesign() {
    return document.querySelector('input[name="design"]:checked').value;
}