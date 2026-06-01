document.addEventListener("DOMContentLoaded", function () {
    let lastData = null; // Переменная для хранения ответов бэкенда

    // Вспомогательная функция для определения, какой таб сейчас активен
    function getActiveTableId() {
        const activeTab = document.querySelector(".tab.active");
        if (!activeTab) return "matrix-table-manual";
        const tabType = activeTab.getAttribute("data-tab"); // manual, random, file
        return `matrix-table-${tabType}`;
    }

    function getActiveWrapperId() {
        const activeTab = document.querySelector(".tab.active");
        if (!activeTab) return "wrapper-manual";
        const tabType = activeTab.getAttribute("data-tab");
        return `wrapper-${tabType}`;
    }

    // ==========================================
    // 1. ПЕРЕКЛЮЧЕНИЕ ОСНОВНЫХ ТАБОВ (ВВОД ДАННЫХ)
    // ==========================================
    document.querySelectorAll(".tab").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            document.querySelectorAll(".tab-content").forEach(t => t.style.display = "none");
            const targetId = "tab-" + btn.getAttribute("data-tab");
            const targetContent = document.getElementById(targetId);
            if (targetContent) targetContent.style.display = "block";
        });
    });

    // ==========================================
    // 2. РУЧНОЙ ВВОД МАТРИЦЫ
    // ==========================================
    const btnCreateMatrix = document.getElementById("btn-create-matrix");
    if (btnCreateMatrix) {
        btnCreateMatrix.addEventListener("click", () => {
            const nInput = document.getElementById("n-manual");
            const n = parseInt(nInput ? nInput.value : 0);
            if (!n || n < 2 || n > 20) {
                alert("Введите N от 2 до 20");
                return;
            }
            const matrix = Array.from({ length: n }, () => Array(n).fill(0));

            // Показываем обертку и строим таблицу
            document.getElementById("wrapper-manual").style.display = "block";
            buildMatrixFromData(matrix, "matrix-table-manual");
        });
    }

    const btnClearMatrix = document.getElementById("btn-clear-matrix");
    if (btnClearMatrix) {
        btnClearMatrix.addEventListener("click", () => {
            const table = document.getElementById("matrix-table-manual");
            if (table) table.innerHTML = "";

            // Скрываем контейнер таблицы
            document.getElementById("wrapper-manual").style.display = "none";
            hideResultPanel();
        });
    }

    // ==========================================
    // 3. СЛУЧАЙНАЯ ГЕНЕРАЦИЯ
    // ==========================================
    const btnRandom = document.getElementById("btn-random");
    if (btnRandom) {
        btnRandom.addEventListener("click", async () => {
            const nEl = document.getElementById("n-random");
            const dEl = document.getElementById("density");
            if (!nEl || !dEl || !nEl.value || !dEl.value) {
                alert("Введите количество вершин и плотность");
                return;
            }

            try {
                const response = await fetch("/euler/random", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ n: nEl.value, density: dEl.value })
                });
                const data = await response.json();
                if (data.error) { alert(data.error); return; }

                // Показываем обертку и генерируем таблицу
                document.getElementById("wrapper-random").style.display = "block";
                buildMatrixFromData(data.matrix, "matrix-table-random");
            } catch (err) {
                console.error("Ошибка генерации:", err);
            }
        });
    }

    // ==========================================
    // 4. ЗАГРУЗКА ИЗ ФАЙЛА (CLICK & DRAG-AND-DROP)
    // ==========================================
    const fileInput = document.getElementById("file-input");
    const fileZone = document.getElementById("file-zone");
    const btnChooseFile = document.getElementById("btn-choose-file");
    const btnClearFile = document.getElementById("btn-clear-file");

    if (btnChooseFile && fileInput) {
        btnChooseFile.addEventListener("click", () => fileInput.click());
    }
    if (fileZone && fileInput) {
        fileZone.addEventListener("click", () => fileInput.click());
        fileZone.addEventListener("dragover", (e) => { e.preventDefault(); fileZone.classList.add("dragover"); });
        fileZone.addEventListener("dragleave", () => fileZone.classList.remove("dragover"));
        fileZone.addEventListener("drop", async (e) => {
            e.preventDefault();
            fileZone.classList.remove("dragover");
            if (e.dataTransfer.files.length) await uploadFile(e.dataTransfer.files[0]);
        });
    }
    if (fileInput) {
        fileInput.addEventListener("change", async (e) => {
            if (e.target.files.length) await uploadFile(e.target.files[0]);
        });
    }
    if (btnClearFile && fileInput && fileZone) {
        btnClearFile.addEventListener("click", () => {
            fileInput.value = "";
            fileZone.innerHTML = "<b>Перетащите файл сюда</b> или нажмите для выбора (.txt)";
            const table = document.getElementById("matrix-table-file");
            if (table) table.innerHTML = "";
            document.getElementById("wrapper-file").style.display = "none";
            hideResultPanel();
        });
    }

    async function uploadFile(file) {
        if (!file) return;
        if (fileZone) fileZone.innerHTML = `<b>${file.name}</b> загружен`;
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/euler/from_file", { method: "POST", body: formData });
            const data = await response.json();
            if (data.error) { alert(data.error); return; }

            // Показываем обертку для файла и строим матрицу
            document.getElementById("wrapper-file").style.display = "block";
            buildMatrixFromData(data.matrix, "matrix-table-file");
        } catch (err) {
            console.error("Ошибка чтения файла:", err);
        }
    }

    // ==========================================
    // 5. ПОЛУЧЕНИЕ И ОТПРАВКА МАТРИЦЫ НА РЕШЕНИЕ
    // ==========================================
    const btnSolve = document.getElementById("btn-solve");
    if (btnSolve) {
        btnSolve.addEventListener("click", async () => {
            const matrix = getMatrixFromTable();
            if (!matrix || !matrix.length) {
                alert("Сначала создайте или загрузите матрицу смежности");
                return;
            }

            try {
                const response = await fetch("/euler/solve", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ matrix })
                });
                const data = await response.json();
                lastData = data;

                const resPanel = document.getElementById("result-panel");
                if (resPanel) resPanel.style.display = "block";

                switchResultView("summary");
            } catch (err) {
                console.error("Ошибка отправки на сервер:", err);
            }
        });
    }

    function getMatrixFromTable() {
        // Динамически берем таблицу из активного в данный момент таба
        const currentTableId = getActiveTableId();
        const table = document.getElementById(currentTableId);
        const matrix = [];
        if (!table || !table.rows.length) return matrix;

        for (let i = 0; i < table.rows.length; i++) {
            const row = [];
            for (let j = 0; j < table.rows[i].cells.length; j++) {
                const input = table.rows[i].cells[j].querySelector("input");
                row.push(input ? Number(input.value) : 0);
            }
            matrix.push(row);
        }
        return matrix;
    }

    function buildMatrixFromData(matrix, tableId) {
        const table = document.getElementById(tableId);
        if (!table) return;

        table.innerHTML = "";
        const n = matrix.length;

        for (let i = 0; i < n; i++) {
            const tr = document.createElement("tr");
            for (let j = 0; j < n; j++) {
                const td = document.createElement("td");
                const input = document.createElement("input");
                input.type = "number";
                input.min = 0;
                input.max = 1;
                input.value = matrix[i][j];

                if (i === j) {
                    input.disabled = true;
                }

                td.appendChild(input);
                tr.appendChild(td);
            }
            table.appendChild(tr);
        }
    }

    // ==========================================
    // 6. ТАБЫ РЕЗУЛЬТАТОВ (ИТОГ / МАТРИЦА ДОСТИЖИМОСТИ / СТЕПЕНИ)
    // ==========================================
    document.querySelectorAll(".result-tab").forEach(tab => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".result-tab").forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            switchResultView(tab.getAttribute("data-view"));
        });
    });

    function switchResultView(viewType) {
        const output = document.getElementById("result-output");
        const graphPlaceholder = document.getElementById("graph-placeholder");
        if (!output || !lastData) return;

        // 1. Если маршрут не существует
        if (!lastData.exists) {
            graphPlaceholder.innerHTML = `<div style="color:#e74c3c; padding:20px; text-align:center; font-weight:bold;">Граф не удовлетворяет условиям Эйлера</div>`;
            output.innerHTML = `
            <div class="step-card">
                <h4 class="theory-step-title" style="color:#e74c3c;">Маршрут невозможен</h4>
                <div class="info-panel info-warning">
                    <p><strong>Внимание:</strong> ${lastData.message}</p>
                </div>
            </div>
        `;
            return;
        }

        // 2. Отображение графа
        if (lastData.image) {
            graphPlaceholder.innerHTML = `<img src="data:image/png;base64,${lastData.image}" class="graph-image" style="max-width:100%; height:auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">`;
        }

        // 3. Вкладка "Итог" (summary)
        if (viewType === "summary") {
            const isCycle = lastData.type === "Эйлеров цикл";

            const oddVerticesHtml = lastData.odd_vertices.length
                ? lastData.odd_vertices.map(v => `<strong>Вершина ${v}</strong>`).join(" ")
                : "<span>отсутствуют (все вершины чётные)</span>";

            output.innerHTML = `
            <div class="step-card">
                <h4 class="theory-step-title">${lastData.type} найден${isCycle ? '' : 'а'}!</h4>
                
                <div class="info-panel info-success">
                    <p>Граф связен и удовлетворяет всем условиям существования ${isCycle ? 'эйлерова цикла' : 'эйлеровой цепи'}.</p>
                </div>

                <p style="margin-top:15px;"><b>Стартовая вершина:</b> <span class="degree-badge">${lastData.start_vertex}</span></p>
                <p><b>Нечётные вершины:</b> ${oddVerticesHtml}</p>
                
                <div class="theory-step-route main-route" style="margin-top: 20px;">
                    ${lastData.path.join(" → ")}
                </div>
                
                <div class="conclusion-panel" style="margin-top: 20px;">
                    <p><strong>Вывод:</strong> Каждое ребро пройдено ровно один раз — маршрут является корректным.</p>
                </div>
            </div>
        `;
        }

        // 4. Вкладка "Матрица достижимости" (closure)
        else if (viewType === "closure") {
            let matrixHtml = `
            <div class="step-card">
                <h4 class="theory-step-title">Матрица достижимости</h4>
                <p>Показывает связность графа (транзитивное замыкание):</p>
                <div style="overflow-x: auto; margin-top: 15px;">
                    <table class="matrix-table" style="margin: 0 auto; border-collapse: collapse;">
        `;
            lastData.closure.forEach(row => {
                matrixHtml += `<tr>`;
                row.forEach(cell => {
                    const colorStyle = cell ? 'style="color:#1e5128; font-weight:bold;"' : 'style="color:#7f1d1d;"';
                    matrixHtml += `<td ${colorStyle} style="border:1px solid #ddd; padding:8px; text-align:center; min-width:30px;">${cell}</td>`;
                });
                matrixHtml += `</tr>`;
            });
            matrixHtml += `</table></div></div>`;
            output.innerHTML = matrixHtml;
        }

        // 5. Вкладка "Степени вершин" (degrees)
        else if (viewType === "degrees") {
            let degsHtml = `
            <div class="step-card">
                <h4 class="theory-step-title">Степени вершин</h4>
                <div class="degrees-badge-container" style="flex-wrap: wrap; justify-content: flex-start; gap: 8px; margin-top: 15px;">
        `;
            lastData.degrees.forEach((deg, idx) => {
                const isOdd = deg % 2 !== 0;
                const label = isOdd ? `deg(${idx + 1}) = ${deg} ← нечётная` : `deg(${idx + 1}) = ${deg}`;
                // Добавляем небольшой inline-стиль только для цветовой дифференциации, как в теории
                const statusHtml = isOdd
                    ? `<span style="color:#e74c3c; font-weight:bold;">(нечётная)</span>`
                    : `<span style="color:#27ae60;">(чётная)</span>`;

                degsHtml += `<li>Вершина <strong>${idx + 1}</strong>: степень = <strong>${deg}</strong> ${statusHtml}</li>`;
            });
            degsHtml += `</div></div>`;
            output.innerHTML = degsHtml;
        }
    }

    function hideResultPanel() {
        const resPanel = document.getElementById("result-panel");
        if (resPanel) resPanel.style.display = "none";
        const graphPlaceholder = document.getElementById("graph-placeholder");
        if (graphPlaceholder) graphPlaceholder.innerHTML = "Здесь будет граф";
        lastData = null;
    }
}); // Конец DOMContentLoaded