% rebase('layout.tpl', title='Поиск максимальных клик')

<link rel="stylesheet" href="/static/content/cliques.css">

<section class="hero-cliques">

    <div class="overlay"></div>

    <div class="content">

        <h1>Поиск максимальных клик графа</h1>

        <!-- ТЕОРИЯ -->
        <details class="theory-block">

            <summary>
                Теоретические сведения
            </summary>

            <div class="theory-content">

                <p>
                    Кликой называется подмножество вершин графа,
                    в котором каждая вершина соединена со всеми остальными.
                </p>

                <p>
                    Максимальная клика — это клика,
                    которую невозможно расширить
                    без нарушения свойства полной связности.
                </p>

                <p>
                    Алгоритм выполняет перебор всех подмножеств вершин,
                    проверяет наличие рёбер между всеми парами вершин
                    и выделяет максимальные сообщества графа.
                </p>

            </div>

        </details>

        <div class="main-layout">

            <!-- ЛЕВАЯ КОЛОНКА -->
            <div class="left-panel">

                <div class="card">

                    <h2>Параметры графа и матрица смежности</h2>

                    <div class="form-group">
                        <input
                            type="number"
                            min="1"
                            max="20"
                            placeholder="Введите количество вершин N"
                        >

                    </div>

                    <div class="buttons">

                        <button class="btn primary">
                            Создать матрицу
                        </button>

                        <button class="btn secondary">
                            Случайные рёбра
                        </button>

                        <button class="btn secondary">
                            Загрузить TXT
                        </button>

                    </div>

                    <div class="matrix-wrapper">

                        <table class="matrix-table">
                            <tr>
                                <td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td><td><input type="number"></td>
                            </tr>

                            <tr>
                                <td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td><input type="number"></td><td>0</td>
                            </tr>
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

                        <div class="result-item">
                            Сообщество 1: {0, 1, 2}
                        </div>

                        <div class="result-item">
                            Сообщество 2: {3}
                        </div>

                        <div class="result-item">
                            Сообщество 3: {2, 4}
                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>