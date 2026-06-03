function prepareMatrix() {

    const table = document.getElementById("matrixTable");

    const size = table.rows.length - 1;

    let matrix = [];

    for (let i = 0; i < size; i++) {

        matrix[i] = [];

        for (let j = 0; j < size; j++) {

            if (i === j) {
                matrix[i][j] = 0;
                continue;
            }

            const checkbox =
                document.querySelector(
                    `[name="cell_${i}_${j}"]`
                );

            matrix[i][j] =
                checkbox.checked ? 1 : 0;
        }
    }

    document.getElementById("matrixData").value =
        JSON.stringify(matrix);
}