import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCliquesSelenium(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("ЗАПУСК ТЕСТОВ ПС")
        cls.driver = webdriver.Chrome() # Инициализация браузера Chrome
        cls.driver.maximize_window() # Разворачиваем окно на весь экран
        cls.base_url = "http://127.0.0.1:5555" # Наш url
        cls.wait = WebDriverWait(cls.driver, 10) # Используется для ожидания загрузки элементов

    # Прокрутка вниз для ввода параметров
    def scroll_up(self, y=230):
        hero = self.driver.find_element(By.CLASS_NAME, "hero-cliques")
        self.driver.execute_script("arguments[0].scrollTop += arguments[1];", hero, y)
        time.sleep(1.5)

    # Прокрутка вниз для результатов
    def scroll_down(self, y=250):
        hero = self.driver.find_element(By.CLASS_NAME, "hero-cliques")
        self.driver.execute_script("arguments[0].scrollTop += arguments[1];", hero, y)
        time.sleep(1.5)

    # Прокрутка вверх
    def scroll_back(self, y=250):
        hero = self.driver.find_element(By.CLASS_NAME, "hero-cliques")
        self.driver.execute_script(
        "arguments[0].scrollTop -= arguments[1];", # -y
         hero, y
        )  
        time.sleep(1.5)

    # Ожидание
    def pause(self, text, sec=None):
        sec = sec or random.uniform(1,2)
        print(text)
        time.sleep(sec)

    # ПС-01, переход с главной на собственную страничку
    def test_1_open_page(self):
        print("\n[TEST 1] Старт с главной страницы")
        self.driver.get(self.base_url) # Главная страница
        self.pause("[TEST 1] Ждём главную страницу")
        self.driver.get(self.base_url + "/clique_detection?tab=manual") # Переход на нашу страницу
        self.pause("[TEST 1] Переход на manual")
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("TEST 1 пройден") # Информация в консоль об успехе

    # ПС-02, случайный граф, его отрисовка и сохранение
    def test_2_random_generation(self):
        print("\n[TEST 2] RANDOM сценарий")
        self.driver.get(self.base_url + "/clique_detection?tab=random")
        self.pause("[TEST 2] Открыли random")
        self.scroll_up() # Скролл вниз
        n_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "n_size")) # Нахождение поля по имени в html
        )
        density_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "density"))
        )
        
        # Ввод данных
        n_input.send_keys("5")
        density_input.send_keys("60")
        self.pause("[TEST 2] Ввели данные")

        btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-create-matrix"))
        )
        btn.click() # Создаём матрицу нажатием на кнопку
        self.pause("[TEST 2] Сгенерировали матрицу")

        self.wait.until(
            EC.presence_of_element_located((By.ID, "matrix-form")) # Ждём появления матрицы на странице
        )

        solve_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-solve"))
        )
        self.pause("[TEST 2] Жмём построить граф")
        solve_btn.click() # Строим граф нажатием кнопки

        self.pause("[TEST 2] Ждём граф")
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".graph-image")) # Ждём появления изображения на странице
        )
        self.scroll_down() # Скролл вниз, для просмотра результата
        
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-save"))
        )
        self.scroll_back() # Скролл вверх
        self.pause("[TEST 2] Жмём сохранить")
        save_btn.click() # Сохранение

        self.pause("[TEST 2] Готово")
        print("TEST 2 пройден")

    # ПС-03, выгрузка из файла + построение графа
    def test_3_file_upload(self):
        print("\n[TEST 3] FILE сценарий")
        self.driver.get(self.base_url + "/clique_detection?tab=file")
        self.pause("[TEST 3] Открыли file вкладку")

        # Неверный файл
        error_file = r"C:\Users\annak\OneDrive\Рабочий стол\error.txt"

        file_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "file-input"))
        )

        file_input.send_keys(error_file)

        upload_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-upload"))
        )

        upload_btn.click()  # Пытаемся загрузить неверный файл

        time.sleep(2)

        # Нажимаем "Очистить"
        clear_btn = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "clear"))
        )

        clear_btn.click()

        time.sleep(2)

        # Загружаем правильный файл
        true_file = r"C:\Users\annak\OneDrive\Рабочий стол\true_matrix.txt"

        file_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "file-input"))
        )

        file_input.send_keys(true_file)

        upload_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-upload"))
        )

        upload_btn.click()

        time.sleep(2)
        self.pause("[TEST 3] Загрузили матрицу")

        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "matrix-table")) # Ждём появления матрицы на странице
        )

        solve_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-solve"))
        )
        self.pause("[TEST 3] Строим граф")
        solve_btn.click() # Построение графа

        self.pause("[TEST 3] Ждём результат")
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".graph-image")) # Ждём появления изображения на странице
        )

        self.scroll_down() # Скролл вниз для результата
        print("TEST 3 пройден")

    @classmethod
    def tearDownClass(cls):
        print("\nЗакрытие браузера")
        time.sleep(2)
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()