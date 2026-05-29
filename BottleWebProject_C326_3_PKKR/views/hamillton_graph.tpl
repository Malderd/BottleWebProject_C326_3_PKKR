% rebase('layout.tpl', title=title)

<head>
    <meta charset="UTF-8">
    <title>Поиск гамильтонова цикла и цепи</title>

    <link rel="stylesheet"
          href="/static/style.css">
</head>
<body>

<div class="container">

    <h1>
        Поиск гамильтонова цикла/цепи
    </h1>

    % if errors:

        <div class="error-box">

            % for key, value in errors.items():

                <p>{{ value }}</p>

            % end

        </div>

    % end

    <div class="panel">

        <label>
            Количество вершин:
        </label>

        <input
            type="number"
            id="size"
            min="1"
            max="15"
            value="5">

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

    </div>

    <form
        action="/decide_hamillton_graph"
        method="post">

        <input
            type="hidden"
            id="hiddenN"
            name="n">

        <div id="matrixContainer"></div>

        <button
            type="submit"
            class="submit-btn">

            Найти решение

        </button>

    </form>

    % if success:

        <hr>

        <h2>
            Результат
        </h2>

        % if result:

            % kind, path = result

            <div class="success">

                <p>
                    <strong>Да</strong>
                </p>

                % if kind == "cycle":

                    <p>
                        Найден гамильтонов цикл:
                    </p>

                    <p class="path">

                        {{ " → ".join(map(str, path + [0])) }}

                    </p>

                % else:

                    <p>
                        Найдена гамильтонова цепь:
                    </p>

                    <p class="path">

                        {{ " → ".join(map(str, path)) }}

                    </p>

                % end

            </div>

        % else:

            <div class="fail">

                <p>
                    <strong>Нет</strong>
                </p>

                <p>
                    Гамильтонова цепь или цикл не найдены.
                </p>

            </div>

        % end

    % end

</div>

<script>

function createMatrix() {

    const n =
        parseInt(
            document.getElementById("size").value
        );

    document.getElementById(
        "hiddenN"
    ).value = n;

    let html =
        '<table class="matrix">';

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
        parseInt(
            document.getElementById("size").value
        );

    for (let i = 0; i < n; i++) {

        for (let j = i + 1; j < n; j++) {

            let value =
                Math.random() < 0.5
                ? 0
                : 1;

            document.getElementsByName(
                `cell_${i}_${j}`
            )[0].value = value;

            document.getElementsByName(
                `cell_${j}_${i}`
            )[0].value = value;
        }
    }

    for (let i = 0; i < n; i++) {

        document.getElementsByName(
            `cell_${i}_${i}`
        )[0].value = 0;
    }
}

window.onload = createMatrix;

</script>

</body>
