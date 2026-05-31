% rebase('layout.tpl', title='Поиск компонент сильной связности')

<link rel="stylesheet" href="/static/content/kosarayu_algorithm.css">

<section class="components_of_strong_connectivity">

    <div class="overlay"></div>

    <div class="content">
        <div class="header-nav">
            <h1>Поиск компонент сильной связности</h1>

            <a href="#graph-form" class="scroll-btn">
                ⬇&nbsp;&nbsp;Перейти к задаче
             </a>
        </div>

        <!-- ТЕОРИЯ -->
        <details class="theory-block">

            <summary>
                Теоретические сведения
            </summary>

            <div class="theory-content">

                <p>
                    <i>Ориентированный граф</i> (или орграф) – это граф, у которого каждое ребро (дуга) направлено от одной вершины к другой.
                    По таким рёбрам можно двигаться только в указанном стрелкой направлении.
                </p>

                <img src="/static/images/directed_graph.png" class="directed_graph-img" alt="Ориентированный граф">

                <p>
                    <i>Компонентой сильной связности</i> ориентированного графа называется такое максимальное по включению подмножество его вершин,
                    что между любыми двумя вершинами существует путь.
                </p>

                <img src="/static/images/components_strong_connectivity.png" class="components-img" alt="Компоненты сильной связности">

                <p>
                    <i>Поиск в глубину</i> (англ. Depth-First Search, DFS) – один из методов обхода графа.
                    Стратегия поиска в глубину состоит в том, чтобы идти «вглубь» графа насколько это возможно,
                    и только потом возвращаться назад.
                </p>

                <p>
                    <i>Алгоритм Косарайю</i> предназначен для поиска компонент сильной связности ориентированного графа
                    и состоит из двух обходов графа в глубину (DFS).
                </p>

                <p>Его идея заключается в следующем:</p>
                 <div class="block">
                <p>
                    <b>1.</b> Выполняется DFS исходного графа, при этом фиксируется время выхода вершины
                    (завершения обхода всех достижимых из неё вершин).
                </p>

                <img src="/static/images/dfs.gif" alt="Первый обход DFS">
                </div>

                <div class="block">
                <p>
                    <b>2.</b> Строится транспонированный граф (все дуги меняют направление на противоположное).
                </p>

                <img src="/static/images/transposed_graph.png" alt="Транспонированный граф">
                </div>

                <div class="block">
                <p>
                    <b>3.</b> После этого вершины рассматриваются в порядке, обратном порядку завершения обхода,
                    и для каждой ещё не посещённой вершины выполняется обход DFS по транспонированному графу.
                    Все вершины, найденные в ходе одного такого обхода, образуют одну компоненту сильной связности.
                </p>

                <img src="/static/images/dfs2.gif" alt="Второй обход DFS">
                </div>
            </div>

        </details>

        <div class="main-layout">

            <!-- ЛЕВАЯ КОЛОНКА -->
            <div class="left-panel" id="graph-form">

                <div class="card">

                    <h2>Представление графа в виде матрицы смежности</h2>

                    <div class="form-group">
                        <input
                            type="number"
                            min="1"
                            max="20"
                            placeholder="Количество вершин"
                        >
                         <div class="other-buttons">
                        <button class="btn other">
                            Создать матрицу
                        </button>
                        <button class="btn primary">
                            Загрузить
                        </button>
                        </div>
                    </div>

                    <div class="buttons">

                        <button class="btn primary">
                            Сгенерировать
                        </button>

                        <button class="btn other">
                            Найти компоненты
                        </button>
                        <button class="btn primary">
                            Очистить
                        </button>
                    </div>

                    <div class="matrix-wrapper">

                    <table class="matrix-table">

                        <tr>
                            <th></th>
                            % for j in range(16):
                                <th>{{j}}</th>
                            % end
                        </tr>

                        % for i in range(16):
                            <tr>

                                <th>{{i}}</th>

                                % for j in range(16):

                                    % if i == j:
                                        <td class="diagonal-cell">0</td>
                                    % else:
                                        <td>
                                            <input
                                                type="checkbox"
                                                name="cell_{{i}}_{{j}}">
                                        </td>
                                    % end

                                % end

                            </tr>
                        % end

                    </table>

                    </div>

                </div>

            </div>

            <!-- ПРАВАЯ КОЛОНКА -->
            <div class="right-panel">

                <div class="card">

                <div class="section-header">
                    <h2>Визуализация графа и результаты</h2>
                    <button class="btn primary">
                         Сохранить
                    </button>
                </div>

                <div class="graph-container">

                    <div class="graph-placeholder">
                        Здесь будет визуализация графа с выделенными компонентами сильной связности
                    </div>

                </div>

                <div class="animation-panel">

                    <button class="btn primary">
                        ▶&nbsp;&nbsp;Показать работу алгоритма
                    </button>
                        
                </div>

            </div>


            <div class="results-card">

                <h2>Найденные компоненты сильной связности</h2>

                <div class="results-info">
                    Количество компонент: <b>4</b>
                </div>

                <div class="components-list">

                    <div class="component-item">
                        <span class="component-color color-1"></span>
                        {0, 1, 2}
                    </div>

                    <div class="component-item">
                        <span class="component-color color-2"></span>
                        {3}
                    </div>

                    <div class="component-item">
                        <span class="component-color color-3"></span>
                        {4, 5}
                    </div>

                    <div class="component-item">
                        <span class="component-color color-4"></span>
                        {6, 7, 8}
                    </div>

                </div>

            </div>

            </div>

        </div>

    </div>

</section>