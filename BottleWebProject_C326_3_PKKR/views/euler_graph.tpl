% rebase('layout.tpl', title='Поиск Эйлерова маршрута')

<!-- Подключение CSS -->
<link rel="stylesheet" href="/static/content/bootstrap.min.css">
<link rel="stylesheet" href="/static/content/site.css">
<link rel="stylesheet" href="/static/content/euler.css">

<!-- Подключение JSZip -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>

<section class="hero-euler">
    <div class="overlay"></div>
    <div class="content">
        <h1>Поиск Эйлерова маршрута</h1>

        <details class="theory-block">
            <summary>Теоретические сведения</summary>
            <div class="theory-content">
                <p class="theory-lead-text">
                    <strong>Эйлеров маршрут</strong> — путь в графе, проходящий через каждое ребро ровно один раз.
                </p>

                <div class="theory-cards-row">
                    <div class="theory-mini-card">
                        <div class="theory-card-badge type-cycle">Эйлеров цикл</div>
                        <p>Существует тогда и только тогда, когда граф связен и все вершины имеют чётную степень.</p>
                        <div class="card-footer">Замкнутый маршрут</div>
                    </div>

                    <div class="theory-mini-card">
                        <div class="theory-card-badge type-chain">Эйлерова цепь</div>
                        <p>Существует тогда и только тогда, когда граф связен, ровно две вершины имеют нечётную степень.
                           Маршрут начинается в одной нечётной вершине и заканчивается в другой.</p>
                        <div class="card-footer">Разомкнутый маршрут</div>
                    </div>

                    <div class="theory-mini-card">
                        <div class="theory-image-block">
                            <img src="/static/images/euler_graph_example.png"
                                 alt="Пример Эйлерова графа"
                                 class="theory-inline-img">
                        </div>
                    </div>
                </div>

                <hr class="theory-divider">

                <div class="theory-section-header">
                    <h2 class="theory-subtitle">Определение и проверка связности графа</h2>
                </div>

                <div class="info-panel">
                    <p>Граф называется <strong>связным</strong>, если для любых двух его вершин существует путь,
                       соединяющий их. Изолированные вершины (степень 0) не влияют на результат —
                       проверяется только подграф из вершин со степенью больше 0.</p>
                </div>

                <p class="list-title">Алгоритм проверки связности:</p>
                <ul class="theory-list">
                    <li>Выбирается первая вершина, имеющая хотя бы одно ребро.</li>
                    <li>Запускается обход — поиск в глубину (DFS) или в ширину (BFS).</li>
                    <li>Если после обхода осталась непосещённая вершина с ненулевой степенью — граф несвязен.</li>
                </ul>

                <hr class="theory-divider">

                <div class="theory-section-header">
                    <h2 class="theory-subtitle">Расчёт степени и чётности вершин</h2>
                </div>

                <p>Степень вершины — количество инцидентных ей рёбер. По матрице смежности A (N×N)
                   степень вершины i вычисляется как сумма элементов i-й строки:</p>

                <div class="theory-formula">
                    deg(vᵢ) = Σ Aᵢⱼ &nbsp;&nbsp; (j = 1 … N)
                </div>

                <hr class="theory-divider">

                <div class="theory-section-header">
                    <h2 class="theory-subtitle">Алгоритм Иерхольцера</h2>
                </div>

                <div class="algorithm-panel">
                    <p>Находит Эйлеров маршрут за линейное время <strong>O(E)</strong>.</p>
                </div>

                <hr class="theory-divider">

                <div class="theory-section-header">
                    <h2 class="theory-subtitle">Разобранный пример</h2>
                </div>

                <div class="step-card">
                    <h3 class="theory-step-title">Шаг 1. Проверка связности</h3>
                    <div class="theory-step-route">1 → 2 → 4 → 5 → 3</div>
                </div>

                <div class="step-card">
                    <h3 class="theory-step-title">Шаг 2. Вычисление степеней вершин</h3>
                    <div class="degrees-badge-container">
                        <span class="degree-badge">deg(1) = 2</span>
                        <span class="degree-badge">deg(2) = 2</span>
                        <span class="degree-badge">deg(3) = 2</span>
                        <span class="degree-badge">deg(4) = 3 ← нечётная</span>
                        <span class="degree-badge">deg(5) = 1 ← нечётная</span>
                    </div>
                </div>

                <div class="step-card">
                    <h3 class="theory-step-title">Шаг 3. Построение маршрута</h3>
                    <div class="theory-step-route main-route">5 → 4 → 2 → 1 → 3 → 4</div>
                </div>
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
                            1 если есть ребро, 0 если нет.
                        </p>
                        <div class="form-group">
                            <input type="number" id="n-manual" min="2" max="20" placeholder="Количество вершин N">
                        </div>
                        <div class="buttons">
                            <button class="btn" id="btn-create-matrix">Создать матрицу</button>
                            <button class="btn secondary" id="btn-clear-matrix">Очистить</button>
                        </div>
                        <div class="matrix-wrapper" id="wrapper-manual" style="display: none;">
                            <table class="matrix-table" id="matrix-table-manual"></table>
                        </div>
                    </div>

                    <div id="tab-random" class="tab-content" style="display:none">
                        <p class="tab-hint">
                            Укажите количество вершин и плотность рёбер.
                        </p>
                        <div class="form-group">
                            <input type="number" id="n-random" min="2" max="20" placeholder="Количество вершин N">
                            <input type="number" id="density" min="1" max="100" placeholder="Плотность рёбер %">
                        </div>
                        <div class="buttons">
                            <button class="btn secondary" id="btn-random">Сгенерировать случайный граф</button>
                        </div>
                        <div class="matrix-wrapper" id="wrapper-random" style="display: none;">
                            <table class="matrix-table" id="matrix-table-random"></table>
                        </div>
                    </div>

                    <div id="tab-file" class="tab-content" style="display:none">
                        <p class="tab-hint">
                            Загрузите TXT-файл с матрицей смежности.
                        </p>
                        <div class="file-zone" id="file-zone">
                            <b>Перетащите файл сюда</b> или нажмите для выбора (.txt)
                        </div>
                        <input type="file" id="file-input" accept=".txt" style="display:none">
                        <div class="buttons">
                            <button class="btn secondary" id="btn-choose-file">Выбрать файл</button>
                            <button class="btn secondary" id="btn-clear-file">Очистить</button>
                        </div>
                        <div class="matrix-wrapper" id="wrapper-file" style="display: none;">
                            <table class="matrix-table" id="matrix-table-file"></table>
                        </div>
                    </div>
                </div>

                <div class="result-full" id="result-panel" style="display: none;">
                    <div class="card result-card">
                        <div class="result-header-wrapper">
                            <h2>Результаты анализа</h2>
                            <button class="btn secondary" id="btn-save">Сохранить результаты</button>
                        </div>
                        <div id="result-output"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    % include('footer.tpl')
</section>

<!-- Подключение скриптов в конце -->
<script src="/static/scripts/euler.js"></script>