<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>
   <div class="navbar navbar-inverse navbar-fixed-top custom-navbar">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                   <span class="icon-bar"></span>
                </button>
            </div>

            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li class="{{'active' if request.path == '/home' else ''}}">
                    <a href="/home">Домашняя страница</a>
                    </li>
                    <li class="{{'active' if request.path == '/euler_graph' else ''}}">
                    <a href="/euler_graph">Эйлеров цикл</a>
                    </li>
                    <li class="{{'active' if request.path == '/hamillton_graph' else ''}}">
                    <a href="/hamillton_graph">Гамильтонов цикл</a>
                    </li>
                    <li class="{{'active' if request.path == '/clique_detection' else ''}}">
                    <a href="/clique_detection">Выявление сообществ</a>
                    </li>
                    <li class="{{'active' if request.path == '/kosarayu_algorithm' else ''}}">
                    <a href="/kosarayu_algorithm">Разбиение на компоненты</a>
                    </li>
                    <li class="{{'active' if request.path == '/about' else ''}}">
                    <a href="/about">Об авторах</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content">
        {{!base}}
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>

</body>
</html>
