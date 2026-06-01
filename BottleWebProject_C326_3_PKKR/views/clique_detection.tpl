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

        <!-- Раскрывающийся блок с теорией -->
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

        <!-- Основной макет: левая панель — ввод, правая — граф и результаты -->
        <div class="main-layout" id="main-layout">
            <div class="left-panel">
                <div class="card">
                    <h2>Параметры графа и матрица смежности</h2>

                    <!-- Вкладки переключают способ задания матрицы -->
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

                    <!-- ═══ ВКЛАДКА: ВРУЧНУЮ ═══════════════════════════════════
                         Шаг 1: GET-форма — пользователь вводит N, сервер рендерит матрицу.
                         Шаг 2: POST-форма — пользователь заполняет верхний треугольник,
                                 сервер зеркалит нижний и строит граф. -->
                    % if tab == 'manual':
                    <div class="tab-content">
                        <p class="tab-hint">
                            Введите количество вершин, затем заполните матрицу смежности.
                        </p>

                        <!-- Шаг 1: ввод N -->
                        <form method="GET" action="/clique_detection">
                            <input type="hidden" name="tab" value="manual">
                            <div class="form-group">
                                <input type="number" name="n_size"
                                       min="3" max="12"
                                       placeholder="Количество вершин N (3–12)"
                                       value="{{request.query.get('n_size', n if defined('n') and n else '')}}">
                            </div>
                            % if defined('errors') and errors.get('n'):
                            <p class="error-msg">{{errors['n']}}</p>
                            % end
                            <div class="buttons">
                                <button type="submit" class="btn primary" id="btn-create-matrix" disabled>
                                    Создать матрицу
                                </button>
                                <button type="button" class="btn secondary" id="btn-clear-matrix"
                                        onclick="location.href='/clique_detection?tab=manual'" disabled>
                                    Очистить
                                </button>
                            </div>
                        </form>

                        <%
                        # n_size берём из переменной шаблона (после POST) или из GET-параметра
                        if defined('n') and n:
                            n_size = n
                        else:
                            n_size_raw = request.query.get('n_size', '')
                            n_size = int(n_size_raw) if n_size_raw.isdigit() and 3 <= int(n_size_raw) <= 12 else 0
                        end
                        %>

                        <!-- Шаг 2: матрица появляется только после ввода N -->
                        % if n_size > 0:
                        <form method="POST" action="/clique_detection?n_size={{n_size}}" id="matrix-form">
                            <input type="hidden" name="tab" value="manual">
                            <input type="hidden" name="n" value="{{n_size}}">

                            <div class="matrix-wrapper">
                                <table class="matrix-table" id="matrix-table">
                                    <tr>
                                        <td class="lbl"></td>
                                        % for j in range(n_size):
                                        <td class="lbl">{{j+1}}</td>
                                        % end
                                    </tr>
                                    % for i in range(n_size):
                                    <tr>
                                        <td class="lbl">{{i+1}}</td>
                                        % for j in range(n_size):
                                        % if i == j:
                                        <!-- Диагональ всегда 0 — петли не допускаются -->
                                        <td class="diag">0</td>
                                        % elif j > i:
                                        <!-- Верхний треугольник — редактируемые ячейки -->
                                        <%
                                        prev = matrix[i][j] if defined('matrix') and matrix else 0
                                        %>
                                        <td>
                                            <input type="number"
                                                   name="m_{{i}}_{{j}}"
                                                   min="0" max="1"
                                                   value="{{prev}}"
                                                   oninput="this.value=this.value.replace(/[^01]/g,'').slice(0,1)">
                                        </td>
                                        % else:
                                        <!-- Нижний треугольник — зеркало, заполняется сервером -->
                                        <%
                                        mirror = matrix[i][j] if defined('matrix') and matrix else '–'
                                        %>
                                        <td class="mirror-cell">{{mirror}}</td>
                                        % end
                                        % end
                                    </tr>
                                    % end
                                </table>
                            </div>
                        </form>
                        % end
                    </div>
                    % end

                    <!-- ═══ ВКЛАДКА: СЛУЧАЙНО ══════════════════════════════════
                         GET-форма: пользователь задаёт N и плотность,
                         сервер генерирует случайную симметричную матрицу.
                         Ячейки readonly — матрица передаётся hidden-полями. -->
                    % if tab == 'random':
                    <div class="tab-content">
                        <p class="tab-hint">
                            Укажите количество вершин и плотность рёбер, затем нажмите «Сгенерировать».
                        </p>
                        <form method="GET" action="/clique_detection">
                            <input type="hidden" name="tab" value="random">
                            <div class="form-group">
                                <input type="number" name="n_size"
                                       min="3" max="12"
                                       placeholder="Количество вершин N (3–12)"
                                       value="{{request.query.get('n_size', n if defined('n') and n else '')}}">
                                <input type="number" name="density"
                                       min="1" max="100"
                                       placeholder="Плотность рёбер % (0-100)"
                                       value="{{request.query.get('density', '')}}">
                            </div>
                            % if defined('errors') and errors.get('n'):
                            <p class="error-msg">{{errors['n']}}</p>
                            % end
                            % if defined('errors') and errors.get('density'):
                            <p class="error-msg">{{errors['density']}}</p>
                            % end
                            <div class="buttons">
                                <button type="submit" class="btn primary" id="btn-create-matrix">
                                    Сгенерировать
                                </button>
                                <button type="button" class="btn secondary" id="btn-clear-matrix"
                                        onclick="location.href='/clique_detection?tab=random'">
                                    Очистить
                                </button>
                            </div>
                        </form>

                        <%
                        if defined('n') and n:
                            n_size = n
                        else:
                            n_size_raw = request.query.get('n_size', '')
                            n_size = int(n_size_raw) if n_size_raw.isdigit() and 3 <= int(n_size_raw) <= 12 else 0
                        end
                        %>

                        % if n_size > 0:
                        <!-- Матрица передаётся hidden-полями, ячейки только для отображения -->
                        <form method="POST" action="/clique_detection?n_size={{n_size}}&density={{request.query.get('density', '')}}" id="matrix-form">
                            <input type="hidden" name="tab" value="random">
                            <input type="hidden" name="n" value="{{n_size}}">

                            <div class="matrix-wrapper">
                                <table class="matrix-table" id="matrix-table">
                                    <tr>
                                        <td class="lbl"></td>
                                        % for j in range(n_size):
                                        <td class="lbl">{{j+1}}</td>
                                        % end
                                    </tr>
                                    % for i in range(n_size):
                                    <tr>
                                        <td class="lbl">{{i+1}}</td>
                                        % for j in range(n_size):
                                        % if i == j:
                                        <td class="diag">0</td>
                                        % elif j > i:
                                        <%
                                        prev = matrix[i][j] if defined('matrix') and matrix else 0
                                        %>
                                        <td>
                                            <input type="hidden" name="m_{{i}}_{{j}}" value="{{prev}}">
                                            {{prev}}
                                        </td>
                                        % else:
                                        <%
                                        mirror = matrix[i][j] if defined('matrix') and matrix else '–'
                                        %>
                                        <td class="mirror-cell">{{mirror}}</td>
                                        % end
                                        % end
                                    </tr>
                                    % end
                                </table>
                            </div>
                        </form>
                        % end
                    </div>
                    % end

                    <!-- ═══ ВКЛАДКА: ИЗ TXT ════════════════════════════════════
                         Шаг 1: пользователь загружает файл → POST /clique_detection_file.
                         Шаг 2: сервер парсит матрицу и возвращает её в hidden-полях.
                         Шаг 3: «Построить граф» → POST /clique_detection_file_solve.
                         Имя файла сохраняется в hidden-поле чтобы не пропадало после шага 3. -->
                    % if tab == 'file':
                    <div class="tab-content">
                        <p class="tab-hint">
                            Загрузите TXT-файл с матрицей смежности (до 12×12). В имени файла разрешены только латинские буквы, цифры и специальные символы.
                        </p>

                        <!-- Форма загрузки файла с поддержкой drag-and-drop -->
                        <form method="POST" action="/clique_detection_file"
                              enctype="multipart/form-data" id="file-upload-form">

                            <div class="file-zone" id="file-zone"
                                 onclick="document.getElementById('file-input').click()">
                                % if defined('file_name') and file_name:
                                <b>{{file_name}}</b>
                                файл загружен
                                % else:
                                <b>Перетащите файл сюда</b>
                                или нажмите для выбора (.txt)
                                % end
                            </div>

                            <input type="file" id="file-input" name="matrix_file"
                                   accept=".txt" style="display:none"
                                   onchange="
                                       var name = this.files[0] ? this.files[0].name : '';
                                       var zone = document.getElementById('file-zone');
                                       zone.innerHTML = '<b>' + name + '</b> файл выбран';
                                       document.getElementById('btn-upload').disabled = false;
                                   ">

                            % if defined('errors') and errors.get('file'):
                            <p class="error-msg">{{errors['file']}}</p>
                            % end

                            <div class="buttons">
                                <button type="submit" class="btn primary" id="btn-upload"
                                        {{'disabled' if not (defined('file_name') and file_name) else ''}}>
                                    Загрузить
                                </button>
                                <button type="button" class="btn secondary"
                                        onclick="location.href='/clique_detection?tab=file'">
                                    Очистить
                                </button>
                            </div>
                        </form>

                        <!-- Матрица и форма для построения графа появляются после загрузки файла.
                             Если файл не загружен — показываем пример формата. -->
                        % if defined('matrix') and matrix and tab == 'file':
                        <form method="POST" action="/clique_detection_file_solve" id="matrix-form">
                            <input type="hidden" name="tab" value="file">
                            <input type="hidden" name="n" value="{{n}}">
                            <!-- Имя файла передаётся чтобы зона загрузки не сбрасывалась после построения -->
                            <input type="hidden" name="file_name" value="{{file_name if defined('file_name') and file_name else ''}}">
                            % for i in range(n):
                            % for j in range(i + 1, n):
                            <input type="hidden" name="m_{{i}}_{{j}}" value="{{matrix[i][j]}}">
                            % end
                            % end

                            <div class="matrix-wrapper matrix-wrapper-file">
                                <table class="matrix-table">
                                    <tr>
                                        <td class="lbl"></td>
                                        % for j in range(n):
                                        <td class="lbl">{{j+1}}</td>
                                        % end
                                    </tr>
                                    % for i in range(n):
                                    <tr>
                                        <td class="lbl">{{i+1}}</td>
                                        % for j in range(n):
                                        % if i == j:
                                        <td class="diag">0</td>
                                        % else:
                                        <td class="mirror-cell">{{matrix[i][j]}}</td>
                                        % end
                                        % end
                                    </tr>
                                    % end
                                </table>
                            </div>
                        </form>
                        % else:
                        <div class="txt-example" id="txt-example">
                            Пример формата файла:<br>
                            <code>0 1 0 1</code><br>
                            <code>1 0 1 1</code><br>
                            <code>0 1 0 1</code><br>
                            <code>1 1 1 0</code>
                        </div>
                        % end
                    </div>
                    % end

                </div>
            </div>

            <!-- ═══ ПРАВАЯ ПАНЕЛЬ: граф и результаты ══════════════════════════
                 Граф рендерится на сервере через matplotlib и передаётся как base64 PNG.
                 «Построить граф» сабмитит matrix-form.
                 «Сохранить» копирует поля matrix-form в save-form и скачивает ZIP. -->
            <div class="right-panel">
                <div class="card">
                    <h2>Визуализация и результаты</h2>

                    % if defined('result') and result and result.get('graph_png'):
                    <div class="graph-placeholder graph-placeholder-image">
                        <img src="data:image/png;base64,{{result['graph_png']}}"
                             alt="Граф" class="graph-image">
                    </div>
                    % else:
                    <div class="graph-placeholder">
                        Здесь будет граф
                    </div>
                    % end

                    <div class="buttons buttons-center">
                        <button class="btn primary" id="btn-solve" disabled>
                            Построить граф
                        </button>
                        <button class="btn secondary" id="btn-save" disabled>
                            Сохранить
                        </button>
                    </div>

                    <!-- Скрытая форма для сохранения: JS копирует в неё поля matrix-form -->
                    <form method="POST" action="/clique_save" id="save-form" class="hidden-form"></form>

                    <div class="result-block">
                        <h2>Найденные клики</h2>

                        <div class="result-list" id="result-list">
                            % if defined('result') and result and result.get('maximal_cliques') is not None:
                                % if result.get('truncated'):
                                <p class="error-msg">⚠ Граф слишком плотный — показаны первые 300 клик.</p>
                                % end
                                % if result['maximal_cliques']:
                                <p><b>Максимальных клик найдено: {{len(result['maximal_cliques'])}}</b></p>
                                % for idx, clique in enumerate(result['maximal_cliques']):
                                <p>{{idx + 1}}) { {{', '.join(map(str, clique))}} }</p>
                                % end
                                % else:
                                <p>В данном графе максимальных клик не найдено.</p>
                                % end
                            % elif defined('errors') and errors:
                                % for key, msg in errors.items():
                                <p class="error-msg">⚠ {{msg}}</p>
                                % end
                            % else:
                            <p>Результаты появятся после запуска алгоритма</p>
                            % end
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    % include('footer.tpl')
</section>
<script src="/static/scripts/cliques.js"></script>
