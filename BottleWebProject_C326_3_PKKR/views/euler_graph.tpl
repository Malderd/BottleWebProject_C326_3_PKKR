% rebase('layout.tpl', title='Поиск Эйлерова маршрута')

<link rel="stylesheet" href="/static/content/euler.css">

<section class="hero-euler">

    <div class="overlay"></div>

    <div class="content">

        <h1>Поиск Эйлерова маршрута</h1>
        <details class="theory-block">
    <summary>Теоретические сведения</summary>
    <div class="theory-content">
        <p><b>Эйлеров маршрут</b> — путь в графе, проходящий через каждое ребро ровно один раз.</p>
        <p>Эйлеров <b>цикл</b> существует тогда и только тогда, когда граф связен (инцидентные ребрам вершины находятся в одной компоненте) и все вершины имеют чётную степень.</p>
        <p>Эйлерова <b>цепь</b> существует тогда и только тогда, когда граф связен и ровно две вершины имеют нечётную степень. В этом случае маршрут обязательно начинается в одной нечётной вершине, а заканчивается в другой.</p>
        
        <div style="text-align: center; margin: 20px 0;">
            <img src="/static/images/euler_graph_example.png" alt="Пример Эйлерова графа" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
        </div>

        <hr style="border: 0; border-top: 1px dashed rgba(255,255,255,0.2); margin: 15px 0;">

        <p><b>Определение и проверка связности графа</b></p>
        <p>Граф называется <i>связным</i>, если для любых двух его вершин существует путь, соединяющий их. При поиске Эйлерова маршрута изолированные вершины (вершины нулевой степени) не влияют на результат, так как они не содержат ребер, которые необходимо обойти. Следовательно, проверять на связность нужно только подграф, состоящий из вершин со степенью больше 0.</p>
        
        <p>Программно связность проверяется следующими этапами:</p>
        <ul style="font-size: 1.8rem; line-height: 1.4; list-style-position: inside;">
            <li style="padding-left: 2em; margin-bottom: 10px;">Выбирается первая попавшаяся вершина, имеющая хотя бы одно ребро.</li>
            <li style="padding-left: 2em; margin-bottom: 10px;">Запускается алгоритм обхода графа — поиск в глубину (DFS) или поиск в ширину (BFS). Алгоритм пошагово посещает все вершины, до которых можно добраться по ребрам.</li>
            <li style="padding-left: 2em; margin-bottom: 10px;">После завершения обхода проверяется, все ли вершины графа с ненулевой степенью были отмечены как посещенные. Если обнаружена вершина со степенью 1 или более, до которой алгоритм обхода не смог дойти, граф считается несвязным (содержит несколько изолированных компонент связности), и Эйлеров маршрут в нем невозможен.</li>
        </ul>
        
        <hr style="border: 0; border-top: 1px dashed rgba(255,255,255,0.2); margin: 15px 0;">

        <p><b>Расчет степени и чётности вершин</b></p>
        <p>Степенью вершины называется количество инцидентных ей ребер. На основе матрицы смежности A размерностью N x N степень вершины i вычисляется как сумма всех элементов соответствующей i-й строки (суммируются значения элементов от j = 1 до N):</p>
        
        <p style="text-align: center; font-weight: bold; margin: 15px 0;">deg(v_i) = СУММА(A_ij) по всем j от 1 до N</p>

        <ul style="font-size: 1.8rem; line-height: 1.4; list-style-position: inside;">
            <li style="padding-left: 2em; margin-bottom: 10px;"><b>Чётная вершина</b> — вершина, степень которой делится на 2 без остатка (остаток от деления deg(v) на 2 равен 0).</li>
            <li style="padding-left: 2em; margin-bottom: 10px;"><b>Нечётная вершина</b> — вершина с нечётным значением степени (остаток от деления deg(v) на 2 не равен 0).</li>
        </ul>

        <p>Согласно лемме о рукопожатиях, сумма степеней всех вершин графа всегда равна удвоенному числу его ребер (2E), поэтому граф не может содержать нечётное количество нечётных вершин. Это фундаментальное свойство используется для первичной валидации корректности введенной матрицы смежности.</p>

        <div style="text-align: center; margin: 20px 0;">
            <img src="/static/images/adjacency_matrix_degree_formula.png" alt="Формула степени вершины через матрицу смежности" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
        </div>

        <hr style="border: 0; border-top: 1px dashed rgba(255,255,255,0.2); margin: 15px 0;">

        <p><b>Алгоритм Иерхольцера</b></p>
        <p>Данный алгоритм находит эйлеров маршрут за линейное время O(E), где E — количество рёбер графа. Он работает по принципу построения отдельных циклов с помощью модифицированного поиска в глубину (DFS): ребра удаляются из графа сразу после их прохождения. Когда алгоритм заходит в тупик (в вершину, у которой не осталось доступных ребер), эта вершина добавляется в стек результатов. После обхода всех инцидентных подциклов стек разворачивается, формируя непрерывный Эйлеров путь.</p>
    </div>
</details>
        <div class="main-layout">

            <div class="left-panel">
                <div class="workspace">
                    <div class="card graph-card">
                        <h2>Визуализация графа</h2>
                        <div class="graph-placeholder" id="graph-placeholder">
                            Здесь будет граф
                        </div>
                        <button class="btn solve-btn" id="btn-solve">
                            Построить граф и найти эйлеров маршрут
                        </button>
                    </div>
                </div>
            </div>

            <div class="right-panel">
                <div class="card">
                    <h2>Параметры графа и матрица смежности</h2>

                    <div class="tabs">
                        <button class="tab active" data-tab="manual">Вручную</button>
                        <button class="tab" data-tab="random">Случайно</button>
                        <button class="tab" data-tab="file">Из TXT</button>
                    </div>

                    <div id="tab-manual" class="tab-content">
                        <p class="tab-hint">
                            Введите количество вершин, затем заполните матрицу смежности — 
                            1 если есть ребро, 0 если нет. Диагональ всегда 0.
                        </p>
                        <div class="form-group">
                            <input type="number" id="n-manual" min="2" max="20" placeholder="Количество вершин N (до 20)">
                        </div>
                        <div class="buttons">
                            <button class="btn primary" id="btn-create-matrix">Создать матрицу</button>
                            <button class="btn secondary" id="btn-clear-matrix">Очистить</button>
                        </div>
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
                            <input type="number" id="n-random" min="2" max="20" placeholder="Количество вершин N (до 20)">
                            <input type="number" id="density" min="1" max="100" placeholder="Плотность рёбер % (Пр.: 50)">
                        </div>
                        <div class="buttons">
                            <button class="btn primary" id="btn-random">Сгенерировать случайный граф</button>
                        </div>
                    </div>

                    <div id="tab-file" class="tab-content" style="display:none">
                        <p class="tab-hint">
                            Загрузите TXT-файл с матрицей смежности. Каждая строка — одна вершина, значения разделены пробелами. N определится автоматически.
                        </p>
                        <div class="file-zone" id="file-zone">
                            <b>Перетащите файл сюда</b> или нажмите для выбора (.txt)
                        </div>
                        <input type="file" id="file-input" accept=".txt" style="display:none">
                        <div class="buttons">
                            <button class="btn primary" id="btn-choose-file">Выбрать файл</button>
                            <button class="btn secondary" id="btn-clear-file">Очистить</button>
                        </div>
                        <div class="txt-example">
                            Пример формата файла:<br>
                            <code>0 1 1 0</code><br>
                            <code>1 0 1 1</code><br>
                            <code>1 1 0 1</code><br>
                            <code>0 1 1 0</code>
                        </div>
                    </div>

                </div>
            </div>

        </div> 
        
        <div class="result-full">
            <div class="card result-card">
                <h2>Результаты анализа</h2>
                <button class="btn solve-btn secondary" id="btn-save">
                    Сохранить результаты
                </button>
                <div class="result-list" id="result-list">
                    <p>Результаты появятся после нажатия кнопки «Построить граф»</p>
                </div>
            </div>
        </div>

    </div> 
</section>

<script>
    // Переключение вкладок (Tabs)
    document.querySelectorAll('.tab').forEach(function(tab) {
        tab.addEventListener('click', function() {
            document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
            document.querySelectorAll('.tab-content').forEach(function(c) { c.style.display = 'none'; });
            tab.classList.add('active');
            document.getElementById('tab-' + tab.dataset.tab).style.display = 'block';
        });
    });

    // Логика выбора файлов кнопками и кликом на зону драг-н-дропа
    document.getElementById('btn-choose-file').addEventListener('click', function() {
        document.getElementById('file-input').click();
    });

    document.getElementById('file-zone').addEventListener('click', function() {
        document.getElementById('file-input').click();
    });

    document.getElementById('file-input').addEventListener('change', function() {
        if (this.files[0]) {
            document.querySelector('#file-zone b').textContent = this.files[0].name;
        }
    });

    // Визуальные эффекты перетаскивания (Drag and Drop)
    var fileZone = document.getElementById('file-zone');

    fileZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        fileZone.style.borderColor = 'rgba(255,255,255,0.8)';
    });

    fileZone.addEventListener('dragleave', function() {
        fileZone.style.borderColor = '';
    });

    fileZone.addEventListener('drop', function(e) {
        e.preventDefault();
        fileZone.style.borderColor = '';
        if (e.dataTransfer.files[0]) {
            document.querySelector('#file-zone b').textContent = e.dataTransfer.files[0].name;
        }
    });

    // Генерация пустой HTML-таблицы для ручного ввода матрицы
    function buildMatrixTable(n) {
        var table = document.getElementById('matrix-table');
        table.innerHTML = '';
        var header = '<tr><td class="lbl"></td>';
        for (var j = 1; j <= n; j++) header += '<td class="lbl">' + j + '</td>';
        header += '</tr>';
        table.innerHTML += header;
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
    }

    // Событие создания пустой матрицы
    document.getElementById('btn-create-matrix').addEventListener('click', function() {
        var n = parseInt(document.getElementById('n-manual').value);
        if (!n || n < 2 || n > 20) return;
        buildMatrixTable(n);
    });

    // Очистка полей ввода вкладки "Вручную"
    document.getElementById('btn-clear-matrix').addEventListener('click', function() {
        document.getElementById('matrix-table').innerHTML = '';
        document.getElementById('n-manual').value = '';
    });

    // Очистка зоны файла
    document.getElementById('btn-clear-file').addEventListener('click', function() {
        document.getElementById('file-input').value = '';
        document.querySelector('#file-zone b').textContent = 'Перетащите файл сюда';
    });

    // Переключение со случайной генерации на вкладку ручного ввода 
    document.getElementById('btn-random').addEventListener('click', function() {
        var n = parseInt(document.getElementById('n-random').value);
        if (!n || n < 2 || n > 20) return;
        
        buildMatrixTable(n);
        
        document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
        document.querySelectorAll('.tab-content').forEach(function(c) { c.style.display = 'none'; });
        document.querySelector('[data-tab="manual"]').classList.add('active');
        document.getElementById('tab-manual').style.display = 'block';
        document.getElementById('n-manual').value = n;
    });

    // Заглушка для демонстрации клика по кнопке расчёта
    document.getElementById('btn-solve').addEventListener('click', function() {
        var resultList = document.getElementById('result-list');
    });

    // Заглушка сохранения
    document.getElementById('btn-save').addEventListener('click', function() {
       
    });
</script>