import unittest
from algorithms.kosarayu_algorithm import find_components
from validations.valid_kosarayu import validate_matrix_kosarayu, validate_matrix_text

class TestKosarayuAlgorithm(unittest.TestCase):
     # Тестирование алгоритма поиска компонентов сильной связности
     
     # Проверка: граф из одной сильной компоненты (все вершины связаны)
     def test_single_component(self):
        matrix = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0]
        ]

        components = find_components(matrix)

        self.assertEqual(len(components), 1)
        self.assertEqual(sorted(components[0]), [0, 1, 2])

     # Проверка: граф разбит на две сильные компоненты
     def test_two_components(self):
        matrix = [
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [1, 0, 0, 1],
            [0, 0, 0, 0]
        ]

        components = find_components(matrix)

        normalized = sorted([sorted(c) for c in components])

        self.assertEqual(normalized, [[0, 1, 2], [3]])

     # Проверка: каждая вершина образует отдельную компоненту связности
     def test_separate_vertices_components(self):
         matrix = [
            [0, 1, 0, 1, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0]
         ]

         components = find_components(matrix)

         normalized = sorted([sorted(c) for c in components])

         self.assertEqual(normalized, [[0], [1], [2], [3], [4]])

    # Все вершины изолированные
     def test_isolated_vertices(self):
        matrix = [
            [0, 0],
            [0, 0]
        ]

        components = find_components(matrix)

        normalized = sorted([sorted(c) for c in components])

        self.assertEqual(normalized, [[0], [1]])

class TestMatrixValidation(unittest.TestCase):
    # Тестирование структуры матрицы

    # корректная матрица без ошибок
    def test_valid_matrix(self):
        matrix = [
            [0, 0, 1, 0],
            [1, 0, 0, 1],
            [0, 0, 0, 0],
            [1, 0, 0, 0]
        ]

        errors = validate_matrix_kosarayu(matrix)

        self.assertEqual(errors, [])

    # обнаружение петли (ребро в себя)
    def test_loop_detection(self):
        matrix = [
            [1, 1, 0],
            [0, 0, 1],
            [1, 0, 0]
        ]

        errors = validate_matrix_kosarayu(matrix)

        self.assertIn("Вершина 0: есть петля", errors)

    # обнаружение взаимных рёбер (антисимметрия нарушена)
    def test_mutual_edges_detection(self):
        matrix = [
            [0, 1, 0],
            [1, 0, 1],
            [1, 0, 0]
        ]

        errors = validate_matrix_kosarayu(matrix)

        self.assertIn(
            "Вершины 0 ↔ 1: взаимные ребра (нарушение антисимметрии)",
            errors
        )
    
     # обнаружение изолированных вершин
    def test_isolated_vertices_detection(self):
        matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        errors = validate_matrix_kosarayu(matrix)

        self.assertIn("Изолированные вершины: [0, 1, 2]", errors)

class TestFileValidation(unittest.TestCase):
    # Тестирование проверки матрицы из текстового файла

     # корректный ввод матрицы из текста
     def test_valid_file(self):
        text = (
            "0 1 0\n"
            "0 0 1\n"
            "1 0 0"
        )

        success, matrix = validate_matrix_text(text)

        self.assertTrue(success)
        self.assertEqual(
            matrix,
            [
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 0]
            ]
        )
        
     # обработка пустого файла
     def test_empty_file(self):
        success, message = validate_matrix_text("")

        self.assertFalse(success)
        self.assertEqual(message, "Файл пустой")

     # некорректные значения в матрице
     def test_invalid_values(self):
        text = (
            "0 1 10\n"
            "0 0 1\n"
            "1 0 0"
        )

        success, message = validate_matrix_text(text)

        self.assertFalse(success)
        self.assertEqual("Элемент (1,3) = '10' не 0 или 1", message)

     # матрица не квадратная
     def test_non_square_matrix(self):
        text = (
            "0 1 0 1 1\n"
            "0 0 1 0\n"
            "1 0 1 1\n"
            "0 0 0 0"
        )

        success, message = validate_matrix_text(text)

        self.assertFalse(success)
        self.assertEqual("Строка 1 имеет длину 5, ожидалось 4", message)

    # неверный формат входных данных
     def test_invalid_format(self):
        text = (
            "abcdefffdggtrtdddddddddddddd\n"
            "0 1\n"
            "1 0"
        )

        success, message = validate_matrix_text(text)

        self.assertFalse(success)
        self.assertEqual(
            message,
            "Данные в файле не в корректном формате"
        )

if __name__ == '__main__':
    unittest.main()