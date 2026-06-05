import unittest

from algorithms.hamillton_graph import find_hamillton_graph
from validations.valid_hamillton import valid_hamillton, validate_txt_file

# Тестирование алгоритма поиска гамильтонова цепи и цикла
class TestHamilltonAlgorithm(unittest.TestCase):
    
    # Проверка наличия в графе гамильтонова цикла
    def test_cycle_exists(self):
        matrix = [
            [0,1,0,1],
            [1,0,1,0],
            [0,1,0,1],
            [1,0,1,0]
        ]

        result = find_hamillton_graph(matrix)
        self.assertIsNotNone(result)

        result_type, path = result
        self.assertEqual(result_type, 'cycle')

    # Проверка наличия в графе гамильтоновой цепи
    def test_chain_exists(self):

        matrix = [
            [0,1,0,0],
            [1,0,1,0],
            [0,1,0,1],
            [0,0,1,0]
        ]

        result = find_hamillton_graph(matrix)
        self.assertIsNotNone(result)

        result_type, path = result
        self.assertEqual(result_type, 'chain')

    # Проверка отсутствия гамильтонова цепи и цикла
    def test_no_solution(self):

        matrix = [
            [0,1,0,0],
            [1,0,0,0],
            [0,0,0,1],
            [0,0,1,0]
        ]

        result = find_hamillton_graph(matrix)
        self.assertIsNone(result)

# Тестирование валидности матрицы смежности
class TestHamilltonValidation(unittest.TestCase):
    # Проверка корректной матрицы
    def test_valid_matrix(self):

        matrix = [
            ['0','1','1'],
            ['1','0','1'],
            ['1','1','0']
        ]

        self.assertEqual(valid_hamillton(matrix), {})


    # Проверка пустой ячейки матрицы
    def test_empty_cell(self):

        matrix = [
            ['0','1',''],
            ['1','0','1'],
            ['','1','0']
        ]

        self.assertNotEqual(valid_hamillton(matrix), {})

    # Проверка недопустимого значения элемента матрицы
    def test_invalid_value(self):

        matrix = [
            ['0','2','1'],
            ['2','0','1'],
            ['1','1','0']
        ]

        self.assertNotEqual(valid_hamillton(matrix), {})

    # Проверка главной диагонали
    def test_invalid_diagonal(self):

        matrix = [
            ['1','1','0'],
            ['1','0','1'],
            ['0','1','0']
        ]

        self.assertNotEqual(valid_hamillton(matrix), {})

    # Проверка симметричности матрицы
    def test_not_symmetric(self):

        matrix = [
            ['0','1','0'],
            ['0','0','1'],
            ['0','1','0']
        ]

        self.assertNotEqual(valid_hamillton(matrix), {})

# Тестирование валидности матрицы смежности, загруженной из txt-файла
class TestHamilltonValidationFile(unittest.TestCase):
    # Проверка корректной матрицы
    def test_txt_ok(self):

        txt = """0 1 1
        1 0 1
        1 1 0"""

        matrix, err = validate_txt_file(txt)

        self.assertIsNone(err)
        self.assertEqual(len(matrix), 3)

    # Проверка что матрицы не является квадратной
    def test_txt_not_square(self):

        txt = """0 1
                1 0
                1 1"""

        matrix, err = validate_txt_file(txt)
        self.assertEqual(err, 'Матрица должна быть квадратной.')

    # Проверка недопустимого значения элемента матрицы
    def test_txt_invalid_value(self):

        txt = """0 1 2
        1 0 1
        1 1 0"""

        matrix, err = validate_txt_file(txt)
        self.assertEqual(err, 'Допустимы только значения 0 или 1.')

    # Проверка симметричности матрицы
    def test_txt_not_symmetric(self):

        txt = """0 1 0
                0 0 1
                0 1 0"""

        matrix, err = validate_txt_file(txt)
        self.assertEqual(err, 'Матрица должна быть симметричной.')

    # Проверка главной диагонали
    def test_txt_invalid_diagonal(self):

        txt = """1 1 0
                1 0 1
                0 1 0"""

        matrix, err = validate_txt_file(txt)
        self.assertEqual(err, 'На главной диагонали должны быть нули.')

if __name__ == '__main__':
    unittest.main()

