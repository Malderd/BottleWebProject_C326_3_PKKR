import unittest
from algorithms.clique_detection import is_clique, find_all_cliques, solve_cliques, generate_random_matrix 
from validations.valid_clique import validate_n, validate_matrix_cell, validate_density, validate_txt_file

class TestGraphAlgorithm(unittest.TestCase):
    # Тестирование алгоритмов поиска сообществ

    # Проверка: 3 вершины образуют сообщество
    def test_is_clique_true(self):
        matrix = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        self.assertTrue(is_clique([1, 2, 3], matrix))

    # Проверка: вершины не образуют сообщество из-за отсутствия рёбер
    def test_is_clique_false(self):
        matrix = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0]
        ]
        self.assertFalse(is_clique([1, 2, 3], matrix))

    # Проверка поиска сообщества с размерностью 3
    def test_find_all_cliques(self):
        matrix = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        cliques, truncated = find_all_cliques(matrix, 3)

        # Среди найденных есть сообщество размера 3
        self.assertTrue(any(len(c) == 3 for c in cliques))

        # Не превышает количества найденных сообществ
        self.assertFalse(truncated)

class TestGraphGenerator(unittest.TestCase):
    # Тестирование генерации случайной матрицы смежности

    # Проверка размера матрицы
    def test_matrix_size(self):
        matrix = generate_random_matrix(5, 50)

        # Количество строк
        self.assertEqual(len(matrix), 5)

        # Количество столбцов
        self.assertEqual(len(matrix[0]), 5)

class TestValidator(unittest.TestCase):
    # Тестирование функций проверки пользовательского ввода

    # Количество вершин входит в допустимый диапазон
    def test_validate_n_ok(self):
        n, err = validate_n("5")
        self.assertEqual(n, 5)
        self.assertIsNone(err)

    # Количество вершин задано некорректно
    def test_validate_n_bad(self):
        n, err = validate_n("abc")
        self.assertIsNone(n)
        self.assertIsNotNone(err)

    # Вероятность входит в допустимый диапазон
    def test_density_ok(self):
        d, err = validate_density("50")
        self.assertEqual(d, 50)
        self.assertIsNone(err)

    # Вероятность превышает допустимое значение
    def test_density_too_large(self):
        d, err = validate_density("400")
        self.assertIsNone(d)
        self.assertIsNotNone(err)

    # Вероятность меньше допустимого значения
    def test_density_negative(self):
        d, err = validate_density("-25")
        self.assertIsNone(d)
        self.assertIsNotNone(err)

    # Проверка корректного значения элемента матрицы
    def test_cell_ok(self):
        v, err = validate_matrix_cell("1")
        self.assertEqual(v, 1)
        self.assertIsNone(err)


class TestFileValidation(unittest.TestCase):
    # Тестирование загрузки и проверки матрицы из текстового файла

    # Матрица в файле корректна
    def test_txt_ok(self):
        txt = """0 1 0
1 0 1
0 1 0"""

        matrix, err = validate_txt_file(txt)
        self.assertIsNone(err)
        self.assertEqual(len(matrix), 3)

    # Матрица в файле содержит ошибку
    def test_txt_bad(self):
        txt = """0 1 0
1 0 0
0 1 0"""

        matrix, err = validate_txt_file(txt)
        self.assertIsNotNone(err)


if __name__ == '__main__':
    unittest.main()