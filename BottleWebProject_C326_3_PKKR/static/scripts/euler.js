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

            // --- ПРОВЕРКА НА ИЗОЛИРОВАННЫЕ ВЕРШИНЫ (СТРОКА ИЗ НУЛЕЙ) ---
            let hasDisconnectedVertex = false;
            let disconnectedVertices = [];

            for (let i = 0; i < matrix.length; i++) {
                // Считаем сумму элементов в строке i
                const rowSum = matrix[i].reduce((sum, val) => sum + val, 0);
                if (rowSum === 0) {
                    hasDisconnectedVertex = true;
                    disconnectedVertices.push(i + 1); // Запоминаем номер вершины (с 1)
                }
            }

            try {
                const response = await fetch("/euler/solve", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ matrix })
                });
                const data = await response.json();

              
                if (hasDisconnectedVertex) {
                    data.exists = false;
                    data.message = `Обнаружены отделенные/изолированные вершины: ${disconnectedVertices.join(", ")}. Граф несвязен!`;
                }

                lastData = data;

                const resPanel = document.getElementById("result-panel");
                if (resPanel) resPanel.style.display = "block";

                // Вызываем отрисовку результатов
                renderResults();
            } catch (err) {
                console.error("Ошибка отправки на сервер:", err);
            }
        });
    }

    function getMatrixFromTable() {
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

        // Массив для хранения ссылок на инпуты, чтобы легко находить "зеркало"
        const inputGrid = Array.from({ length: n }, () => Array(n).fill(null));

        for (let i = 0; i < n; i++) {
            const tr = document.createElement("tr");
            for (let j = 0; j < n; j++) {
                const td = document.createElement("td");
                const input = document.createElement("input");
                input.type = "number";
                input.min = 0;
                input.max = 1;
                input.value = matrix[i][j];

                // Сохраняем ссылку на инпут в сетку
                inputGrid[i][j] = input;

                // Главная диагональ (петли) — выключаем
                if (i === j) {
                    input.disabled = true;
                } else {
                    input.addEventListener("input", function () {
                        // Ограничиваем ввод (только 0 или 1, если ввели что-то другое)
                        let val = parseInt(input.value);
                        if (isNaN(val) || val < 0) val = 0;
                        if (val > 1) val = 1;
                        input.value = val;

                        // Находим зеркальный инпут (меняем i и j местами)
                        const mirrorInput = inputGrid[j][i];
                        if (mirrorInput) {
                            mirrorInput.value = val;
                        }
                    });
                }

                td.appendChild(input);
                tr.appendChild(td);
            }
            table.appendChild(tr);
        }
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
    // 6. ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ
    // ==========================================
    function renderResults() {
        const output = document.getElementById("result-output");
        const graphPlaceholder = document.getElementById("graph-placeholder");
        if (!output || !lastData) return;

        // 1. Если маршрут не существует
        if (!lastData.exists) {

            if (lastData.image) {
                graphPlaceholder.innerHTML =
                    `<img src="data:image/png;base64,${lastData.image}"
             class="graph-image"
             style="max-width:100%; height:auto;">`;
            } else {
                graphPlaceholder.innerHTML =
                    `<div style="color:#e74c3c;">Граф не удовлетворяет условиям Эйлера</div>`;
            }

            output.innerHTML = `
        <div class="step-card">
            <h4 style="color:#e74c3c;">Маршрут невозможен</h4>
            <p>${lastData.message}</p>
        </div>
    `;
            return;
        }

        // 2. Отображение графа в левой панели
        if (lastData.image) {
            graphPlaceholder.innerHTML = `<img src="data:image/png;base64,${lastData.image}" class="graph-image" style="max-width:100%; height:auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">`;
        }

        // 3. Сборка единого вывода результатов
        const isCycle = lastData.type === "Эйлеров цикл";
        const oddVerticesHtml = lastData.odd_vertices.length
            ? lastData.odd_vertices.map(v => `<strong>Вершина ${v}</strong>`).join(" ")
            : "<span>отсутствуют (все вершины чётные)</span>";

        // Генерируем HTML для степеней вершин
        let degreesHtml = "";
        lastData.degrees.forEach((deg, idx) => {
            const isOdd = deg % 2 !== 0;
            const statusHtml = isOdd
                ? `<span style="color:#e74c3c; font-weight:bold;">(нечётная)</span>`
                : `<span style="color:#27ae60;">(чётная)</span>`;
            degreesHtml += `<li>Вершина <strong>${idx + 1}</strong>: степень = <strong>${deg}</strong> ${statusHtml}</li>`;
        });

        // Генерируем HTML для матрицы достижимости
        let matrixHtml = `<table class="matrix-table" style="margin: 15px auto 0 auto; border-collapse: collapse;">`;
        lastData.closure.forEach(row => {
            matrixHtml += `<tr>`;
            row.forEach(cell => {
                const colorStyle = cell ? 'style="color:#2ecc71; font-weight:bold;"' : 'style="color:#e74c3c;"';
                matrixHtml += `<td ${colorStyle} style="border:1px solid #ddd; padding:8px; text-align:center; min-width:30px;">${cell}</td>`;
            });
            matrixHtml += `</tr>`;
        });
        matrixHtml += `</table>`;

        // Выводим все данные одним сплошным свитком
        output.innerHTML = `
            <div class="step-card" style="margin-bottom: 20px;">
                <h4 class="theory-step-title">${lastData.type} найден${isCycle ? '' : 'а'}!</h4>
                <div class="info-panel info-success" style="margin-bottom: 15px;">
                    <p>Граф связен и удовлетворяет всем условиям существования ${isCycle ? 'эйлерова цикла' : 'эйлеровой цепи'}.</p>
                </div>
                <p><b>Стартовая вершина:</b> <span class="degree-badge">${lastData.start_vertex}</span></p>
                <p><b>Нечётные вершины:</b> ${oddVerticesHtml}</p>
                
                <div class="theory-step-route main-route" style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 6px; text-align: center; font-size: 1.2em; font-weight: bold;">
                    ${lastData.path.join(" → ")}
                </div>
            </div>

            <div class="step-card" style="margin-bottom: 20px;">
                <h4 class="theory-step-title">Степени вершин</h4>
                <ul style="list-style: none; padding-left: 0; margin-top: 10px; display: flex; flex-direction: column; gap: 6px;">
                    ${degreesHtml}
                </ul>
            </div>

            <div class="step-card">
                <h4 class="theory-step-title">Матрица достижимости</h4>
                <p style="font-size: 0.9em; color: #666;">Показывает связность графа (транзитивное замыкание):</p>
                <div style="overflow-x: auto;">
                    ${matrixHtml}
                </div>
            </div>
        `;
    }

    // ==========================================
    // 7. СБОРКА И СКАЧИВАНИЕ ZIP-АРХИВА
    // ==========================================
    const btnSave = document.getElementById("btn-save");
    if (btnSave) {
        btnSave.addEventListener("click", async () => {
            if (!lastData) {
                alert("Нет данных для сохранения. Сначала найдите маршрут.");
                return;
            }

            if (typeof JSZip === "undefined") {
                alert("Ошибка: Библиотека JSZip не загружена.");
                return;
            }

            const zip = new JSZip();
            const timestamp = new Date().toISOString().slice(0, 10);

            // --- 1. Формируем текстовый отчет (report.txt) ---
            let reportText = `ОТЧЕТ ОБ АНАЛИЗЕ ГРАФА (${timestamp})\n`;
            
            if (!lastData.exists) {
                reportText += `Статус: Граф не удовлетворяет условиям Эйлера.\n`;
                reportText += `Причина: ${lastData.message}\n`;
            } else {
                reportText += `Тип маршрута: ${lastData.type}\n`;
                reportText += `Стартовая вершина: ${lastData.start_vertex}\n`;

                const oddCount = lastData.odd_vertices ? lastData.odd_vertices.length : 0;
                reportText += `Количество нечётных вершин: ${oddCount}\n`;
                if (oddCount > 0) {
                    reportText += `Нечётные вершины: ${lastData.odd_vertices.join(", ")}\n`;
                } else {
                    reportText += `Нечётные вершины: отсутствуют (все вершины чётные)\n`;
                }

                reportText += `\nЭйлеров маршрут:\n`;
                reportText += lastData.path.join(" -> ") + `\n\n`;
                reportText += `Вывод: Каждое ребро пройдено ровно один раз.\n`;
            }

            reportText += `\n Степени всех вершин:\n`;
            if (lastData.degrees) {
                lastData.degrees.forEach((deg, idx) => {
                    const status = deg % 2 !== 0 ? "(нечётная)" : "(чётная)";
                    reportText += `  Вершина ${idx + 1}: степень = ${deg} ${status}\n`;
                });
            }

            zip.file("report.txt", reportText);

            // --- 2. Формируем файл исходной матрицы (matrix.txt) ---
            const currentMatrix = getMatrixFromTable();
            if (currentMatrix && currentMatrix.length > 0) {
                const matrixText = currentMatrix.map(row => row.join(" ")).join("\n");
                zip.file("matrix.txt", matrixText);
            }

            // --- 3. Добавляем картинку графа (graph.png) ---
            if (lastData.exists && lastData.image) {
                zip.file("graph.png", lastData.image, { base64: true });
            }

            // --- 4. Генерация и скачивание архива ---
            try {
                const content = await zip.generateAsync({ type: "blob" });
                const link = document.createElement("a");
                link.href = URL.createObjectURL(content);
                link.download = `euler_graph_results_${timestamp}.zip`;

                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } catch (err) {
                console.error("Ошибка при создании ZIP-архива:", err);
                alert("Не удалось создать архив результатов.");
            }
        });
    }

    function hideResultPanel() {
        const resPanel = document.getElementById("result-panel");
        if (resPanel) resPanel.style.display = "none";
        const graphPlaceholder = document.getElementById("graph-placeholder");
        if (graphPlaceholder) graphPlaceholder.innerHTML = "Здесь будет граф";
        lastData = null;
    }
}); // Конец DOMContentLoaded