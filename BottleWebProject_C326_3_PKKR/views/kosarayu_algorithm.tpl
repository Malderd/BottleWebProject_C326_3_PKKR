% rebase('layout.tpl', title='Поиск компонент сильной связности')

<link rel="stylesheet" href="/static/content/kosarayu_algorithm.css">
<script src="/static/scripts/matrix_generator.js"></script>
<script src="/static/scripts/random-graph_generator.js"></script>
<script src="/static/scripts/matrix_clear.js"></script>
<script src="/static/scripts/matrix_prepare.js"></script>
<script src="/static/scripts/button_state.js"></script>
<script src="/static/scripts/button_find_state.js"></script>

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
                            max="14"
                            placeholder="Количество вершин" id="sizeInput">
                        
                        <div class="other-buttons">
                            
                            <button class="btn primary" onclick="generateMatrix()" id="createMatrixButton">
                                Создать матрицу
                            </button>

                            <form method="POST" action="/kosarayu_algorithm/load_matrix" enctype="multipart/form-data">
                                <label class="btn primary">
                                    Загрузить
                                    <input type="file" name="matrix_file" accept=".txt" onchange="this.form.submit()" hidden>
                                </label>
                            </form>
                        </div>
                    </div>
                        % if errors:
                            <div class="error-box">
                                <p>Ошибки:</p>
                                <ul>
                                    % for e in errors:
                                        <li>{{e}}</li>
                                    % end
                                </ul>
                            </div>
                        % end
                    <form method="post" action="/kosarayu_algorithm/find_components">
                        <div class="table_and_buttons" id="table_and_buttons" style="display: {{'block' if matrix else 'none'}}">
                            <div class="buttons">

                                <button type="button" class="btn primary" onclick="generateRandomGraph()">
                                    Сгенерировать
                                </button>

                                <button type="submit" class="btn" onclick="prepareMatrix()" id="findComponentsButton">
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
                        % if matrix and components:
                        <form method="post" action="/kosarayu_algorithm/save_matrix">

                            <input type="hidden"
                                   name="matrix"
                                   value="{{matrix}}">

                            <input type="hidden"
                                   name="components"
                                   value="{{components}}">

                            <button type="submit" class="btn primary">
                                Сохранить
                            </button>
                        </form>
                        % end
                    </div>

                    <div class="graph-container">

                        % if graph_image:
                            <img
                                src="{{graph_image}}"
                                class="graph-image"
                                alt="Граф">
                        % else:
                            <div class="graph-placeholder">
                                Здесь будет визуализация графа
                            </div>
                        % end

                    </div>

                </div>


                <div class="results-card">

                    <h2>Найденные компоненты сильной связности</h2>

                        % if components:
                            <div class="results-info">
                                Количество компонент: <b>{{len(components)}}</b>
                            </div>

                            <div class="components-list">

                                % for component in components:
                                    <div class="component-item">
                                        {{"{" + ", ".join(map(str, component)) + "}"}}
                                    </div>
                                % end

                            </div>
                            % else:
                            <div class="results-info">
                                Результаты алгоритма появятся после обработки графа
                            </div>
                        % end

                    </div>

                </div>

            </div>

        </div>

    </div>
% include('footer.tpl')
</section>