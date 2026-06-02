const formData = window.formData || {};

// Создание таблицы матрицы
function createMatrix() {

    const n = Number(document.getElementById('size').value);
    const errorBox = document.getElementById('matrixError');

    errorBox.innerHTML = '';

    // Проверки количества вершин
    if (n < 3) {
        errorBox.innerHTML = 'Количество вершин не должно быть меньше 3.';
        return;
    }
    if (n > 15) {
        errorBox.innerHTML = 'Количество вершин не должно превышать 15.';
        return;
    }

    document.getElementById('hiddenN').value = n;

    let html = '<table class="matrix">'; // Начало таблицы

    // Цикл по строкам
    for (let i = 0; i < n; i++) {
        html += '<tr>'; // Добавление строки таблицы

        for (let j = 0; j < n; j++) {
            const key = `${i}_${j}`;
            let value = '';

            if (formData[key] !== undefined) {
                value = formData[key];
            } else if (i === j) {
                value = '0';
            }

            // Добавление ячейки
            html += `
                <td>
                    <input
                        class="cell"
                        type="number"
                        min="0"
                        max="1"
                        value="${value}"
                        name="${key}">
                </td>
            `;
        }

        html += '</tr>';
    }

    html += '</table>';

    // Вывод таблицы на страницу
    document.getElementById('matrixContainer').innerHTML = html;
}

// Очищение матрицы
function clearMatrix() {
    const n =
        Number(
            document.getElementById('size').value
        );

    const errorBox =
        document.getElementById('matrixError');

    errorBox.innerHTML = '';

    // Проверки количества вершин
    if (n < 3) {

        errorBox.innerHTML =
            'Количество вершин не должно быть меньше 3.';

        return;
    }
    if (n > 15) {

        errorBox.innerHTML =
            'Количество вершин не должно превышать 15.';

        return;
    }

    document.getElementById('hiddenN').value = n;

    let html = '<table class="matrix">'; // Начало таблицы

    // Цикл по строкам
    for (let i = 0; i < n; i++) {
        html += '<tr>'; // Добавление строки таблицы

        for (let j = 0; j < n; j++) {

            const value =
                i === j ? '0' : '';

            html += `
                <td>
                    <input
                        class="cell"
                        type="number"
                        min="0"
                        max="1"
                        value="${value}"
                        name="${i}_${j}">
                </td>
            `;
        }

        html += '</tr>';
    }

    html += '</table>';

    document.getElementById(
        'matrixContainer'
    ).innerHTML = html;
}

// Создание случайной симметричной матрицы
function generateMatrix() {

    const n = Number(document.getElementById('size').value);
    const errorBox = document.getElementById('matrixError');

    errorBox.innerHTML = '';

    // Проверки количества вершин
    if (n < 3) {

        errorBox.innerHTML =
            'Количество вершин не должно быть меньше 3.';

        return;
    }
    if (n > 15) {

        errorBox.innerHTML =
            'Количество вершин не должно превышать 15.';

        return;
    }

    createMatrix();

    for (let i = 0; i < n; i++) {

        for (let j = i; j < n; j++) {

            const value =
                i === j ? 0 : Math.random() < 0.5 ? 0 : 1;

            // Поиск первой клетки
            const first =
                document.getElementsByName(
                    `${i}_${j}`
                )[0];

            // Поиск зеркальной клетки
            const second =
                document.getElementsByName(
                    `${j}_${i}`
                )[0];

            // Запись значений
            first.value = value;
            second.value = value;
        }
    }
}

// Загрузка матрицы из txt
function loadMatrixFile(event) {

    // Получение файоа
    const file = event.target.files[0];

    if (!file) {
        return;
    }

    const reader = new FileReader();

    reader.onload = function (e) {

        // Получение текста
        const text = e.target.result.trim();

        // Разбиение на строки
        const rows = text
            .split(/\r?\n/)
            .map(row => row.trim())
            .filter(row => row.length > 0);

        // Создание матрицы
        const matrix = rows.map(
            row => row.split(/\s+/)
        );

        const n = matrix.length;

        const errorBox =
            document.getElementById(
                'matrixError'
            );

        errorBox.innerHTML = '';

        if (n < 3 || n > 15) {

            errorBox.innerHTML =
                'Размер матрицы должен быть от 3 до 15.';

            return;
        }

        for (const row of matrix) {

            if (row.length !== n) {

                errorBox.innerHTML =
                    'Матрица должна быть квадратной.';

                return;
            }
        }

        document.getElementById('size').value = n;

        document.getElementById('hiddenN').value = n;

        createMatrix();

        for (let i = 0; i < n; i++) {

            for (let j = 0; j < n; j++) {

                const cell =
                    document.getElementsByName(
                        `${i}_${j}`
                    )[0];

                cell.value =
                    matrix[i][j];
            }
        }
    };

    reader.readAsText(file);
}

// Обработчик выбора файла
document.addEventListener('DOMContentLoaded', () => {

    const fileInput =
        document.getElementById('matrixFile');

    if (!fileInput) {
        return;
    }

    fileInput.addEventListener(
        'change',
        loadMatrixFile
    );
});

window.onload = createMatrix;
