import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

class TestKosarayuSelenium(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Edge() # Запуск браузера Microsoft Edge
        cls.driver.maximize_window() # Разворачиваем окно на весь экран
        cls.base_url = "http://127.0.0.1:5555"
        cls.wait = WebDriverWait(cls.driver, 10) # Используется для ожидания загрузки элементов

    # Прокрутка вниз для ввода параметров
    def scroll_to(self, y=230):
        page = self.driver.find_element(By.CLASS_NAME, "components_of_strong_connectivity")
        self.driver.execute_script("arguments[0].scrollTop += arguments[1];", page, y)
        time.sleep(1)

    # Прокрутка вниз для результатов
    def scroll_down(self, y=250):
        page = self.driver.find_element(By.CLASS_NAME, "components_of_strong_connectivity")
        self.driver.execute_script("arguments[0].scrollTop += arguments[1];", page, y)
        time.sleep(1)

    # Прокрутка вверх
    def scroll_back(self, y=250):
        page = self.driver.find_element(By.CLASS_NAME, "components_of_strong_connectivity")
        self.driver.execute_script(
        "arguments[0].scrollTop -= arguments[1];",
         page, y
        )  
        time.sleep(1)

    # Ожидание
    def pause(self, sec=None):
        sec = sec or random.uniform(1,2)
        time.sleep(sec)

    # Тест 1: переход с главной на собственную страничку
    def test_open_page(self):
        print("\nЗапуск TEST 1")
        self.driver.get(self.base_url) # Главная страница
        kosarayu_link = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/kosarayu_algorithm"]'))
        )
        self.pause()
        kosarayu_link.click() # переход на собственную страницу через хедер сайта
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("TEST 1 пройден")

    # Тест 2: случайный граф, его отрисовка и сохранение
    def test_random_generation(self):
        print("\nЗапуск TEST 2")
        self.driver.get(self.base_url + "/kosarayu_algorithm")
        self.pause()
        self.scroll_to() # Скролл вниз
        n_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "sizeInput")) # Нахождение поля по id в html
        )
        
        # Ввод данных
        n_input.send_keys("14")
        self.pause()

        btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "createMatrixButton"))
        )
        btn.click() # Создаём матрицу нажатием на кнопку
        self.pause()

        self.wait.until(
            EC.presence_of_element_located((By.ID, "matrixTable")) # Ждём появления матрицы на странице
        )

        generate_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "generateButton"))
        )
        generate_btn.click() # Рандомно заполняем матрицу
        self.pause()

        solve_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "findComponentsButton"))
        )
        self.pause()
        solve_btn.click() # Строим граф нажатием кнопки

        self.pause()
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".graph-image")) # Ждём появления изображения на странице
        )
        self.scroll_down() # Скролл вниз, для просмотра результата
        
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "saveButton"))
        )
        self.scroll_back() # Скролл вверх
        self.pause()
        save_btn.click() # Сохранение

        self.pause()
        print("TEST 2 пройден")

    # Тест 3: заполнение матрицы смежности вручную
    def test_manual_matrix_input(self):
        print("\nЗапуск TEST 3")
        self.driver.get(self.base_url + "/kosarayu_algorithm")
        self.pause()

        self.scroll_to()
        n_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "sizeInput")) # Нахождение поля по id в html
        )
        
        # Ввод данных
        n_input.send_keys("14")
        self.pause()

        btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "createMatrixButton"))
        )
        btn.click() # Создаём матрицу нажатием на кнопку
        self.pause()

        self.wait.until(
            EC.presence_of_element_located((By.ID, "matrixTable")) # Ждём появления матрицы на странице
        )
        matrix = [
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        for i in range(len(matrix)):
            for j in range(len(matrix)):

                if i == j:
                    continue

                if matrix[i][j] == 1:

                    checkbox = self.driver.find_element(
                        By.NAME,
                        f"cell_{i}_{j}"
                    )

                    checkbox.click()

        solve_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "findComponentsButton"))
        )
        self.pause()
        solve_btn.click() # Строим граф нажатием кнопки

        self.pause()
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".graph-image")) # Ждём появления изображения на странице
        )

        self.scroll_down()
        print("TEST 3 пройден")

    # Тест 4: выгрузка из файла + построение графа
    def test_correct_file_upload(self):
        print("\nЗапуск TEST 4")
        self.driver.get(self.base_url + "/kosarayu_algorithm")
        self.pause()

        file_path = r"C:\Users\rozhi\Downloads\abr.txt" # Выбранный файл

        file_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "matrix_file"))
        )
        file_input.send_keys(file_path) # Загрузили файл в форму
        self.pause()

        self.wait.until(
            EC.presence_of_element_located((By.ID, "matrixTable")) # Ждём появления матрицы на странице
        )

        solve_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "findComponentsButton"))
        )
        self.pause()
        solve_btn.click() # Строим граф нажатием кнопки

        self.pause()
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".graph-image")) # Ждём появления изображения на странице
        )
        self.scroll_down()
        
        print("TEST 4 пройден")

    # Тест 5: загрузка некорректного файла, просмотр ошибки
    def test_uncorrect_file_upload(self):
        print("\nЗапуск TEST 5")
        self.driver.get(self.base_url + "/kosarayu_algorithm")
        self.pause()

        file_path = r"C:\Users\rozhi\Downloads\table.txt"

        file_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "matrix_file"))
        )
        file_input.send_keys(file_path) # Загрузили файл в форму
        self.pause()

        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-box")) # Ждём появления ошибки на странице
        )

        self.scroll_down()
        
        print("TEST 5 пройден")

    @classmethod
    def tearDownClass(cls):
        print("\nЗакрытие браузера")
        time.sleep(2)
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()