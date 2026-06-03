document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("sizeInput");
    const button = document.getElementById("createMatrixButton");

    function updateButtonState() {

        if (input.value.trim() === "") {
            button.classList.remove("other");
            button.classList.add("primary");
        }
        else {
            button.classList.remove("primary");
            button.classList.add("other");
        }
    }

    input.addEventListener("input", updateButtonState);

    updateButtonState();
});