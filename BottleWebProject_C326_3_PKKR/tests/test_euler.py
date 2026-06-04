import unittest
from io import BytesIO

# Импортируем тестируемые функции валидации из модуля validations.valid_euler
from validations.valid_euler import (
    validation_euler,
    validation_random_params,
    validation_and_parse_file
)


class MockUploadFile:
    def __init__(self, content: str):
        # Преобразуем строку в байтовый поток, имитируя чтение файла
        self.file = BytesIO(content.encode("utf-8"))


class TestEulerValidation(unittest.TestCase):
    #Тестирование функции проверки матрицы смежности графа (validation_euler)

    def test_validation_euler_ok(self):
        #Проверка корректной матрицы смежности для простого неориентированного графа
        matrix = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]

        # Вызов тестируемой функции
        valid, err = validation_euler(matrix)

        # Проверка ожидаемого успешного результата
        self.assertTrue(valid)
        self.assertIsNone(err)

    def test_validation_euler_empty(self):
        #Проверка пустой матрицы (передан пустой список)
        valid, err = validation_euler([])

        # Ожидаем ошибку валидации
        self.assertFalse(valid)
        self.assertIsNotNone(err)

    def test_validation_euler_not_square(self):
        #Проверка неквадратной матрицы (количество строк не равно количеству столбцов)
        matrix = [
            [0, 1],
            [1, 0],
            [0, 1]
        ]

        valid, err = validation_euler(matrix)

        self.assertFalse(valid)
        self.assertIsNotNone(err)

    def test_validation_euler_loop(self):
        #Проверка матрицы, содержащей петлю (единица на главной диагонали)
        matrix = [
            [1, 0],
            [0, 0]
        ]

        valid, err = validation_euler(matrix)

        self.assertFalse(valid)
        self.assertIsNotNone(err)

    def test_validation_euler_bad_value(self):
        #Проверка матрицы с недопустимыми значениями 
        matrix = [
            [0, 2],
            [2, 0]
        ]

        valid, err = validation_euler(matrix)

        self.assertFalse(valid)
        self.assertIsNotNone(err)

    def test_validation_euler_not_symmetric(self):
        #Проверка несимметричной матрицы (граф должен быть неориентированным, а тут ориентированное ребро)
        matrix = [
            [0, 1],
            [0, 0]
        ]

        valid, err = validation_euler(matrix)

        self.assertFalse(valid)
        self.assertIsNotNone(err)
    def test_validation_euler_negative_value(self):
    # Отрицательные значения
        matrix = [
            [0, -1],
            [-1, 0]
        ]
        valid, err = validation_euler(matrix)
        self.assertFalse(valid)


class TestRandomParamsValidation(unittest.TestCase):
    #Тестирование функции проверки параметров генерации случайного графа (validation_random_params)

    def test_random_params_ok(self):
        #Проверка с корректными строковыми параметрами (количество вершин и плотность)
        valid, n, density, err = validation_random_params("5", "50")

        # Ожидаем успешную валидацию и корректное приведение типов к int
        self.assertTrue(valid)
        self.assertEqual(n, 5)
        self.assertEqual(density, 50)
        self.assertIsNone(err)

    def test_random_params_bad_n(self):
        #Проверка некорректного количества вершин (например, слишком мало для создания графа)
        valid, n, density, err = validation_random_params("1", "50")

        self.assertFalse(valid)
        self.assertIsNone(n)
        self.assertIsNotNone(err)

    def test_random_params_bad_density(self):
        #Проверка некорректного значения плотности графа (выход за пределы диапазона, например > 100%)
        valid, n, density, err = validation_random_params("5", "200")

        self.assertFalse(valid)
        self.assertIsNone(n)
        self.assertIsNotNone(err)

    def test_random_params_not_number(self):
        #Проверка передачи строк, которые невозможно преобразовать в числа
        valid, n, density, err = validation_random_params("abc", "xyz")

        self.assertFalse(valid)
        self.assertIsNone(n)
        self.assertIsNone(density)
        self.assertIsNotNone(err)


class TestFileValidation(unittest.TestCase):
    #Тестирование функции загрузки, парсинга и валидации матрицы из файла (validation_and_parse_file)

    def test_file_ok(self):
        #Проверка успешного парсинга файла с корректно отформатированной матрицей
        # Создаем mock-файл с правильным содержимым
        file = MockUploadFile(
            """0 1 0
               1 0 1
               0 1 0"""
        )

        valid, matrix, err = validation_and_parse_file(file)

        # Ожидаем успешный парсинг и проверку размера полученной матрицы
        self.assertTrue(valid)
        self.assertEqual(len(matrix), 3)
        self.assertIsNone(err)

    def test_file_none(self):
        #Проверка ситуации, когда файл вообще не был передан (None)
        valid, matrix, err = validation_and_parse_file(None)

        self.assertFalse(valid)
        self.assertIsNone(matrix)
        self.assertIsNotNone(err)

    def test_file_not_numbers(self):
        #Проверка файла, содержащего недопустимые символы (буквы вместо цифр)
        file = MockUploadFile(
            """0 1 a
               1 0 1
               0 1 0"""
        )

        valid, matrix, err = validation_and_parse_file(file)

        self.assertFalse(valid)
        self.assertIsNone(matrix)
        self.assertIsNotNone(err)

    def test_file_not_square(self):
        #Проверка файла, где текстовое представление матрицы не является квадратным
        file = MockUploadFile(
            """0 1
               1 0
               0 1"""
        )

        valid, matrix, err = validation_and_parse_file(file)

        self.assertFalse(valid)
        self.assertIsNone(matrix)
        self.assertIsNotNone(err)

    def test_file_empty(self):
        #Проверка загрузки абсолютно пустого файла
        file = MockUploadFile("")

        valid, matrix, err = validation_and_parse_file(file)

        self.assertFalse(valid)
        self.assertIsNone(matrix)
        self.assertIsNotNone(err)

    def test_validation_euler_not_connected(self):
        matrix = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ]

        valid, err = validation_euler(matrix)

        self.assertFalse(valid)
        self.assertIsNotNone(err)
        self.assertIn("несвязен", err["message"])

    # Граф связен, но содержит изолированную вершину без ребер (это допустимо для Эйлера!)
    def test_validation_euler_connected_with_isolated_vertex(self):
        matrix = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0]  # Вершина 3 вообще без ребер
        ]

        valid, err = validation_euler(matrix)

        self.assertTrue(valid)
        self.assertIsNone(err)


# Точка входа для запуска тестов из консоли
if __name__ == '__main__':
    unittest.main()
