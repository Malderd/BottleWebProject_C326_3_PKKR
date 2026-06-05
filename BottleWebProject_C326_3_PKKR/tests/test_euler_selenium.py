import unittest
import time
import random
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TestEulerSelenium(unittest.TestCase):
    
    # Этот метод запускается один раз перед всеми тестами
    # Тут мы настраиваем браузер и создаем тестовые файлы
    @classmethod
    def setUpClass(cls):
        print("ЗАПУСК ТЕСТОВ ЭЙЛЕРОВА МАРШРУТА")
        
        # Настройки для Chrome, чтобы он работал стабильно
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # Запускаем браузер и делаем его на весь экран
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.maximize_window()
        
        # Адрес нашего сайта
        cls.base_url = "http://127.0.0.1:5555"
        # Ждем элементы до 20 секунд
        cls.wait = WebDriverWait(cls.driver, 20)
        
        # Папка для тестовых файлов
        cls.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
        cls._generate_test_files()
    
    # Генерируем файлы с матрицами для тестов, если их нет
    @classmethod
    def _generate_test_files(cls):
        """Генерация тестовых файлов с матрицами смежности."""
        os.makedirs(cls.data_dir, exist_ok=True)
        
        # Создаем файл с графом-циклом на 6 вершин
        path_cycle = os.path.join(cls.data_dir, "euler_cycle_6.txt")
        if not os.path.exists(path_cycle):
            n = 6
            matrix = [[0] * n for _ in range(n)]
            # Соединяем вершины в кольцо
            for i in range(n):
                matrix[i][(i + 1) % n] = 1
                matrix[(i + 1) % n][i] = 1
            with open(path_cycle, "w", encoding="utf-8") as f:
                for row in matrix:
                    f.write(" ".join(map(str, row)) + "\n")
            print(f"[INIT] Создан файл: {path_cycle}")
        
        # Создаем файл с графом-цепью на 5 вершин
        path_chain = os.path.join(cls.data_dir, "euler_chain_5.txt")
        if not os.path.exists(path_chain):
            n = 5
            matrix = [[0] * n for _ in range(n)]
            # Соединяем вершины в линию
            for i in range(n - 1):
                matrix[i][i + 1] = 1
                matrix[i + 1][i] = 1
            with open(path_chain, "w", encoding="utf-8") as f:
                for row in matrix:
                    f.write(" ".join(map(str, row)) + "\n")
            print(f"[INIT] Создан файл: {path_chain}")
        
        # Создаем файл с несвязным графом (две отдельные компоненты)
        path_disconnected = os.path.join(cls.data_dir, "euler_disconnected_4.txt")
        if not os.path.exists(path_disconnected):
            matrix = [
                [0, 1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 0, 1, 0],
            ]
            with open(path_disconnected, "w", encoding="utf-8") as f:
                for row in matrix:
                    f.write(" ".join(map(str, row)) + "\n")
            print(f"[INIT] Создан файл: {path_disconnected}")
        
        # Сохраняем пути к файлам для использования в тестах
        cls.file_cycle = path_cycle
        cls.file_chain = path_chain
        cls.file_disconnected = path_disconnected
    
    # Вспомогательные методы для удобства
    
    # Пауза с выводом сообщения, чтобы видеть что происходит
    def pause(self, text, sec=None):
        sec = sec or random.uniform(1.2, 2.0)
        print(f"  -> {text}")
        time.sleep(sec)
    
    # Прокрутка страницы вниз
    def scroll_down(self, y=400):
        self.driver.execute_script(f"window.scrollBy(0, {y});")
        time.sleep(1.0)
    
    # Прокрутка страницы вверх
    def scroll_up(self, y=400):
        self.driver.execute_script(f"window.scrollBy(0, -{y});")
        time.sleep(1.0)
    
    # Прокручиваем страницу так, чтобы элемент оказался по центру экрана
    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )
        time.sleep(1.0)
    
    # Открываем страницу с эйлеровым маршрутом
    def open_euler_page(self):
        self.driver.get(self.base_url + "/euler_graph")
        self.wait.until(EC.presence_of_element_located((By.ID, "btn-solve")))
        time.sleep(2)
    
    # Переключаемся между вкладками manual, random, file
    def switch_tab(self, tab_name):
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-tab="{tab_name}"]'))
        ).click()
        self.pause(f"Переключились на вкладку «{tab_name}»")
    
    # Создаем пустую матрицу заданного размера в ручном режиме
    def create_manual_matrix(self, n):
        n_input = self.wait.until(EC.presence_of_element_located((By.ID, "n-manual")))
        n_input.clear()
        time.sleep(0.8)
        n_input.send_keys(str(n))
        time.sleep(1.0)
        self.driver.find_element(By.ID, "btn-create-matrix").click()
        self.wait.until(EC.presence_of_element_located((By.ID, "matrix-table-manual")))
        self.pause(f"Матрица {n}×{n} создана")
    
    # Заполняем ячейки матрицы вручную (передаем словарь с координатами и значениями)
    def scroll_to_matrix_and_fill(self, values: dict):
        # Сначала прокручиваем к таблице
        table = self.driver.find_element(By.ID, "matrix-table-manual")
        self.scroll_to_element(table)
        time.sleep(1.0)
        
        # Находим все ячейки и заполняем нужные
        cells = self.driver.find_elements(
            By.CSS_SELECTOR, "#matrix-table-manual .matrix-cell"
        )
        for cell in cells:
            i = int(cell.get_attribute("data-i"))
            j = int(cell.get_attribute("data-j"))
            if (i, j) in values:
                self.scroll_to_element(cell)
                cell.clear()
                cell.send_keys(str(values[(i, j)]))
                # Генерируем событие change, чтобы страница поняла, что значение изменилось
                self.driver.execute_script(
                    "arguments[0].dispatchEvent(new Event('change', {bubbles: true}))",
                    cell
                )
                time.sleep(0.4)
        self.pause("Ячейки матрицы заполнены")
    
    # Заполняем большую матрицу через JavaScript (быстрее, чем через send_keys)
    def fill_matrix_via_js(self, matrix):
        table = self.driver.find_element(By.ID, "matrix-table-manual")
        self.scroll_to_element(table)
        time.sleep(1.0)
        
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                val = matrix[i][j]
                if val != 0 and i != j:
                    # Находим ячейку через JS и меняем ее значение
                    self.driver.execute_script(f"""
                        var inp = document.querySelector(
                            '#matrix-table-manual .matrix-cell[data-i="{i}"][data-j="{j}"]'
                        );
                        if (inp) {{
                            inp.value = {val};
                            inp.dispatchEvent(new Event('change', {{bubbles: true}}));
                        }}
                    """)
                    time.sleep(0.05)
    
    # Нажимаем кнопку построения графа
    def click_solve(self):
        time.sleep(1.0)
        btn = self.driver.find_element(By.ID, "btn-solve")
        self.scroll_to_element(btn)
        btn.click()
        self.pause("Нажали «Построить граф»")
    
    # Ждем появления результата и возвращаем его текст
    def wait_result(self):
        self.wait.until(EC.visibility_of_element_located((By.ID, "result-panel")))
        result_panel = self.driver.find_element(By.ID, "result-panel")
        self.scroll_to_element(result_panel)
        time.sleep(1.5)
        return self.driver.find_element(By.ID, "result-output").text
    
    # Читаем матрицу из файла для проверки
    def read_matrix_from_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        return [list(map(int, line.split())) for line in lines]
    
    # ==================== САМИ ТЕСТЫ ====================
    
    # Тест 1: проверяем, что страница открывается и содержит нужные элементы
    def test_01_open_page(self):
        print("\n[TEST 01] Открытие страницы Эйлерова маршрута")
        
        self.driver.get(self.base_url + "/euler_graph")
        time.sleep(2)
        
        # Проверяем наличие основных кнопок
        self.wait.until(EC.presence_of_element_located((By.ID, "btn-solve")))
        time.sleep(1.0)
        self.wait.until(EC.presence_of_element_located((By.ID, "btn-create-matrix")))
        time.sleep(1.0)
        self.wait.until(EC.presence_of_element_located((By.ID, "n-manual")))
        time.sleep(1.0)
        
        title = self.driver.title
        print(f"  -> Заголовок страницы: {title}")
        # Проверяем, что на странице есть слово "Эйлер"
        assert "Эйлер" in self.driver.page_source, "Страница не содержит ожидаемого заголовка"
        
        time.sleep(1.5)
        print("[OK] TEST 01 пройден")
    
    # Тест 2: проверяем переключение между вкладками
    def test_02_tab_switching(self):
        print("\n[TEST 02] Переключение вкладок (manual / random / file)")
        
        self.open_euler_page()
        
        # Переключаемся на random и проверяем
        self.switch_tab("random")
        time.sleep(1.5)
        random_tab = self.driver.find_element(By.ID, "tab-random")
        assert random_tab.is_displayed(), "Вкладка random не отображается"
        time.sleep(1.5)
        
        # Переключаемся на file и проверяем
        self.switch_tab("file")
        time.sleep(1.5)
        file_tab = self.driver.find_element(By.ID, "tab-file")
        assert file_tab.is_displayed(), "Вкладка file не отображается"
        time.sleep(1.5)
        
        # Переключаемся на manual и проверяем
        self.switch_tab("manual")
        time.sleep(1.5)
        manual_tab = self.driver.find_element(By.ID, "tab-manual")
        assert manual_tab.is_displayed(), "Вкладка manual не отображается"
        time.sleep(1.5)
        
        print("[OK] TEST 02 пройден")
    
    # Тест 3: проверяем создание матрицы вручную
    def test_03_create_matrix(self):
        print("\n[TEST 03] Создание матрицы вручную")
        
        self.open_euler_page()
        self.create_manual_matrix(4)
        
        table = self.driver.find_element(By.ID, "matrix-table-manual")
        self.scroll_to_element(table)
        time.sleep(1.5)
        
        # Проверяем, что ячеек достаточно много
        cells = table.find_elements(By.CSS_SELECTOR, ".matrix-cell")
        assert len(cells) >= 12, f"Ожидалось ≥12 ячеек матрицы, найдено: {len(cells)}"
        
        wrapper = self.driver.find_element(By.ID, "wrapper-manual")
        assert wrapper.is_displayed(), "Обёртка матрицы не отображается"
        
        time.sleep(1.5)
        print("[OK] TEST 03 пройден")
    
    # Тест 4: ручной ввод графа, который должен дать эйлеров цикл
    def test_04_manual_euler_cycle(self):
        print("\n[TEST 04] Ручной ввод — Эйлеров цикл (4 вершины)")
        
        self.open_euler_page()
        self.create_manual_matrix(4)
        
        # Создаем цикл 0-1-2-3-0 (все степени = 2)
        edges = {
            (0, 1): 1, (1, 0): 1,
            (1, 2): 1, (2, 1): 1,
            (2, 3): 1, (3, 2): 1,
            (0, 3): 1, (3, 0): 1,
        }
        self.scroll_to_matrix_and_fill(edges)
        time.sleep(1.5)
        self.click_solve()
        
        result = self.wait_result()
        print(f"  -> Результат: {result[:200]}")
        # Проверяем, что в ответе есть слова "Эйлеров цикл" или "cycle"
        assert "Эйлеров цикл" in result or "cycle" in result.lower(), \
            f"Ожидался Эйлеров цикл, получено: {result}"
        
        time.sleep(1.5)
        print("[OK] TEST 04 пройден")
    
    # Тест 5: ручной ввод графа, который должен дать эйлерову цепь
    def test_05_manual_euler_chain(self):
        print("\n[TEST 05] Ручной ввод — Эйлерова цепь (4 вершины)")
        
        self.open_euler_page()
        self.create_manual_matrix(4)
        
        # Создаем путь 0-1-2-3 (вершины 0 и 3 имеют нечетную степень)
        edges = {
            (0, 1): 1, (1, 0): 1,
            (1, 2): 1, (2, 1): 1,
            (2, 3): 1, (3, 2): 1,
        }
        self.scroll_to_matrix_and_fill(edges)
        time.sleep(1.5)
        self.click_solve()
        
        result = self.wait_result()
        print(f"  -> Результат: {result[:200]}")
        assert "Эйлерова цепь" in result or "path" in result.lower(), \
            f"Ожидалась Эйлерова цепь, получено: {result}"
        
        time.sleep(1.5)
        print("[OK] TEST 05 пройден")
    
    # Тест 6: ручной ввод несвязного графа (должна быть ошибка)
    def test_06_manual_disconnected_graph(self):
        print("\n[TEST 06] Ручной ввод — несвязный граф")
        
        self.open_euler_page()
        self.create_manual_matrix(4)
        
        # Две отдельные компоненты: 0-1 и 2-3
        edges = {
            (0, 1): 1, (1, 0): 1,
            (2, 3): 1, (3, 2): 1,
        }
        self.scroll_to_matrix_and_fill(edges)
        time.sleep(1.5)
        self.click_solve()
        
        result = self.wait_result()
        print(f"  -> Результат: {result[:200]}")
        # Ожидаем сообщение о несвязности графа
        assert (
            "не связный" in result
            or "несвязн" in result
            or "disconnected" in result.lower()
            or "не существует" in result
        ), f"Ожидалось сообщение о несвязности, получено: {result}"
        
        time.sleep(1.5)
        print("[OK] TEST 06 пройден")
    
    # Тест 7: генерация случайного графа
    def test_07_random_graph(self):
        print("\n[TEST 07] Случайный граф")
        
        self.open_euler_page()
        self.switch_tab("random")
        time.sleep(1.5)
        
        # Вводим параметры: 6 вершин, плотность 70%
        n_input = self.driver.find_element(By.ID, "n-random")
        self.scroll_to_element(n_input)
        n_input.clear()
        time.sleep(0.8)
        n_input.send_keys("6")
        time.sleep(1.0)
        
        density_input = self.driver.find_element(By.ID, "density")
        self.scroll_to_element(density_input)
        density_input.clear()
        time.sleep(0.8)
        density_input.send_keys("70")
        self.pause("Параметры введены: N=6, плотность=70%")
        
        # Генерируем матрицу
        self.driver.find_element(By.ID, "btn-random").click()
        self.pause("Матрица сгенерирована")
        
        self.wait.until(EC.visibility_of_element_located((By.ID, "wrapper-random")))
        random_table = self.driver.find_element(By.ID, "matrix-table-random")
        self.scroll_to_element(random_table)
        time.sleep(1.5)
        
        assert random_table.is_displayed(), "Таблица случайной матрицы не отображается"
        
        self.click_solve()
        
        result = self.wait_result()
        assert result.strip(), "Панель результатов пуста"
        print(f"  -> Результат: {result[:200]}")
        
        time.sleep(1.5)
        print("[OK] TEST 07 пройден")
    
    # Тест 8: загрузка файла с графом-циклом
    def test_08_file_upload_cycle(self):
        print("\n[TEST 08] Загрузка файла — Эйлеров цикл (6 вершин)")
        
        self.open_euler_page()
        self.switch_tab("file")
        time.sleep(1.5)
        
        # Загружаем файл
        file_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "file-input"))
        )
        time.sleep(1.0)
        file_input.send_keys(self.file_cycle)
        self.pause(f"Файл загружен: {os.path.basename(self.file_cycle)}")
        
        self.wait.until(EC.visibility_of_element_located((By.ID, "wrapper-file")))
        file_table = self.driver.find_element(By.ID, "matrix-table-file")
        self.scroll_to_element(file_table)
        self.pause("Матрица из файла отображена")
        
        self.click_solve()
        
        result = self.wait_result()
        print(f"  -> Результат: {result[:200]}")
        assert "Эйлеров цикл" in result or "cycle" in result.lower(), \
            f"Ожидался Эйлеров цикл, получено: {result}"
        
        time.sleep(1.5)
        print("[OK] TEST 08 пройден")
    
    # Тест 9: загрузка файла с графом-цепью
    def test_09_file_upload_chain(self):
        print("\n[TEST 09] Загрузка файла — Эйлерова цепь (5 вершин)")
        
        self.open_euler_page()
        self.switch_tab("file")
        time.sleep(1.5)
        
        file_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "file-input"))
        )
        time.sleep(1.0)
        file_input.send_keys(self.file_chain)
        self.pause(f"Файл загружен: {os.path.basename(self.file_chain)}")
        
        self.wait.until(EC.visibility_of_element_located((By.ID, "wrapper-file")))
        file_table = self.driver.find_element(By.ID, "matrix-table-file")
        self.scroll_to_element(file_table)
        time.sleep(1.5)
        
        self.click_solve()
        
        result = self.wait_result()
        print(f"  -> Результат: {result[:200]}")
        assert "Эйлерова цепь" in result or "path" in result.lower(), \
            f"Ожидалась Эйлерова цепь, получено: {result}"
        
        time.sleep(1.5)
        print("[OK] TEST 09 пройден")
    
    # Тест 10: проверка кнопки сохранения результатов
    def test_10_save_results(self):
        print("\n[TEST 10] Сохранение результатов")
        
        self.open_euler_page()
        self.create_manual_matrix(3)
        
        # Полный граф K3 (треугольник) - эйлеров цикл
        edges = {
            (0, 1): 1, (1, 0): 1,
            (1, 2): 1, (2, 1): 1,
            (0, 2): 1, (2, 0): 1,
        }
        self.scroll_to_matrix_and_fill(edges)
        time.sleep(1.5)
        self.click_solve()
        self.wait_result()
        time.sleep(1.5)
        
        # Нажимаем кнопку сохранения
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-save"))
        )
        self.scroll_to_element(save_btn)
        time.sleep(1.0)
        save_btn.click()
        self.pause("Нажали кнопку «Сохранить»")
        
        print("[OK] TEST 10 пройден")
    
    # Тест 11: проверка кнопки очистки матрицы
    def test_11_clear_matrix(self):
        print("\n[TEST 11] Очистка матрицы")
        
        self.open_euler_page()
        self.create_manual_matrix(3)
        
        table = self.driver.find_element(By.ID, "matrix-table-manual")
        self.scroll_to_element(table)
        time.sleep(1.0)
        
        # Заполняем несколько ячеек
        cells = self.driver.find_elements(
            By.CSS_SELECTOR, "#matrix-table-manual .matrix-cell"
        )
        for cell in cells[:4]:
            if cell.is_enabled():
                self.scroll_to_element(cell)
                cell.clear()
                cell.send_keys("1")
                self.driver.execute_script(
                    "arguments[0].dispatchEvent(new Event('change', {bubbles: true}))", cell
                )
                time.sleep(0.4)
        self.pause("Несколько ячеек заполнено")
        
        # Очищаем матрицу
        clear_btn = self.driver.find_element(By.ID, "btn-clear-matrix")
        self.scroll_to_element(clear_btn)
        time.sleep(1.0)
        clear_btn.click()
        self.pause("Нажали «Очистить»")
        
        # Панель результатов должна скрыться
        result_panel = self.driver.find_element(By.ID, "result-panel")
        display = result_panel.value_of_css_property("display")
        assert display == "none", \
            f"Панель результатов должна быть скрыта (display: none), но display = {display}"
        
        time.sleep(1.5)
        print("[OK] TEST 11 пройден")
    
    # Тест 12: проверка очистки на файловой вкладке
    def test_12_clear_file(self):
        print("\n[TEST 12] Очистка файловой вкладки")
        
        self.open_euler_page()
        self.switch_tab("file")
        time.sleep(1.5)
        
        # Загружаем файл
        file_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "file-input"))
        )
        time.sleep(1.0)
        file_input.send_keys(self.file_cycle)
        self.wait.until(EC.visibility_of_element_located((By.ID, "wrapper-file")))
        
        file_table = self.driver.find_element(By.ID, "matrix-table-file")
        self.scroll_to_element(file_table)
        self.pause("Файл загружен, матрица отображена")
        
        # Очищаем
        clear_btn = self.driver.find_element(By.ID, "btn-clear-file")
        self.scroll_to_element(clear_btn)
        time.sleep(1.0)
        clear_btn.click()
        self.pause("Нажали «Очистить» на вкладке файла")
        
        # Обертка с матрицей должна скрыться
        wrapper = self.driver.find_element(By.ID, "wrapper-file")
        display = wrapper.value_of_css_property("display")
        assert display == "none", \
            f"Обёртка матрицы файла должна скрыться после очистки, но display = {display}"
        
        time.sleep(1.5)
        print("[OK] TEST 12 пройден")
    
    # Тест 13: проверка работы с большой матрицей через JS
    def test_13_big_matrix_js_fill(self):
        print("\n[TEST 13] Большая матрица 15×15 — заполнение через JS")
        
        self.open_euler_page()
        
        # Создаем матрицу 15x15 в виде цикла
        n = 15
        big = [[0] * n for _ in range(n)]
        for i in range(n):
            big[i][(i + 1) % n] = 1
            big[(i + 1) % n][i] = 1
        
        self.create_manual_matrix(n)
        time.sleep(1.5)
        
        # Замеряем время заполнения через JS
        t0 = time.time()
        self.fill_matrix_via_js(big)
        print(f"  -> JS-заполнение: {time.time() - t0:.2f} сек")
        time.sleep(2)
        
        self.click_solve()
        
        result = self.wait_result()
        print(f"  -> Результат: {result[:200]}")
        assert "Эйлеров цикл" in result or "cycle" in result.lower(), \
            f"Ожидался Эйлеров цикл, получено: {result}"
        
        time.sleep(1.5)
        print("[OK] TEST 13 пройден")
    
    # Тест 14: проверка производительности (время выполнения не более 10 секунд)
    def test_14_performance(self):
        print("\n[TEST 14] Тест производительности (15 вершин, доп. рёбра)")
        
        self.open_euler_page()
        
        # Создаем граф на 15 вершинах с дополнительными ребрами
        n = 15
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            matrix[i][(i + 1) % n] = 1
            matrix[(i + 1) % n][i] = 1
        extra = [(0, 4), (1, 7), (2, 8), (3, 9), (5, 11), (6, 12)]
        for a, b in extra:
            matrix[a][b] = 1
            matrix[b][a] = 1
        
        self.create_manual_matrix(n)
        time.sleep(1.5)
        self.fill_matrix_via_js(matrix)
        time.sleep(2)
        
        # Замеряем время поиска маршрута
        t0 = time.time()
        self.click_solve()
        self.wait_result()
        elapsed = time.time() - t0
        
        print(f"  -> Время поиска маршрута: {elapsed:.2f} сек")
        assert elapsed < 10.0, f"Поиск занял слишком много времени: {elapsed:.2f} сек"
        
        time.sleep(1.5)
        print("[OK] TEST 14 пройден")
    
    # Тест 15: пустой граф без ребер
    def test_15_empty_graph(self):
        print("\n[TEST 15] Пустой граф — нет рёбер")
        
        self.open_euler_page()
        self.create_manual_matrix(3)
        
        table = self.driver.find_element(By.ID, "matrix-table-manual")
        self.scroll_to_element(table)
        time.sleep(1.5)
        
        # Просто нажимаем "построить граф" без заполнения ребер
        self.click_solve()
        
        result = self.wait_result()
        print(f"  -> Результат: {result[:200]}")
        # Проверяем, что результат не пустой (какое-то сообщение есть)
        assert result.strip(), "Панель результатов пуста — ожидалось какое-либо сообщение"
        
        time.sleep(1.5)
        print("[OK] TEST 15 пройден")
    
    # Закрываем браузер после всех тестов
    @classmethod
    def tearDownClass(cls):
        print("\nЗакрытие браузера")
        time.sleep(2)
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)