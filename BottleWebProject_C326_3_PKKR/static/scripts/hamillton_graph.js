const formData = {
    ...window.formData
};

function createMatrix() {

    const n =
        Number(
            document.getElementById('size').value
        );

    const errorBox =
        document.getElementById('matrixError');

    errorBox.innerHTML = '';

    if (n < 3) {

        errorBox.innerHTML =
            'Количество вершин не должно быть меньше 3.';

        return;
    }

    if (n > 15) {

        errorBox.innerHTML =
            'Количество вершин не должно превышать 15.';

        return;
    }

    document.getElementById(
        'hiddenN'
    ).value = n;

    let html = '<table class="matrix">';

    for (let i = 0; i < n; i++) {

        html += '<tr>';

        for (let j = 0; j < n; j++) {

            const key =
                `cell_${i}_${j}`;

            let value = '';

            if (formData[key] !== undefined) {

                value = formData[key];

            } else if (i === j) {

                value = '0';
            }

            html += `
                <td>
                    <input
                        class="cell"
                        type="number"
                        min="0"
                        max="1"
                        value="${value}"
                        name="${key}">
                </td>
            `;
        }

        html += '</tr>';
    }

    html += '</table>';

    document.getElementById(
        'matrixContainer'
    ).innerHTML = html;
}


function clearMatrix() {
    const n =
        Number(
            document.getElementById('size').value
        );

    const errorBox =
        document.getElementById('matrixError');

    errorBox.innerHTML = '';

    if (n < 3) {

        errorBox.innerHTML =
            'Количество вершин не должно быть меньше 3.';

        return;
    }

    if (n > 15) {

        errorBox.innerHTML =
            'Количество вершин не должно превышать 15.';

        return;
    }

    document.getElementById(
        'hiddenN'
    ).value = n;

    let html = '<table class="matrix">';

    for (let i = 0; i < n; i++) {

        html += '<tr>';

        for (let j = 0; j < n; j++) {

            const value =
                i === j ? '0' : '';

            html += `
                <td>
                    <input
                        class="cell"
                        type="number"
                        min="0"
                        max="1"
                        value="${value}"
                        name="cell_${i}_${j}">
                </td>
            `;
        }

        html += '</tr>';
    }

    html += '</table>';

    document.getElementById(
        'matrixContainer'
    ).innerHTML = html;
}

function generateMatrix() {

    const n =
        Number(
            document.getElementById('size').value
        );

    const errorBox =
        document.getElementById('matrixError');

    errorBox.innerHTML = '';

    if (n < 3) {

        errorBox.innerHTML =
            'Количество вершин не должно быть меньше 3.';

        return;
    }

    if (n > 15) {

        errorBox.innerHTML =
            'Количество вершин не должно превышать 15.';

        return;
    }

    createMatrix();

    for (let i = 0; i < n; i++) {

        for (let j = i; j < n; j++) {

            const value =
                i === j ? 0 : Math.random() < 0.5 ? 0 : 1;

            const first =
                document.getElementsByName(
                    `cell_${i}_${j}`
                )[0];

            const second =
                document.getElementsByName(
                    `cell_${j}_${i}`
                )[0];

            first.value = value;
            second.value = value;
        }
    }
}

window.onload = createMatrix;
