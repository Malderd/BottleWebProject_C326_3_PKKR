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
% include('footer.tpl')
</section>