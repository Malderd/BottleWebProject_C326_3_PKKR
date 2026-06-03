// Основные элементы DOM
let currentMatrix = [];
let currentN = 0;
let currentTab = 'manual';
let currentGraphImage = null;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function () {
            const tabId = this.getAttribute('data-tab');
            switchTab(tabId);
        });
    });

    document.getElementById('btn-create-matrix').addEventListener('click', createMatrixInput);
    document.getElementById('btn-clear-matrix').addEventListener('click', clearMatrix);
    document.getElementById('btn-random').addEventListener('click', generateRandomMatrix);
    document.getElementById('btn-choose-file').addEventListener('click', () => document.getElementById('file-input').click());
    document.getElementById('btn-clear-file').addEventListener('click', clearFileMatrix);
    document.getElementById('btn-solve').addEventListener('click', solveEuler);
    document.getElementById('btn-save').addEventListener('click', saveResults);

    const fileInput = document.getElementById('file-input');
    fileInput.addEventListener('change', handleFileUpload);

    const fileZone = document.getElementById('file-zone');
    fileZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileZone.style.borderColor = '#4CAF50';
    });
    fileZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        fileZone.style.borderColor = '#ccc';
    });
    fileZone.addEventListener('drop', (e) => {
        e.preventDefault();
        fileZone.style.borderColor = '#ccc';
        const file = e.dataTransfer.files[0];
        if (file && file.name.endsWith('.txt')) {
            readFile(file);
        } else {
            alert('Пожалуйста, загрузите файл в формате .txt');
        }
    });
    fileZone.addEventListener('click', () => fileInput.click());
});

function switchTab(tabId) {
    currentTab = tabId;
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.getAttribute('data-tab') === tabId) {
            tab.classList.add('active');
        }
    });
    document.getElementById('tab-manual').style.display = tabId === 'manual' ? 'block' : 'none';
    document.getElementById('tab-random').style.display = tabId === 'random' ? 'block' : 'none';
    document.getElementById('tab-file').style.display = tabId === 'file' ? 'block' : 'none';
}

function createMatrixInput() {
    const nInput = document.getElementById('n-manual');
    let n = parseInt(nInput.value);
    if (isNaN(n) || n < 2) {
        alert('Введите количество вершин (минимум 2)');
        return;
    }
    if (n > 20) {
        alert('Максимальное количество вершин - 20');
        return;
    }
    currentN = n;
    currentMatrix = Array(n).fill().map(() => Array(n).fill(0));
    const wrapper = document.getElementById('wrapper-manual');
    const table = document.getElementById('matrix-table-manual');
    table.innerHTML = '';
    let thead = '<tr><th></th>';
    for (let i = 1; i <= n; i++) {
        thead += `<th>${i}</th>`;
    }
    thead += '</tr>';
    table.innerHTML = thead;
    for (let i = 0; i < n; i++) {
        let row = `<tr><th>${i + 1}</th>`;
        for (let j = 0; j < n; j++) {
            const isDisabled = (i === j);
            row += `<td>
                        <input type="number" 
                               class="matrix-cell" 
                               data-i="${i}" 
                               data-j="${j}"
                               min="0" 
                               max="1" 
                               value="0"
                               ${isDisabled ? 'disabled' : ''}>
                    </td>`;
        }
        row += '</tr>';
        table.innerHTML += row;
    }
    document.querySelectorAll('#matrix-table-manual .matrix-cell').forEach(cell => {
        if (!cell.disabled) {
            cell.addEventListener('change', function () {
                const i = parseInt(this.getAttribute('data-i'));
                const j = parseInt(this.getAttribute('data-j'));
                let val = parseInt(this.value);
                if (isNaN(val)) val = 0;
                if (val < 0) val = 0;
                if (val > 1) val = 1;
                currentMatrix[i][j] = val;
                const sibling = document.querySelector(`#matrix-table-manual .matrix-cell[data-i="${j}"][data-j="${i}"]`);
                if (sibling && sibling !== this) {
                    sibling.value = val;
                    currentMatrix[j][i] = val;
                }
            });
        }
    });
    wrapper.style.display = 'block';
    const placeholder = document.getElementById('graph-placeholder');
    placeholder.innerHTML = '<div style="text-align: center; padding: 50px;">Граф будет отображён после нажатия кнопки "Построить граф и найти эйлеров маршрут"</div>';
    document.getElementById('result-panel').style.display = 'none';
    currentGraphImage = null;
}

function clearMatrix() {
    const wrapper = document.getElementById('wrapper-manual');
    wrapper.style.display = 'none';
    document.getElementById('n-manual').value = '';
    currentMatrix = [];
    currentN = 0;
    const placeholder = document.getElementById('graph-placeholder');
    placeholder.innerHTML = '<div style="text-align: center; padding: 50px;">Граф будет отображён после нажатия кнопки "Построить граф и найти эйлеров маршрут"</div>';
    document.getElementById('result-panel').style.display = 'none';
    currentGraphImage = null;
}

function generateRandomMatrix() {
    const nInput = document.getElementById('n-random');
    const densityInput = document.getElementById('density');
    let n = parseInt(nInput.value);
    let density = parseInt(densityInput.value);
    if (isNaN(n) || n < 2) {
        alert('Введите количество вершин (минимум 2)');
        return;
    }
    if (n > 20) {
        alert('Максимальное количество вершин - 20');
        return;
    }
    if (isNaN(density) || density < 1 || density > 100) {
        alert('Введите плотность рёбер от 1 до 100');
        return;
    }
    fetch('/euler/random', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ n: n, density: density })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            if (data.matrix) {
                currentMatrix = data.matrix;
                currentN = n;
                displayMatrixRandom(currentMatrix);
                const placeholder = document.getElementById('graph-placeholder');
                placeholder.innerHTML = '<div style="text-align: center; padding: 50px;">Граф будет отображён после нажатия кнопки "Построить граф и найти эйлеров маршрут"</div>';
                document.getElementById('result-panel').style.display = 'none';
                currentGraphImage = null;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ошибка при генерации случайного графа');
        });
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        fetch('/euler/from_file', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                if (data.matrix) {
                    currentMatrix = data.matrix;
                    currentN = data.matrix.length;
                    displayMatrixFile(currentMatrix);
                    const placeholder = document.getElementById('graph-placeholder');
                    placeholder.innerHTML = '<div style="text-align: center; padding: 50px;">Граф будет отображён после нажатия кнопки "Построить граф и найти эйлеров маршрут"</div>';
                    document.getElementById('result-panel').style.display = 'none';
                    currentGraphImage = null;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ошибка при загрузке файла');
            });
    }
}

function readFile(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
        const content = e.target.result;
        parseMatrixFromText(content);
    };
    reader.readAsText(file);
}

function parseMatrixFromText(text) {
    const lines = text.trim().split('\n');
    const matrix = [];
    for (let line of lines) {
        const numbers = line.trim().split(/\s+/).map(Number);
        if (numbers.length > 0 && !isNaN(numbers[0])) {
            matrix.push(numbers);
        }
    }
    if (matrix.length === 0) {
        alert('Файл пуст или имеет неверный формат');
        return;
    }
    const n = matrix.length;
    for (let row of matrix) {
        if (row.length !== n) {
            alert('Матрица должна быть квадратной');
            return;
        }
    }
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            if (matrix[i][j] !== matrix[j][i]) {
                alert('Матрица должна быть симметричной (неориентированный граф)');
                return;
            }
            if (i === j && matrix[i][j] !== 0) {
                alert('На диагонали должны быть нули (нет петель)');
                return;
            }
        }
    }
    currentN = n;
    currentMatrix = matrix;
    displayMatrixFile(matrix);
}

function clearFileMatrix() {
    const wrapper = document.getElementById('wrapper-file');
    wrapper.style.display = 'none';
    document.getElementById('file-input').value = '';
    currentMatrix = [];
    currentN = 0;
    const placeholder = document.getElementById('graph-placeholder');
    placeholder.innerHTML = '<div style="text-align: center; padding: 50px;">Граф будет отображён после нажатия кнопки "Построить граф и найти эйлеров маршрут"</div>';
    document.getElementById('result-panel').style.display = 'none';
    currentGraphImage = null;
}

function drawGraph(matrix) {
    return fetch('/euler/draw', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ matrix: matrix })
    })
        .then(response => response.json())
        .then(data => {
            if (data.image) {
                currentGraphImage = data.image;
                return data.image;
            } else if (data.error) {
                throw new Error(data.error);
            } else {
                throw new Error('Ошибка при отображении графа');
            }
        });
}

function solveEuler() {
    if (currentN === 0 || currentMatrix.length === 0) {
        alert('Сначала создайте или загрузите граф');
        return;
    }
    const solveBtn = document.getElementById('btn-solve');
    const originalText = solveBtn.textContent;
    solveBtn.textContent = '⏳ Обработка...';
    solveBtn.disabled = true;
    const placeholder = document.getElementById('graph-placeholder');
    placeholder.innerHTML = '<div style="text-align: center; padding: 50px;">🔄 Построение графа и поиск маршрута...</div>';

    drawGraph(currentMatrix)
        .then(imageBase64 => {
            placeholder.innerHTML = `<img src="data:image/png;base64,${imageBase64}" alt="Граф" style="max-width: 100%; height: auto; border-radius: 8px;">`;
            return fetch('/euler/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ matrix: currentMatrix })
            });
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
            solveBtn.textContent = originalText;
            solveBtn.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            placeholder.innerHTML = `<div style="text-align: center; padding: 50px; color: red;">❌ Ошибка: ${error.message}</div>`;
            alert('Ошибка при построении графа или поиске маршрута');
            solveBtn.textContent = originalText;
            solveBtn.disabled = false;
        });
}

function displayResults(data) {
    const resultPanel = document.getElementById('result-panel');
    const resultOutput = document.getElementById('result-output');
    resultOutput.innerHTML = '';

    // Степени вершин
    const degreesDiv = document.createElement('div');
    degreesDiv.className = 'degrees-section';
    degreesDiv.innerHTML = '<h3>📊 Степени вершин</h3><div class="degrees-list"></div>';
    const degreesList = degreesDiv.querySelector('.degrees-list');
    data.degrees.forEach((deg, idx) => {
        const degItem = document.createElement('span');
        degItem.className = 'degree-item';
        if (deg === 0) {
            degItem.classList.add('isolated');
            degItem.title = 'Изолированная вершина';
        } else if (deg % 2 === 1) {
            degItem.classList.add('odd');
            degItem.title = 'Нечётная вершина';
        }
        degItem.textContent = `deg(${idx + 1}) = ${deg}`;
        degreesList.appendChild(degItem);
    });
    resultOutput.appendChild(degreesDiv);

    // Результат
    const resultDiv = document.createElement('div');
    resultDiv.className = 'result-section';
    let resultIcon = '';
    let resultClass = '';
    if (data.type === 'cycle') {
        resultIcon = '🔄';
        resultClass = 'cycle';
    }
    else if (data.type === 'isolated_vertex') {
        resultIcon = '⚠️';
        resultClass = 'disconnected';
    } else if (data.type === 'path') {
        resultIcon = '🔗';
        resultClass = 'path';
    } else if (data.type === 'disconnected') {
        resultIcon = '⚠️';
        resultClass = 'disconnected';
    } else if (data.type === 'no_edges') {
        resultIcon = '📭';
        resultClass = 'no-edges';
    } else {
        resultIcon = '❌';
        resultClass = 'none';
    }
    let resultHtml = `<h3>${resultIcon} Результат</h3><div class="result-message ${resultClass}">${data.message}</div>`;

    if (data.is_connected && data.path && data.path.length > 0) {
        resultHtml += `<div class="path-section">
                            <h4>${data.type === 'cycle' ? '🔄 Эйлеров цикл' : '🔗 Эйлерова цепь'}</h4>
                            <div class="path-display">${data.path.join(' → ')}</div>
                        </div>`;
    }
    if (data.type === 'disconnected') {
        resultHtml += `<div class="warning-section">
                            <div class="warning-message">
                                <strong>Эйлеров маршрут не существует!</strong><br>
                                Граф не является связным. Для существования Эйлерова маршрута граф должен быть связным.<br>
                                <small>Изолированные компоненты: вершины ${data.isolated_components ? data.isolated_components.join(', ') : ''}</small>
                            </div>
                        </div>`;
    }
    if (data.type === 'isolated_vertex') {
        resultHtml += `<div class="warning-section">
                        <div class="warning-message">
                            <strong>Обнаружены несвязные вершины</strong><br>
                            Невозможно выполнить поиск Эйлерова маршрута.<br>
                            <small>Изолированные вершины: ${data.isolated_vertices.join(', ')}</small>
                        </div>
                    </div>`;
    }
    if (data.type === 'no_edges') {
        resultHtml += `<div class="warning-section">
                            <div class="warning-message">
                                <strong>Нет рёбер</strong><br>
                                Граф не содержит рёбер. Эйлеров маршрут не существует.
                            </div>
                        </div>`;
    }
    resultDiv.innerHTML = resultHtml;
    resultOutput.appendChild(resultDiv);
    resultPanel.style.display = 'block';
    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function saveResults() {
    if (!currentGraphImage || currentMatrix.length === 0) {
        alert('Сначала постройте граф и найдите маршрут');
        return;
    }
    const resultOutput = document.getElementById('result-output');
    const resultText = resultOutput.innerText;
    const currentTime = new Date().toLocaleString('ru-RU');
    let report = `═══════════════════════════════════════════════════════\n`;
    report += `            АНАЛИЗ ЭЙЛЕРОВА МАРШРУТА\n`;
    report += `═══════════════════════════════════════════════════════\n\n`;
    report += `Дата и время: ${currentTime}\n`;
    report += `Количество вершин: ${currentN}\n\n`;
    report += `Матрица смежности:\n`;
    for (let i = 0; i < currentN; i++) {
        let row = `   ${i + 1}  `;
        for (let j = 0; j < currentN; j++) {
            row += `${currentMatrix[i][j]}  `;
        }
        report += row + '\n';
    }
    report += `\n${'─'.repeat(55)}\n\n`;
    report += resultText;
    report += `\n\n${'─'.repeat(55)}\n`;
    report += ` Легенда:\n`;
    report += `   • Чётные вершины: нормальные\n`;
    report += `   • Нечётные вершины: выделены цветом\n`;
    report += `   • Эйлеров цикл: все вершины чётные\n`;
    report += `   • Эйлерова цепь: ровно две нечётные вершины\n`;
    report += `\n${'═'.repeat(55)}\n`;
    const zip = new JSZip();
    zip.file("graph.png", currentGraphImage, { base64: true });
    zip.file("euler_results.txt", report);
    zip.generateAsync({ type: "blob" }).then(function (content) {
        const url = URL.createObjectURL(content);
        const a = document.createElement('a');
        a.href = url;
        a.download = `euler_results_${currentTime.replace(/[/:,. ]/g, '_')}.zip`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
}

function displayMatrixRandom(matrix) {
    const n = matrix.length;
    const wrapper = document.getElementById('wrapper-random');
    const table = document.getElementById('matrix-table-random');
    table.innerHTML = '';
    let thead = '<tr><th></th>';
    for (let i = 1; i <= n; i++) {
        thead += `<th>${i}</th>`;
    }
    thead += '</tr>';
    table.innerHTML = thead;
    for (let i = 0; i < n; i++) {
        let row = `<tr><th>${i + 1}</th>`;
        for (let j = 0; j < n; j++) {
            const isDisabled = (i === j);
            row += `<td>
                        <input type="text" 
                               class="matrix-cell-readonly" 
                               value="${matrix[i][j]}"
                               ${isDisabled ? 'disabled' : 'readonly'}
                               style="text-align: center; width: 40px;">
                    </td>`;
        }
        row += '</tr>';
        table.innerHTML += row;
    }
    wrapper.style.display = 'block';
}

function displayMatrixFile(matrix) {
    const n = matrix.length;
    const wrapper = document.getElementById('wrapper-file');
    const table = document.getElementById('matrix-table-file');
    table.innerHTML = '';
    let thead = '<tr><th></th>';
    for (let i = 1; i <= n; i++) {
        thead += `<th>${i}</th>`;
    }
    thead += '</tr>';
    table.innerHTML = thead;
    for (let i = 0; i < n; i++) {
        let row = `<tr><th>${i + 1}</th>`;
        for (let j = 0; j < n; j++) {
            const isDisabled = (i === j);
            row += `<td>
                        <input type="text" 
                               class="matrix-cell-readonly" 
                               value="${matrix[i][j]}"
                               ${isDisabled ? 'disabled' : 'readonly'}
                               style="text-align: center; width: 40px;">
                    </td>`;
        }
        row += '<tr>';
        table.innerHTML += row;
    }
    wrapper.style.display = 'block';
}