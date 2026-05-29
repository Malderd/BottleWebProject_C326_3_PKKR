% rebase('layout.tpl', title=title)

<head>
    <meta charset="UTF-8">

    <title>
        Поиск гамильтонова цикла и цепи
    </title>

    <link rel="stylesheet"
          href="/static/content/hamillton_graph.css">
</head>

<body>

<div class="hamilton-page">

    <div class="container">

        <h1>
            Поиск гамильтонова цикла/цепи
        </h1>

        <!-- описание -->
        <details class="info-block">

            <summary>
                Описание алгоритма
            </summary>

            <div class="info-content">

                <h2>
                    Общая информация
                </h2>

                <p>
                    Данный модуль предназначен для поиска
                    гамильтоновых цепей и циклов
                    в неориентированном графе.
                </p>

                <p>
                    Граф задаётся при помощи матрицы смежности,
                    где каждая строка и столбец соответствуют вершинам,
                    а значения 0 и 1 определяют наличие рёбер между ними.
                </p>

                <h2>
                    Гамильтонова цепь
                </h2>

                <p>
                    Гамильтонова цепь —
                    это путь в графе,
                    проходящий через все вершины
                    ровно один раз.
                </p>

                <p>
                    При этом возврат в начальную вершину
                    не требуется.
                </p>

                <h2>
                    Гамильтонов цикл
                </h2>

                <p>
                    Гамильтонов цикл —
                    это замкнутый путь,
                    проходящий через каждую вершину графа
                    ровно один раз
                    с возвратом в исходную вершину.
                </p>

                <h2>
                    Принцип работы алгоритма
                </h2>

                <p>
                    Поиск решения выполняется
                    методом полного перебора.
                </p>

                <p>
                    Алгоритм последовательно строит возможные пути,
                    проверяя наличие рёбер между вершинами
                    и отсутствие повторного посещения вершин.
                </p>

                <p>
                    Если удаётся пройти через все вершины графа,
                    формируется гамильтонова цепь
                    или цикл.
                </p>

                <h2>
                    Ограничения
                </h2>

                <p>
                    Задача поиска гамильтонова цикла
                    относится к NP-полным задачам,
                    поэтому время выполнения
                    значительно увеличивается
                    при росте количества вершин.
                </p>

                <p>
                    Рекомендуется использовать графы
                    небольшой размерности.
                </p>

                <h2>
                    Формат входных данных
                </h2>

                <p>
                    Матрица смежности должна содержать:
                </p>

                <ul>
                    <li>
                        1 — если между вершинами существует ребро
                    </li>

                    <li>
                        0 — если ребро отсутствует
                    </li>

                    <li>
                        Главная диагональ должна содержать нули
                    </li>
                </ul>

                <h2>
                    Результат работы
                </h2>

                <p>
                    После выполнения алгоритма
                    отображается найденный путь,
                    тип решения
                    (гамильтонова цепь или цикл),
                    а также визуализация графа.
                </p>

            </div>

        </details>

        % if errors:

            <div class="error-box">

                % for key, value in errors.items():

                    <p>{{ value }}</p>

                % end

            </div>

        % end

        <!-- панель -->
        <div class="panel">

            <div class="panel-group">

                <label>
                    Количество вершин:
                </label>

                <input
                    type="number"
                    id="size"
                    min="1"
                    max="15"
                    value="5">

            </div>

            <div class="panel-buttons">

                <button
                    type="button"
                    onclick="createMatrix()">

                    Создать матрицу

                </button>

                <button
                    type="button"
                    onclick="generateMatrix()">

                    Сгенерировать граф

                </button>

                <button
                    type="button">

                    Загрузить файл

                </button>

                <button
                    type="button"
                    onclick="createMatrix()">

                    Очистить матрицу

                </button>

            </div>

        </div>

        <form
            action="/decide_hamillton_graph"
            method="post">

            <input
                type="hidden"
                id="hiddenN"
                name="n">

            <div id="matrixContainer"></div>

            <!-- действия -->
            <div class="action-buttons">

                <button
                    type="submit"
                    class="submit-btn">

                    Найти решение

                </button>

                <button
                    type="button"
                    class="save-btn">

                    Сохранить результаты

                </button>

            </div>

            <!-- граф -->
            <div class="graph-section">

                <h2>
                    Визуализация графа
                </h2>

                <div class="graph-box">
                </div>

            </div>

        </form>

    </div>

</div>

```javascript id="5x4uk9"
<script>

function createMatrix() {

    const n =
        Number(
            document.getElementById('size').value
        );

    document.getElementById(
        'hiddenN'
    ).value = n;

    let html = '<table class="matrix">';

    for (let i = 0; i < n; i++) {

        html += '<tr>';

        for (let j = 0; j < n; j++) {

            html += `
                <td>
                    <input
                        class="cell"
                        type="number"
                        min="0"
                        max="1"
                        value="${i === j ? 0 : ''}"
                        name="cell_${i}_${j}">
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

function generateMatrix() {

    createMatrix();

    const n =
        Number(
            document.getElementById('size').value
        );

    for (let i = 0; i < n; i++) {

        for (let j = i; j < n; j++) {

            const value =
                i === j
                ? 0
                : Math.random() < 0.5 ? 0 : 1;

            const first =
                document.getElementsByName(
                    `cell_${i}_${j}`
                )[0];

            const second =
                document.getElementsByName(
                    `cell_${j}_${i}`
                )[0];

            first.value = value;
            second.value = value;
        }
    }
}

window.onload = createMatrix;

</script>

</body>
