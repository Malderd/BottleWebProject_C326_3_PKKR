function generateMatrix() {
    const n = parseInt(document.getElementById("sizeInput").value);
    const block = document.getElementById("table_and_buttons")
    const table = document.getElementById("matrixTable");

    table.innerHTML = ""; // очистка старой таблицы

    if (!n || n < 3 || n > 14) {
        alert("Введите число от 3 до 14");
        block.style.display = "none";
        return;
    }
    if (getComputedStyle(block).display === "none") block.style.display = "block";
    // заголовок
    const headerRow = document.createElement("tr");

    const emptyTh = document.createElement("th");
    headerRow.appendChild(emptyTh);

    for (let j = 0; j < n; j++) {
        const th = document.createElement("th");
        th.textContent = j;
        headerRow.appendChild(th);
    }

    table.appendChild(headerRow);

    // строки
    for (let i = 0; i < n; i++) {
        const row = document.createElement("tr");

        // заголовок строки
        const rowHeader = document.createElement("th");
        rowHeader.textContent = i;
        row.appendChild(rowHeader);

        for (let j = 0; j < n; j++) {
            const cell = document.createElement("td");

            if (i === j) {
                cell.textContent = "0";
                cell.classList.add("diagonal-cell");
            } else {
                const checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.name = `cell_${i}_${j}`;
                cell.appendChild(checkbox);
            }

            row.appendChild(cell);
        }

        table.appendChild(row);
    }
}