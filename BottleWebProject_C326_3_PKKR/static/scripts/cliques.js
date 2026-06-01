// Находим главный контейнер страницы
var hero = document.querySelector('.hero-cliques');

// Восстанавливаем скролл из sessionStorage, если он там есть
var scrollY = sessionStorage.getItem('clique_scroll');
if (scrollY) {
    hero.scrollTop = parseInt(scrollY);
    sessionStorage.removeItem('clique_scroll'); // чистим, чтобы не сработало дважды
}

// Сохраняем позицию скролла при клике по странице (кроме кнопки-ссылки)
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('scroll-link')) return;
    sessionStorage.setItem('clique_scroll', hero.scrollTop);
});

// Кнопки и инпуты — кэшируем селекторы
var btnCreate = document.getElementById('btn-create-matrix');
var btnClear = document.getElementById('btn-clear-matrix');
var btnSolve = document.getElementById('btn-solve');
var btnSave = document.getElementById('btn-save');
var nInput = document.querySelector('input[name="n_size"]');
var densityInput = document.querySelector('input[name="density"]');

// Флаги: есть ли уже матрица и граф на странице
var hasMatrix = !!document.getElementById('matrix-form');
var hasGraph = !!document.querySelector('.graph-placeholder img');

// Функция включения/выключения кнопок в зависимости от заполнения полей
function updateButtons() {
    var nFilled = nInput && nInput.value.trim() !== '';
    if (densityInput) {
        var densityFilled = densityInput.value.trim() !== '';
        if (btnCreate) btnCreate.disabled = !(nFilled && densityFilled);
    } else {
        // Если нет density (вкладка file) — проверяем только n
        if (btnCreate) btnCreate.disabled = !nFilled;
    }
    if (btnClear) btnClear.disabled = !nFilled;
    // Кнопка "Решить" активна, если матрица уже есть
    if (btnSolve) btnSolve.disabled = !hasMatrix;
    // Кнопка "Сохранить" активна, если граф уже отрисован
    if (btnSave) btnSave.disabled = !hasGraph;
}

// Для вкладки file: если матрица уже загружена — сразу включаем btnSolve
if (!nInput && hasMatrix && btnSolve) {
    btnSolve.disabled = false;
}

// Вешаем обработчики на инпуты, чтобы кнопки реагировали на ввод
if (nInput) nInput.addEventListener('input', updateButtons);
if (densityInput) densityInput.addEventListener('input', updateButtons);
updateButtons(); // первичный вызов

// Обработчик кнопки "Решить"
if (btnSolve) {
    btnSolve.addEventListener('click', function () {

        var placeholder = document.querySelector('.graph-placeholder');

        // Показываем лоадер вместо плейсхолдера
        if (placeholder) {
            placeholder.innerHTML = '<p>Идёт генерация графа...</p>';
        }

        // Блокируем кнопку, чтобы не кликали дважды
        btnSolve.disabled = true;

        var form = document.getElementById('matrix-form');

        // Небольшая задержка перед сабмитом (чтобы успел отрисоваться лоадер)
        setTimeout(function () {
            if (form) form.submit();
        }, 100);
    });
}

// Обработчик кнопки "Сохранить"
if (btnSave) {
    btnSave.addEventListener('click', function () {
        var matrixForm = document.getElementById('matrix-form');
        var saveForm = document.getElementById('save-form');
        if (!matrixForm || !saveForm) return;

        // Очищаем форму сохранения
        saveForm.innerHTML = '';

        // Копируем все инпуты из матрицы в скрытые поля формы сохранения
        matrixForm.querySelectorAll('input').forEach(function (inp) {
            var copy = document.createElement('input');
            copy.type = 'hidden'; copy.name = inp.name; copy.value = inp.value;
            saveForm.appendChild(copy);
        });

        // Отправляем форму
        saveForm.submit();
    });
}

// Drag-and-drop логика для зоны загрузки файла
var fileZone = document.getElementById('file-zone');
var fileInput = document.getElementById('file-input');
if (fileZone && fileInput) {
    // При перетаскивании файла над зоной — подсвечиваем рамку
    fileZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        fileZone.style.borderColor = 'rgba(255,255,255,0.8)';
    });

    // Убрали файл — вернули рамку как была
    fileZone.addEventListener('dragleave', function () {
        fileZone.style.borderColor = '';
    });

    // Файл бросили в зону
    fileZone.addEventListener('drop', function (e) {
        e.preventDefault();
        fileZone.style.borderColor = '';
        var file = e.dataTransfer.files[0];
        if (!file) return;

        // Подставляем файл в инпут и меняем текст в зоне
        fileInput.files = e.dataTransfer.files;
        fileZone.innerHTML = '<b>' + file.name + '</b> файл выбран';

        // Включаем кнопку загрузки, если она есть
        var btnUpload = document.getElementById('btn-upload');
        if (btnUpload) btnUpload.disabled = false;
    });
}