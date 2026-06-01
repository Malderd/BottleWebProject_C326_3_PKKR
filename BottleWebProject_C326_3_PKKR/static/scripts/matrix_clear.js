function clearMatrix() {
    const table = document.getElementById("matrixTable");
    const rows = table.rows;

    const n = rows.length - 1;
    for (let i = 1; i <= n; i++) {
        for (let j = 1; j <= n; j++) {
            const cb = rows[i].cells[j].querySelector("input[type='checkbox']");
            if (cb) cb.checked = false;
        }
    }
}