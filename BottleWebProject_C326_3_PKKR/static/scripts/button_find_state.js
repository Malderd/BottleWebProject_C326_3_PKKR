document.addEventListener("DOMContentLoaded", function () {

    const findButton = document.getElementById("findComponentsButton");

    function updateFindButtonState() {

        const checkboxes = document.querySelectorAll(
            "#matrixTable input[type='checkbox']"
        );

        let hasChecked = false;

        for (const checkbox of checkboxes) {
            if (checkbox.checked) {
                hasChecked = true;
                break;
            }
        }

        if (hasChecked) {
            findButton.classList.remove("primary");
            findButton.classList.add("other");
        } else {
            findButton.classList.remove("other");
            findButton.classList.add("primary");
        }
    }

    window.updateFindButtonState = updateFindButtonState;

    document.addEventListener("change", function (event) {
        if (event.target.matches("#matrixTable input[type='checkbox']")) {
            updateFindButtonState();
        }
    });

    updateFindButtonState();
});