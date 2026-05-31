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
                        if defined('n') and n:
                            n_size = n
                        else:
                            n_size_raw = request.query.get('n_size', '')
                            n_size = int(n_size_raw) if n_size_raw.isdigit() and 3 <= int(n_size_raw) <= 12 else 0
                        end
                        %>

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
                                        <td class="diag">0</td>

                                        % elif j > i:
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
                                       placeholder="Плотность рёбер %"
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

                    % if defined('result') and result and result.get('graph_png'):
                    <div class="graph-placeholder" style="padding:0; border:none; background:none;">
                        <img src="data:image/png;base64,{{result['graph_png']}}"
                             alt="Граф"
                             style="width:100%; height:100%; object-fit:fill; border-radius:14px; display:block;">
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

                    <form method="POST" action="/clique_save" id="save-form" style="display:none"></form>

                    <div class="result-block">

                        <h2>Найденные клики</h2>

                        <div class="result-list" id="result-list">
                            % if defined('result') and result and result.get('maximal_cliques') is not None:
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
<script>
    var hero = document.querySelector('.hero-cliques');

    var scrollY = sessionStorage.getItem('clique_scroll');
    if (scrollY) {
        hero.scrollTop = parseInt(scrollY);
        sessionStorage.removeItem('clique_scroll');
    }

    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('scroll-link')) return;
        sessionStorage.setItem('clique_scroll', hero.scrollTop);
    });

    var btnCreate  = document.getElementById('btn-create-matrix');
    var btnClear   = document.getElementById('btn-clear-matrix');
    var btnSolve   = document.getElementById('btn-solve');
    var btnSave    = document.getElementById('btn-save');

    var nInput       = document.querySelector('input[name="n_size"]');
    var densityInput = document.querySelector('input[name="density"]');

    var hasMatrix  = !!document.getElementById('matrix-form');
    var hasGraph   = !!document.querySelector('.graph-placeholder img');

    function updateButtons() {

        var nFilled = nInput && nInput.value.trim() !== '';

        if (densityInput) {
            var densityFilled = densityInput.value.trim() !== '';

            if (btnCreate) {
                btnCreate.disabled = !(nFilled && densityFilled);
            }
        }
        else {
            if (btnCreate) {
                btnCreate.disabled = !nFilled;
            }
        }

        if (btnClear) btnClear.disabled = !nFilled;
        if (btnSolve) btnSolve.disabled = !hasMatrix;
        if (btnSave) btnSave.disabled = !hasGraph;
    }

    if (nInput) nInput.addEventListener('input', updateButtons);
    if (densityInput) densityInput.addEventListener('input', updateButtons);

    updateButtons();

    if (btnSolve) {
        btnSolve.addEventListener('click', function () {
            var form = document.getElementById('matrix-form');
            if (form) form.submit();
        });
    }

    if (btnSave) {
        btnSave.addEventListener('click', function () {
            var matrixForm = document.getElementById('matrix-form');
            var saveForm   = document.getElementById('save-form');
            if (!matrixForm || !saveForm) return;

            saveForm.innerHTML = '';
            var inputs = matrixForm.querySelectorAll('input');
            inputs.forEach(function (inp) {
                var copy = document.createElement('input');
                copy.type  = 'hidden';
                copy.name  = inp.name;
                copy.value = inp.value;
                saveForm.appendChild(copy);
            });

            saveForm.submit();
        });
    }
</script>
