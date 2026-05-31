% rebase('layout.tpl', title='Главная страница')

<link rel="stylesheet" href="/static/content/index.css" />

<div class="hero-home">

    <div class="home-content">

        <div class="hero-header">

            <h1>Теория графов</h1>

            <p class="home-subtitle">
                Интерактивная система для исследования графов, визуализации алгоритмов и анализа структуры сетей.
            </p>

        </div>

        <div class="algorithm-cards">

            <div class="algorithm-card">

                <div class="card-number">01</div>

                <h2>Эйлеров цикл</h2>

                <p>
                    Определение существования Эйлеровой цепи/цикла в неориентированном графе с выводом последовательности вершин.
                </p>

                <a href="/euler_graph">
                    Открыть раздел
                </a>

            </div>

            <div class="algorithm-card">

                <div class="card-number">02</div>

                <h2>Гамильтонов цикл</h2>

                <p>
                    Проверка существования Гамильтонова пути и цикла методом полного перебора для графов небольшой размерности.
                </p>

                <a href="/hamillton_graph">
                    Открыть раздел
                </a>

            </div>

            <div class="algorithm-card">

                <div class="card-number">03</div>

                <h2>Выявление сообществ</h2>

                <p>
                    Поиск клик и анализ связей между вершинами для выделения тесно связанных групп пользователей.
                </p>

                <a href="/clique_detection">
                    Открыть раздел
                </a>

            </div>

            <div class="algorithm-card">

                <div class="card-number">04</div>

                <h2>Компоненты связности</h2>

                <p>
                    Разбиение ориентированного графа на компоненты сильной связности алгоритмом Косарайю.
                </p>

                <a href="/kosarayu_algorithm">
                    Открыть раздел
                </a>

            </div>

        </div>

    </div>

</div>
