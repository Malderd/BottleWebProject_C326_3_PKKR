% rebase('layout.tpl', title='Поиск максимальных клик')

<link rel="stylesheet" href="/static/content/cliques.css">
<link rel="stylesheet" href="/static/content/fonts.css">

<section class="hero-cliques">

    <div class="overlay"></div>

    <div class="content">

        <h1>Поиск максимальных клик графа</h1>

        <details class="theory-block">

            <summary>
                Теоретические сведения
            </summary>

            <div class="theory-content">

                % for section in theory['sections']:

                    <div class="theory-section">

                        <h3 class="theory-section-title">{{section['title']}}</h3>

                        <div class="theory-section-body">

                            <div class="theory-section-text">
                                <p>{{section['text']}}</p>
                            </div>

                            <!-- картинка отображается только если путь указан в json -->
                            % if section.get('image'):
                                <figure class="theory-figure">
                                    <img src="{{section['image']}}" alt="{{section.get('image_caption', '')}}">
                                    % if section.get('image_caption'):
                                        <figcaption>{{section['image_caption']}}</figcaption>
                                    % end
                                </figure>
                            % end

                        </div>

                    </div>

                % end

            </div>

        </details>

        <div class="main-layout">

            <div class="left-panel">

                <div class="card">

                    <h2>Параметры графа и матрица смежности</h2>

                    <!-- три вкладки: вручную, случайно, из файла -->
                    <div class="tabs">
                        <button class="tab active" data-tab="manual">✎ Вручную</button>
                        <button class="tab" data-tab="random">⚂ Случайно</button>
                        <button class="tab" data-tab="file">↑ Из TXT</button>
                    </div>

                    <div id="tab-manual" class="tab-content">

                        <p class="tab-hint">
                            Введите количество вершин, затем заполните матрицу смежности —
                            1 если есть ребро, 0 если нет. Диагональ всегда 0.
                        </p>

                        <div class="form-group">
                            <input
                                type="number"
                                id="n-manual"
                                min="1"
                                max="20"
                                placeholder="Количество вершин N (до 20)"
                            >
                        </div>

                        <div class="buttons">
                            <button class="btn primary" id="btn-create-matrix">
                                Создать матрицу
                            </button>
                            <button class="btn secondary" id="btn-clear-matrix">
                                Очистить
                            </button>
                        </div>

                        <!-- таблица генерируется через js после нажатия "создать матрицу" -->
                        <div class="matrix-wrapper">
                            <table class="matrix-table" id="matrix-table"></table>
                        </div>

                    </div>

                    <div id="tab-random" class="tab-content" style="display:none">

                        <p class="tab-hint">
                            Укажите количество вершин и плотность рёбер —
                            матрица и граф будут заполнены случайными связями автоматически.
                        </p>

                        <div class="form-group">
                            <input
                                type="number"
                                id="n-random"
                                min="1"
                                max="20"
                                placeholder="Количество вершин N (до 20)"
                            >
                            <input
                                type="number"
                                id="density"
                                min="1"
                                max="100"
                                placeholder="Плотность рёбер % (Пр.: 50)"
                            >
                        </div>

                        <div class="buttons">
                            <button class="btn primary" id="btn-random">
                                Сгенерировать случайный граф
                            </button>
                        </div>

                    </div>

                    <div id="tab-file" class="tab-content" style="display:none">

                        <p class="tab-hint">
                            Загрузите TXT-файл с матрицей смежности.
                            Каждая строка — одна вершина, значения разделены пробелами.
                            N определится автоматически.
                        </p>

                        <!-- зона для перетаскивания файла -->
                        <div class="file-zone" id="file-zone">
                            <b>Перетащите файл сюда</b>
                            или нажмите для выбора (.txt)
                        </div>

                        <!-- скрытый input, открывается по клику на кнопку или зону -->
                        <input type="file" id="file-input" accept=".txt" style="display:none">

                        <div class="buttons">
                            <button class="btn primary" id="btn-choose-file">
                                Выбрать файл
                            </button>
                            <button class="btn secondary" id="btn-clear-file">
                                Очистить
                            </button>
                        </div>

                        <!-- пример симметричной матрицы -->
                        <div class="txt-example" id="txt-example">
                            Пример формата файла:<br>
                            <code>0 1 0 1 1 1 1<br></code>
                            <code>1 0 1 1 0 0 1<br></code>
                            <code>0 1 0 0 0 0 0<br></code>
                            <code>1 1 0 0 1 0 0<br></code>
                            <code>1 0 0 1 0 1 0<br></code>
                            <code>1 0 0 0 1 0 1<br></code>
                            <code>1 1 0 0 0 1 0<br></code>
                        </div>

                        <div class="matrix-wrapper" id="file-matrix-wrapper" style="display:none; margin-top:18px">
                            <table class="matrix-table" id="file-matrix-table"></table>
                        </div>

                    </div>

                </div>

            </div>

            <div class="right-panel">

                <div class="card">

                    <h2>Визуализация и результаты</h2>

                    <!-- placeholder для canvas с графом -->
                    <div class="graph-placeholder" id="graph-placeholder">
                        Здесь будет граф
                    </div>

                    <button class="btn solve-btn" id="btn-solve">
                        Построить граф и найти максимальные клики
                    </button>

                    <button class="btn solve-btn secondary" id="btn-save">
                        Сохранить результаты
                    </button>

                    <div class="result-block">

                        <h2>Найденные клики</h2>

                        <!-- сюда через js вставляются найденные клики -->
                        <div class="result-list" id="result-list">
                            <p>Результаты появятся после нажатия кнопки «Построить граф»</p>
                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>

<script>
    // переключение вкладок: скрываем все, показываем нужную
    document.querySelectorAll('.tab').forEach(function (tab) {
        tab.addEventListener('click', function () {
            document.querySelectorAll('.tab').forEach(function (t) {
                t.classList.remove('active');
            });
            document.querySelectorAll('.tab-content').forEach(function (c) {
                c.style.display = 'none';
            });
            tab.classList.add('active');
            document.getElementById('tab-' + tab.dataset.tab).style.display = 'block';
        });
    });

    // кнопка "выбрать файл" открывает скрытый input
    document.getElementById('btn-choose-file').addEventListener('click', function () {
        document.getElementById('file-input').click();
    });

    // клик по зоне drag-and-drop тоже открывает выбор файла
    var fileZone = document.getElementById('file-zone');

    fileZone.addEventListener('click', function () {
        document.getElementById('file-input').click();
    });

    // обработка drag-and-drop
    fileZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        fileZone.style.borderColor = 'rgba(255,255,255,0.8)';
    });

    fileZone.addEventListener('dragleave', function () {
        fileZone.style.borderColor = '';
    });

    fileZone.addEventListener('drop', function (e) {
        e.preventDefault();
        fileZone.style.borderColor = '';
        var file = e.dataTransfer.files[0];
        if (file) {
            fileZone.querySelector('b').textContent = file.name;
            readMatrixFile(file);
        }
    });

    // показываем имя выбранного файла и читаем матрицу
    document.getElementById('file-input').addEventListener('change', function () {
        var file = this.files[0];
        if (!file) return;
        fileZone.querySelector('b').textContent = file.name;
        readMatrixFile(file);
    });

    // читаем txt-файл и парсим матрицу
    function readMatrixFile(file) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var text = e.target.result.trim();
            var rows = text.split('\n');
            var matrix = rows.map(function (row) {
                return row.trim().split(/\s+/).map(Number);
            });
            var n = matrix.length;

            for (var i = 0; i < n; i++) {
                if (matrix[i].length !== n) {
                    alert('Матрица должна быть квадратной!');
                    return;
                }
            }

            buildFileMatrix(matrix, n);
        };
        reader.readAsText(file);
    }

    // строим таблицу матрицы во вкладке "из txt", пример пропадает
    function buildFileMatrix(matrix, n) {
        var wrapper = document.getElementById('file-matrix-wrapper');
        var example = document.getElementById('txt-example');
        var table = document.getElementById('file-matrix-table');
        table.innerHTML = '';

        var headerRow = '<tr><td class="lbl"></td>';
        for (var j = 1; j <= n; j++) {
            headerRow += '<td class="lbl">' + j + '</td>';
        }
        headerRow += '</tr>';
        table.innerHTML += headerRow;

        for (var i = 0; i < n; i++) {
            var rowHtml = '<tr><td class="lbl">' + (i + 1) + '</td>';
            for (var j = 0; j < n; j++) {
                if (i === j) {
                    rowHtml += '<td class="diag">0</td>';
                } else {
                    // readonly — редактировать нельзя
                    rowHtml += '<td><input type="number" value="' +
                        matrix[i][j] + '" name="m_' + (i + 1) + '_' + (j + 1) +
                        '" readonly tabindex="-1"></td>';
                }
            }
            rowHtml += '</tr>';
            table.innerHTML += rowHtml;
        }

        example.style.display = 'none';
        wrapper.style.display = 'block';
    }

    // очистка: убираем матрицу, возвращаем пример
    document.getElementById('btn-clear-file').addEventListener('click', function () {
        document.getElementById('file-input').value = '';
        fileZone.querySelector('b').textContent = 'Перетащите файл сюда';
        document.getElementById('file-matrix-table').innerHTML = '';
        document.getElementById('file-matrix-wrapper').style.display = 'none';
        document.getElementById('txt-example').style.display = 'block';
    });

    // генерация таблицы матрицы смежности по введённому n
    document.getElementById('btn-create-matrix').addEventListener('click', function () {
        var n = parseInt(document.getElementById('n-manual').value);
        if (!n || n < 1 || n > 20) return;

        var table = document.getElementById('matrix-table');
        table.innerHTML = '';

        // первая строка — номера столбцов
        var headerRow = '<tr><td class="lbl"></td>';
        for (var j = 1; j <= n; j++) {
            headerRow += '<td class="lbl">' + j + '</td>';
        }
        headerRow += '</tr>';
        table.innerHTML += headerRow;

        // строки матрицы: диагональ = 0, остальное — input
        for (var i = 1; i <= n; i++) {
            var row = '<tr><td class="lbl">' + i + '</td>';
            for (var j = 1; j <= n; j++) {
                if (i === j) {
                    row += '<td class="diag">0</td>';
                } else {
                    row += '<td><input type="number" min="0" max="1" value="0" name="m_' + i + '_' + j + '"></td>';
                }
            }
            row += '</tr>';
            table.innerHTML += row;
        }
    });
</script>
