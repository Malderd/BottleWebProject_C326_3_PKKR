function generateRandomGraph() {
    const table = document.getElementById("matrixTable");
    const rows = table.rows;

    const n = rows.length - 1;

    // 1. очистка
    for (let i = 1; i <= n; i++) {
        for (let j = 1; j <= n; j++) {
            const cb = rows[i].cells[j].querySelector("input[type='checkbox']");
            if (cb) cb.checked = false;
        }
    }

    // 2. случайная генерация (антисимметрия сохраняется)
    for (let i = 1; i <= n; i++) {
        for (let j = 1; j <= n; j++) {
            if (i === j) continue;

            const cb_ij = rows[i].cells[j].querySelector("input[type='checkbox']");
            const cb_ji = rows[j].cells[i].querySelector("input[type='checkbox']");

            if (!cb_ij || !cb_ji) continue;

            if (!cb_ij.checked && !cb_ji.checked) {
                if (Math.random() < (0.25 + Math.sin((i + j) * 12.9898) * 0.05 + 0.05)) {
                    cb_ij.checked = true;
                }
            }
        }
    }

    // 3. гарантия: нет изолированных вершин
    for (let i = 1; i <= n; i++) {

        let hasEdge = false;

        for (let j = 1; j <= n; j++) {
            const cb1 = rows[i].cells[j].querySelector("input[type='checkbox']");
            const cb2 = rows[j].cells[i].querySelector("input[type='checkbox']");

            if ((cb1 && cb1.checked) || (cb2 && cb2.checked)) {
                hasEdge = true;
                break;
            }
        }

        // если вершина изолирована — добавляем случайное ребро
        if (!hasEdge) {
            let j;
            do {
                j = Math.floor(Math.random() * n) + 1;
            } while (j === i);

            const cb = rows[i].cells[j].querySelector("input[type='checkbox']");
            if (cb) cb.checked = true;
        }
        updateFindButtonState();
    }
}