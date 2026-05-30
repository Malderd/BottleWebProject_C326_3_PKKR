% rebase('layout.tpl', title='Поиск максимальных клик')

<link rel="stylesheet" href="/static/content/cliques.css">
<link rel="stylesheet" href="/static/content/fonts.css">

<section class="hero-cliques">

    <div class="overlay"></div>

    <div class="content">

        <div class="page-header">
            <h1>Поиск максимальных клик графа</h1>

            <a href="#main-layout" class="scroll-link">
                Перейти к вводу данных ↓
            </a>
        </div>

        <details class="theory-block">
            <summary>Теоретические сведения</summary>

            <div class="theory-content">

                % for section in theory['sections']:

                <div class="theory-section">

                    <h3 class="theory-section-title">{{section['title']}}</h3>

                    <div class="theory-section-body">

                        <div class="theory-section-text">
                            <p>{{section['text']}}</p>
                        </div>

                        % if section.get('image'):
                        <figure class="theory-figure">
                            <img src="{{section['image']}}">
                        </figure>
                        % end

                    </div>

                </div>

                % end

            </div>
        </details>

        <div class="main-layout" id="main-layout">

            <div class="left-panel">

                <div class="card">

                    <h2>Параметры графа и матрица смежности</h2>

                    <div class="tabs">

                        <button type="button"
                                class="tab {% if tab == 'manual' %}active{% end %}"
                                data-tab="manual"
                                onclick="location.href='/clique_detection?tab=manual'">
                            ✎ Вручную
                        </button>

                        <button type="button"
                                class="tab {% if tab == 'random' %}active{% end %}"
                                data-tab="random"
                                onclick="location.href='/clique_detection?tab=random'">
                            ⚂ Случайно
                        </button>

                        <button type="button"
                                class="tab {% if tab == 'file' %}active{% end %}"
                                data-tab="file"
                                onclick="location.href='/clique_detection?tab=file'">
                            ↑ Из TXT
                        </button>

                    </div>

                    % if tab == 'manual':
                    <div class="tab-content">

                        <p class="tab-hint">
                            Введите количество вершин, затем заполните матрицу смежности.
                        </p>

                        <div class="form-group">
                            <input type="number" id="n-manual" min="1" max="20"
                                   placeholder="Количество вершин N (до 16)">
                        </div>

                        <div class="buttons">
                            <button class="btn primary" id="btn-create-matrix">
                                Создать матрицу
                            </button>
                            <button class="btn secondary" id="btn-clear-matrix">
                                Очистить
                            </button>
                        </div>

                        <div class="matrix-wrapper">
                            <table class="matrix-table" id="matrix-table"></table>
                        </div>

                    </div>
                    % end

                    % if tab == 'random':
                    <div class="tab-content">

                        <p class="tab-hint">
                            Укажите количество вершин и плотность рёбер.
                        </p>

                        <div class="form-group">
                            <input type="number" id="n-random" min="1" max="20"
                                   placeholder="Количество вершин N">
                            <input type="number" id="density" min="1" max="100"
                                   placeholder="Плотность рёбер %">
                        </div>

                        <div class="buttons">
                            <button class="btn primary" id="btn-random">
                                Сгенерировать случайный граф
                            </button>
                        </div>

                    </div>
                    % end

                    % if tab == 'file':
                    <div class="tab-content">

                        <p class="tab-hint">
                            Загрузите TXT-файл с матрицей смежности.
                        </p>

                        <div class="file-zone" id="file-zone">
                            <b>Перетащите файл сюда</b>
                            или нажмите для выбора (.txt)
                        </div>

                        <input type="file" id="file-input" accept=".txt" style="display:none">

                        <div class="buttons">
                            <button class="btn primary" id="btn-choose-file">
                                Выбрать файл
                            </button>
                            <button class="btn secondary" id="btn-clear-file">
                                Очистить
                            </button>
                        </div>

                        <div class="txt-example" id="txt-example">
                            Пример формата файла:<br>
                            <code>0 1 0 1 1 1 1</code><br>
                            <code>1 0 1 1 0 0 1</code>
                        </div>

                        <div class="matrix-wrapper" id="file-matrix-wrapper"
                             style="display:none; margin-top:18px">
                            <table class="matrix-table" id="file-matrix-table"></table>
                        </div>

                    </div>
                    % end

                </div>
            </div>

            <div class="right-panel">

                <div class="card">

                    <h2>Визуализация и результаты</h2>

                    <div class="graph-placeholder">
                        Здесь будет граф
                    </div>

                    <div class="buttons buttons-center">
                        <button class="btn primary" id="btn-solve">
                            Построить граф
                        </button>
                        <button class="btn secondary">
                            Сохранить
                        </button>
                    </div>

                    <div class="result-block">

                        <h2>Найденные клики</h2>

                        <div class="result-list">
                            <p>Результаты появятся после запуска алгоритма</p>
                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

    % include('footer.tpl')

</section>