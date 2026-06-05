import unittest
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin


class TestCliquesSelenium(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("ЗАПУСК ТЕСТОВ ПС")
        cls.driver = webdriver.Edge() # Инициализация браузера
        cls.driver.maximize_window() # Разворачиваем окно на весь экран
        cls.base_url = "http://127.0.0.1:5555" # Наш url
        cls.wait = WebDriverWait(cls.driver, 10) # Используется для ожидания загрузки элементов

    # Прокрутка вниз для ввода параметров
    def scroll_up(self, y=230):
        hero = self.driver.find_element(By.CLASS_NAME, "hero-cliques")
        origin = ScrollOrigin.from_element(hero) # Начинаем скрол от элемента
        ActionChains(self.driver).scroll_from_origin(origin, 0, y).perform() # Скролл на y пикселей
        time.sleep(1.5)
 
    # Прокрутка вниз для результатов
    def scroll_down(self, y=250):
        hero = self.driver.find_element(By.CLASS_NAME, "hero-cliques")
        origin = ScrollOrigin.from_element(hero)
        ActionChains(self.driver).scroll_from_origin(origin, 0, y).perform()
        time.sleep(1.5)
 
    # Прокрутка вверх
    def scroll_back(self, y=250):
        hero = self.driver.find_element(By.CLASS_NAME, "hero-cliques")
        origin = ScrollOrigin.from_element(hero)
        ActionChains(self.driver).scroll_from_origin(origin, 0, -y).perform() # -y
        time.sleep(1.5)

    # ПС-01, переход с главной на собственную страничку
    def test_1_open_page(self):
        print("\n[TEST 1] Старт с главной страницы")
        self.driver.get(self.base_url) # Главная страница
        time.sleep(1)
        self.driver.get(self.base_url + "/clique_detection?tab=manual") # Переход на нашу страницу
        time.sleep(1)
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("\nTEST 1 пройден") # Информация в консоль об успехе

    # ПС-02, случайный граф, его отрисовка и сохранение
    def test_2_random_generation(self):
        print("\n[TEST 2] RANDOM сценарий")
        self.driver.get(self.base_url + "/clique_detection?tab=random")
        time.sleep(1)
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
        time.sleep(1)

        btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-create-matrix"))
        )
        btn.click() # Создаём матрицу нажатием на кнопку
        time.sleep(1)

        self.wait.until(
            EC.presence_of_element_located((By.ID, "matrix-form")) # Ждём появления матрицы на странице
        )

        solve_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-solve"))
        )
        time.sleep(1)
        solve_btn.click() # Строим граф нажатием кнопки

        time.sleep(1)
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".graph-image")) # Ждём появления изображения на странице
        )
        self.scroll_down() # Скролл вниз, для просмотра результата
        
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-save"))
        )
        self.scroll_back() # Скролл вверх
        time.sleep(1)
        save_btn.click() # Сохранение

        time.sleep(1)
        print("TEST 2 пройден")

    # ПС-03, выгрузка из файла + построение графа
    def test_3_file_upload(self):
        print("\n[TEST 3] FILE сценарий")
        self.driver.get(self.base_url + "/clique_detection?tab=file")
        time.sleep(1)

        # Неверный файл
        error_file = os.path.abspath("./tests/test_data/error.txt") 

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
        true_file = os.path.abspath("./tests/test_data/true_matrix.txt") 

        file_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "file-input"))
        )

        file_input.send_keys(true_file)

        upload_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-upload"))
        )

        upload_btn.click()

        time.sleep(2)

        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "matrix-table")) # Ждём появления матрицы на странице
        )

        solve_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-solve"))
        )
        time.sleep(1)
        solve_btn.click() # Построение графа

        time.sleep(1)
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