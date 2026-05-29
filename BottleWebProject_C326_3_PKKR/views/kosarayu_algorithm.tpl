% rebase('layout.tpl', title='Поиск компонент сильной связности')

<link rel="stylesheet" href="/static/content/kosarayu_algorithm.css">

<section class="hero-cliques">

    <div class="overlay"></div>

    <div class="content">

        <h1>Поиск компонент сильной связности в ориентированном графе</h1>

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

                <img src="/static/images/components_of_strong_connectivity.png" class="components-img" alt="Компоненты сильной связности">

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
            <div class="left-panel">

                <div class="card">

                    <h2>Представление графа матрицей смежности</h2>

                    <div class="form-group">
                        <input
                            type="number"
                            min="1"
                            max="20"
                            placeholder="Введите количество вершин"
                        >

                    </div>

                    <div class="buttons">

                        <button class="btn primary">
                            Создать матрицу
                        </button>

                        <button class="btn primary">
                            Случайные рёбра
                        </button>

                        <button class="btn primary">
                            Загрузить
                        </button>

                    </div>

                    <div class="matrix-wrapper">

                     <table class="matrix-table">

    <tr>
        <th></th>
        % for j in range(20):
            <th>{{j}}</th>
        % end
    </tr>

    % for i in range(20):
        <tr>

            <th>{{i}}</th>

            % for j in range(20):

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

                    <h2>Визуализация и результаты</h2>

                    <div class="graph-placeholder">

                        Здесь будет граф

                    </div>

                    <button class="btn solve-btn">
                       Построить граф и найти максимальные клики
                    </button>

                    <div class="result-block">

                        <h2>Найденные компоненты сильной связности</h2>

                        <div class="result-list">

                            <p>1. {0, 1, 2}</p>

                            <p>2. {3}</p>

                            <p>3. {2, 4}</p>

                            <p>4. {5, 6, 7}</p>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>