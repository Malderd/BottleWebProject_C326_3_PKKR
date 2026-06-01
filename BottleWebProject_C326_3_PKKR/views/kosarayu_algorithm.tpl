% rebase('layout.tpl', title='Поиск компонент сильной связности')

<link rel="stylesheet" href="/static/content/kosarayu_algorithm.css">
<script src="/static/scripts/matrix_generator.js"></script>
<script src="/static/scripts/random-graph_generator.js"></script>
<script src="/static/scripts/matrix_clear.js"></script>
<script src="/static/scripts/matrix_prepare.js"></script>

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

                % for section in theory["sections"]:

            % if section.get("block"):

                <div class="block">
                    <p>{{!section["text"]}}</p>

                    % if "image" in section:
                        <img src="{{section['image']}}" alt="{{section.get('image_caption', '')}}" class="{{section.get('image_class', '')}}">
                    % end
                </div>

            % else:

                <p>{{!section["text"]}}</p>

                % if "image" in section:
                    <img src="{{section['image']}}" alt="{{section.get('image_caption', '')}}" class="{{section.get('image_class', '')}}">
                % end

            % end

        % end
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
                            min="3"
                            max="16"
                            placeholder="Количество вершин" id="sizeInput">
                        
                        <div class="other-buttons">
                            
                            <button class="btn other" onclick="generateMatrix()">
                                Создать матрицу
                            </button>

                            <button class="btn primary">
                                Загрузить
                            </button>
                        </div>
                    </div>

                    <form method="post" action="/kosarayu_algorithm/find_components">
                        <div class="table_and_buttons" id="table_and_buttons" style="display: {{'block' if matrix else 'none'}}">
                            <div class="buttons">

                                <button type="button" class="btn primary" onclick="generateRandomGraph()">
                                    Сгенерировать
                                </button>

                                <button type="submit" class="btn other" onclick="prepareMatrix()">
                                    Найти компоненты
                                </button>

                                <button type="button" class="btn primary" onclick="clearMatrix()">
                                    Очистить
                                </button>
                            </div>

                            <div class="matrix-wrapper">

                                
                                <table class="matrix-table" id="matrixTable">
                                % if matrix:
                                    <tr>
                                        <th></th>

                                        % for j in range(len(matrix)):
                                            <th>{{j}}</th>
                                        % end

                                    </tr>

                                    % for i in range(len(matrix)):

                                        <tr>

                                            <th>{{i}}</th>

                                            % for j in range(len(matrix)):

                                                % if i == j:

                                                    <td class="diagonal-cell">
                                                        0
                                                    </td>

                                                % else:

                                                    <td>

                                                        <input
                                                            type="checkbox"
                                                            name="cell_{{i}}_{{j}}"

                                                            % if matrix[i][j]:
                                                                checked
                                                            % end
                                                        >

                                                    </td>

                                                % end

                                            % end

                                        </tr>

                                    % end
                                    % end
                                </table>

                            </div>
                            <input
                                type="hidden"
                                name="matrix_data"
                                id="matrixData">
                        </div>
                    </form>
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
% include('footer.tpl')
</section>