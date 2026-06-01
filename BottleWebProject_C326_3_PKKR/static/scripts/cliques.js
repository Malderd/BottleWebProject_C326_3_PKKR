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

var btnCreate = document.getElementById('btn-create-matrix');
var btnClear = document.getElementById('btn-clear-matrix');
var btnSolve = document.getElementById('btn-solve');
var btnSave = document.getElementById('btn-save');
var nInput = document.querySelector('input[name="n_size"]');
var densityInput = document.querySelector('input[name="density"]');
var hasMatrix = !!document.getElementById('matrix-form');
var hasGraph = !!document.querySelector('.graph-placeholder img');

function updateButtons() {
    var nFilled = nInput && nInput.value.trim() !== '';
    if (densityInput) {
        var densityFilled = densityInput.value.trim() !== '';
        if (btnCreate) btnCreate.disabled = !(nFilled && densityFilled);
    } else {
        if (btnCreate) btnCreate.disabled = !nFilled;
    }
    if (btnClear) btnClear.disabled = !nFilled;
    // Если нет nInput (вкладка file) — кнопка активна если есть matrix-form
    if (btnSolve) btnSolve.disabled = !hasMatrix;
    if (btnSave) btnSave.disabled = !hasGraph;
}

// Для вкладки file: если matrix-form уже есть на странице — сразу активируем btnSolve
if (!nInput && hasMatrix && btnSolve) {
    btnSolve.disabled = false;
}

if (nInput) nInput.addEventListener('input', updateButtons);
if (densityInput) densityInput.addEventListener('input', updateButtons);
updateButtons();

if (btnSolve) {
    btnSolve.addEventListener('click', function () {

        var placeholder = document.querySelector('.graph-placeholder');

        if (placeholder) {
            placeholder.innerHTML = '<p>Идёт генерация графа...</p>';
        }

        btnSolve.disabled = true;

        var form = document.getElementById('matrix-form');

        setTimeout(function () {
            if (form) form.submit();
        }, 100);
    });
}

if (btnSave) {
    btnSave.addEventListener('click', function () {
        var matrixForm = document.getElementById('matrix-form');
        var saveForm = document.getElementById('save-form');
        if (!matrixForm || !saveForm) return;
        saveForm.innerHTML = '';
        matrixForm.querySelectorAll('input').forEach(function (inp) {
            var copy = document.createElement('input');
            copy.type = 'hidden'; copy.name = inp.name; copy.value = inp.value;
            saveForm.appendChild(copy);
        });
        saveForm.submit();
    });
}

// Drag-and-drop для зоны файла
var fileZone = document.getElementById('file-zone');
var fileInput = document.getElementById('file-input');
if (fileZone && fileInput) {
    fileZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        fileZone.style.borderColor = 'rgba(255,255,255,0.8)';
    });
    fileZone.addEventListener('dragleave', function () {
        fileZone.style.borderColor = '';
    });
    fileZone.addEventListener('drop', function (e) {
        e.preventDefault();
        fileZone.style.borderColor = '';
        var file = e.dataTransfer.files[0];
        if (!file) return;
        fileInput.files = e.dataTransfer.files;
        fileZone.innerHTML = '<b>' + file.name + '</b> файл выбран';
        var btnUpload = document.getElementById('btn-upload');
        if (btnUpload) btnUpload.disabled = false;
    });
}