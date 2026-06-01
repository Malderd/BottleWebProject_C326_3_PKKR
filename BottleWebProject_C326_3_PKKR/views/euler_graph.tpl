% rebase('layout.tpl', title='Поиск Эйлерова маршрута')

<link rel="stylesheet" href="/static/content/euler.css">

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
                    <h3 class="theory-subtitle">Определение и проверка связности графа</h3>
                </div>

                <div class="info-panel">
                    <p>Граф называется <strong>связным</strong>, если для любых двух его вершин существует путь,
                       соединяющий их. Изолированные вершины (степень 0) не влияют на результат —
                       проверяется только подграф из вершин со степенью больше 0.</p>
                </div>

                <p class="list-title">Алгоритм проверки связности:</p>
                <ul class="theory-list">
                    <li>Выбирается первая вершина, имеющая хотя бы одно ребро.</li>
                    <li>Запускается обход — поиск в глубину (DFS) или в ширину (BFS).
                        Алгоритм посещает все вершины, достижимые по рёбрам.</li>
                    <li>Если после обхода осталась непосещённая вершина с ненулевой степенью —
                        граф несвязен и Эйлеров маршрут невозможен.</li>
                </ul>

                <hr class="theory-divider">

                <div class="theory-section-header">
                    <h3 class="theory-subtitle">Расчёт степени и чётности вершин</h3>
                </div>

                <p>Степень вершины — количество инцидентных ей рёбер. По матрице смежности A (N×N)
                   степень вершины i вычисляется как сумма элементов i-й строки:</p>

                <div class="theory-formula">
                    deg(vᵢ) = Σ Aᵢⱼ &nbsp;&nbsp; (j = 1 … N)
                </div>

                <ul class="theory-list">
                    <li><strong>Чётная вершина</strong> — deg(v) mod 2 = 0.</li>
                    <li><strong>Нечётная вершина</strong> — deg(v) mod 2 ≠ 0.</li>
                </ul>

                <div class="info-panel">
                    <p>По <strong>лемме о рукопожатиях</strong> сумма степеней всех вершин равна 2E,
                       поэтому нечётных вершин в любом графе всегда чётное количество.
                       Это используется для первичной валидации введённой матрицы.</p>
                </div>

                <div class="theory-image-block">
                    <img src="/static/images/adjacency_matrix_degree_formula.png"
                         alt="Формула степени вершины через матрицу смежности"
                         class="theory-inline-img">
                </div>

                <hr class="theory-divider">


                <div class="theory-section-header">
                    <h3 class="theory-subtitle">Алгоритм Иерхольцера</h3>
                </div>

                <div class="algorithm-panel">
                    <p>Находит Эйлеров маршрут за линейное время <strong>O(E)</strong>.
                       Работает через модифицированный DFS: рёбра удаляются сразу после прохождения.
                       При попадании в тупик вершина помещается в стек результатов.
                       После обхода всех подциклов стек разворачивается в непрерывный Эйлеров путь.</p>
                </div>

                <hr class="theory-divider">


                <div class="theory-section-header">
                    <h3 class="theory-subtitle">Разобранный пример</h3>
                </div>

                <p class="example-desc">
                    Рассмотрим неориентированный граф из 5 вершин с заданной матрицей смежности:
                </p>

                <div class="theory-flex-container">
                    <div class="theory-flex-item">
                        <div class="matrix-grid-container">
                            <div class="grid-cell label-cell"></div>
                            <div class="grid-cell label-cell">1</div>
                            <div class="grid-cell label-cell">2</div>
                            <div class="grid-cell label-cell">3</div>
                            <div class="grid-cell label-cell">4</div>
                            <div class="grid-cell label-cell">5</div>

                            <div class="grid-cell label-cell">1</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell">1</div>
                            <div class="grid-cell">1</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell zero-cell">0</div>

                            <div class="grid-cell label-cell">2</div>
                            <div class="grid-cell">1</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell">1</div>
                            <div class="grid-cell zero-cell">0</div>

                            <div class="grid-cell label-cell">3</div>
                            <div class="grid-cell">1</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell">1</div>
                            <div class="grid-cell zero-cell">0</div>

                            <div class="grid-cell label-cell">4</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell">1</div>
                            <div class="grid-cell">1</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell">1</div>

                            <div class="grid-cell label-cell">5</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell zero-cell">0</div>
                            <div class="grid-cell">1</div>
                            <div class="grid-cell zero-cell">0</div>
                        </div>
                    </div>

                    <div class="theory-flex-item">
                        <div class="graph-img-wrapper">
                            <img src="/static/images/euler_graph_example2.png" alt="Граф примера">
                            <span class="img-caption">Граф, соответствующий матрице</span>
                        </div>
                    </div>
                </div>

                
                <div class="step-card">
                    <h4 class="theory-step-title">Шаг 1. Проверка связности</h4>
                    <p>DFS из вершины 1 посещает все вершины с ненулевой степенью:</p>
                    <div class="theory-step-route">1 → 2 → 4 → 5 → 3</div>
                    <p>Все вершины достижимы — граф <strong>связен</strong>.</p>
                    <div class="theory-image-block">
                        <img src="/static/images/euler_connectivity.png"
                             alt="Проверка связности графа"
                             class="theory-inline-img">
                    </div>
                </div>

               
                <div class="step-card">
                    <h4 class="theory-step-title">Шаг 2. Вычисление степеней вершин</h4>
                    <p>Суммируем элементы каждой строки матрицы смежности:</p>

                    <div class="degrees-badge-container">
                        <span class="degree-badge">deg(1) = 2</span>
                        <span class="degree-badge">deg(2) = 2</span>
                        <span class="degree-badge">deg(3) = 2</span>
                        <span class="degree-badge">deg(4) = 3 ← нечётная</span>
                        <span class="degree-badge">deg(5) = 1 ← нечётная</span>
                    </div>

                    <div class="info-panel info-warning">
                        <p>Нечётных вершин ровно две (4 и 5) — в графе существует <strong>Эйлерова цепь</strong>.</p>
                    </div>

                    <div class="theory-image-block">
                        <img src="/static/images/euler_degrees_example.png"
                             alt="Степени вершин графа"
                             class="theory-inline-img">
                    </div>
                </div>

                <div class="step-card">
                    <h4 class="theory-step-title">Шаг 3. Построение маршрута (алгоритм Иерхольцера)</h4>
                    <p>Начинаем из нечётной вершины 5, удаляя каждое ребро после прохождения:</p>

                    <div class="theory-step-route main-route">5 → 4 → 2 → 1 → 3 → 4</div>

                    <div class="info-panel info-success">
                        <p>Каждое ребро пройдено ровно один раз — маршрут является корректной <strong>Эйлеровой цепью</strong>.</p>
                    </div>

                    <div class="theory-image-block">
                        <img src="/static/images/euler_path_result.png"
                             alt="Найденный Эйлеров маршрут"
                             class="theory-inline-img">
                    </div>
                </div>

               
                <div class="conclusion-panel">
                    <p><strong>Вывод:</strong> граф связен и содержит ровно две вершины нечётной степени —
                       все условия существования Эйлеровой цепи выполнены.</p>
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
                            1 если есть ребро, 0 если нет. Диагональ всегда 0.
                        </p>
                        <div class="form-group">
                            <input type="number" id="n-manual" min="2" max="20"
                                   placeholder="Количество вершин N (до 20)">
                        </div>
                        <div class="buttons">
                            <button class="btn" id="btn-create-matrix">Создать матрицу</button>
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
                            <input type="number" id="n-random" min="2" max="20"
                                   placeholder="Количество вершин N (до 20)">
                            <input type="number" id="density" min="1" max="100"
                                   placeholder="Плотность рёбер % (Пр.: 50)">
                        </div>
                        <div class="buttons">
                            <button class="btn" id="btn-random">Сгенерировать случайный граф</button>
                        </div>
                    </div>

                    
                    <div id="tab-file" class="tab-content" style="display:none">
                        <p class="tab-hint">
                            Загрузите TXT-файл с матрицей смежности. Каждая строка — одна вершина,
                            значения разделены пробелами. N определится автоматически.
                        </p>
                        <div class="file-zone" id="file-zone">
                            <b>Перетащите файл сюда</b> или нажмите для выбора (.txt)
                        </div>
                        <input type="file" id="file-input" accept=".txt" style="display:none">
                        <div class="buttons">
                            <button class="btn" id="btn-choose-file">Выбрать файл</button>
                            <button class="btn secondary" id="btn-clear-file">Очистить</button>
                        </div>
                        <div class="txt-example">
                            Пример формата файла:<br>
                            0 1 1 0<br>
                            1 0 1 1<br>
                            1 1 0 1<br>
                            0 1 1 0
                        </div>
                    </div>
                </div>

               
                <div class="result-full">
                    <div class="card result-card">
                        <div class="result-header-wrapper">
                            <h2>Результаты анализа</h2>
                            <button class="btn secondary" id="btn-save">
                                Сохранить результаты
                            </button>
                        </div>
                        <div id="result-output"></div>
                    </div>
                </div>

            </div>
        </div>

    </div>
</section>
