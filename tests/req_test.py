from selenium.common.exceptions import NoSuchElementException
from tests.page_object import ToDoPage

todo_titles = ["TODO #1 get job in BI.ZONE", "TODO #2 learn about the PageObject pattern", "TODO #3 make a test task"]


class TestReq(ToDoPage):
    def test_header(self):
        """
        Тест на отсутствие верхнего колонтитула("шапки") сайта
            Предварительноы условия:
        -отсутствуют
            Шаги:
        1. Открыть браузер и перейдите главную страницу.
            Ожидаемый результат:
        1. На странице должен отсутствовать верхний колонтитул сайта.
        """
        element = None
        try:
            element = self.driver.find_element_by_xpath("/html/body/section/div/section")
        except NoSuchElementException:
            pass
        assert element is None

    def test_footer(self):
        """
        Тест на отсутствие нижнего колонтитула сайта
            Предварительноы условия:
        -отсутствуют
            Шаги:
        1. Открыть браузер и перейдите главную страницу.
            Ожидаемый результат:
        1. На странице должен отсутствовать нижний колонтитул сайта.
        """
        element = None
        try:
            element = self.driver.find_element_by_xpath("/html/body/section/div/footer")
        except NoSuchElementException:
            pass
        assert element is None

    def test_create_todo_input_focus(self):
        """
        Тест на присутствие фокуса на поле ввода новой задачи
            Предварительноы условия:
        -отсутствуют
            Шаги:
        1. Открыть браузер и перейдите главную страницу.
            Ожидаемый результат:
        1. Фокус
        """
        todo_input = self.get_todo_input()
        assert todo_input == self.driver.switch_to.active_element

    def test_item_add_to_list(self):
        """
        Тест на возможность создания to-do
            Предварительноы условия:
        1. Список to-do пуст.
            Шаги:
        1. Открыть браузер и перейдите главную страницу.
        2. Ввести заголовок новой задачи.
        3. Нажать клавишу ВВОД.

            Ожидаемый результат:
        1. Новая задача существует в списке всех задач.
        2. Новая задача существует в списке активных задач.
        """
        self.create_todo(todo_titles[0])
        assert self.check_todo_exist(todo_titles[0]) is True
        self.move_to("#/active")
        assert self.check_todo_exist(todo_titles[0]) is True

    def test_two_items_add_to_list(self):
        """
        Тест на возможность создания нескольких to-do
            Предварительноы условия:
        1. Список to-do пуст.
            Шаги:
        1. Открыть браузер и перейти на главную страницу.
        3. Ввести заголовок задачи #1.
        4. Нажать клавишу ВВОД.
        5. Ввести заголовок задачи #2.
        6. Нажать клавишу ВВОД.

            Ожидаемый результат:
        1. Новые задачи существуют в списке всех задач.
        2. Новые задачи существуют в списке активных задач.
        3. Новые задачи отсутствуют в списке завершенных задач.
        """
        self.create_todo(todo_titles[0])
        self.create_todo(todo_titles[1])
        assert self.check_todo_exist(todo_titles[0]) is True
        assert self.check_todo_exist(todo_titles[1]) is True
        self.move_to("#/active")
        assert self.check_todo_exist(todo_titles[0]) is True
        assert self.check_todo_exist(todo_titles[1]) is True
        self.move_to("#/completed")
        assert self.check_todo_exist(todo_titles[0]) is False
        assert self.check_todo_exist(todo_titles[1]) is False

    def test_delete_item_from_list(self):
        """
        Тест на возможность удаления to-do
            Предварительноы условия:
        1. В списке to-do находится 2 задачи.
            Шаги:
        1. Открыть браузер и перейти на главную страницу.
        2. Навести указатель мыши на активную задачу. Должна появится кнопка «х».
        3. Нажать на кнопку «х».
            Ожидаемый результат:
        1. Удаленная задача отсутствует в списке всех задач.
        2. Удаленная задача отсутствует в списке активных задач.
        3. Удаленная задача отсутствует в списке завершенных задач.
        """
        self.create_todo(todo_titles[0])
        self.create_todo(todo_titles[1])
        assert self.check_todo_exist(todo_titles[0]) is True
        assert self.check_todo_exist(todo_titles[1]) is True
        self.delete_todo(todo_titles[0])
        assert self.check_todo_exist(todo_titles[0]) is False
        self.move_to("#/active")
        assert self.check_todo_exist(todo_titles[0]) is False
        self.move_to("#/completed")
        assert self.check_todo_exist(todo_titles[0]) is False

    def test_todo_counter(self):
        """
        Тест проверки счетчика невыполненных to-do
            Предварительное условие:
        1. Список задач состоит из 1 активной задачи.
        2. Счетчик задач находится в состоянии "1 item left"
            Шаги:
        1. Открыть браузер и перейти на главную страницу.
        2. Отметить задачу #1 как выполненную
        3. Добавить задачу #2
        4. Добавить задачу #3
            Ожидаемый результат:
        1. Изменение счетчика невыполненных задач в соответствии:
        - 1 выполненная задача : "0 items left"
        - 1 невыполненная задача : "1 item left"
        - 2 невыполненные задачи : "2 items left"
        """
        self.create_todo(todo_titles[0])
        self.change_todo_status(todo_titles[0])
        assert self.get_todos_count_string() == "0 items left"
        self.create_todo(todo_titles[1])
        assert self.get_todos_count_string() == "1 item left"
        self.create_todo(todo_titles[2])
        assert self.get_todos_count_string() == "2 items left"

    def test_change_one_todo_status(self):
        """
        Тест на смену статуса задачи (активная или завершенная)
            Предварительное условие:
        1. Список задач состоит из 2 активных задач. Завершенные задачи отсутствуют.
            Шаги:
        1. Открыть браузер и перейти на главную страницу.
        2. Установить флажок перед меткой активной задачи.
            Ожидаемый результат:
        1. Задача должна сменить статус
        2. Задача должна остаться в общем списке
        3. Задача должна отсутствовать в списке активных
        4. Задача должна присутствовать в списке завершенных
        """
        self.create_todo(todo_titles[0])
        self.create_todo(todo_titles[1])
        self.change_todo_status(todo_titles[1])
        assert self.check_todo_exist(todo_titles[1]) is True
        self.move_to("#/active")
        assert self.check_todo_exist(todo_titles[1]) is False
        self.move_to("#/completed")
        assert self.check_todo_exist(todo_titles[1]) is True

    def test_all_todos_count(self):
        """
        Тест на проверку количества элементов в разделах
            Предварительное условие:
        1. Список задач состоит из 2 активных и 1 завершенной задачи.
            Шаги:
        1. Открыть браузер и перейти на главную страницу.
        2. Проверить количеств общих задач (активные + завершенные)
        3. Перейти в раздел активных to-do
        4. Проверить количество активных задач
        5. Перейти в раздел завершенных to-do
        6. Проверить количество завершенных задач

            Ожидаемый результат:
        1. Количество задач в разделе All == 3 (2 активные, 1 завершенная)
        2. Количество задач в разделе Complete == 1
        3. Количество задач в разделе Active = 2
        """
        self.create_todo(todo_titles[0])
        self.create_todo(todo_titles[1])
        self.create_todo(todo_titles[2])
        self.change_todo_status(todo_titles[1])
        all_todos = self.get_all_todos_count()
        active_todos_count = self.get_active_todos_count()
        complete_todos_count = self.get_comlete_todos_count()
        assert all_todos == 3
        assert active_todos_count == 2
        assert complete_todos_count == 1
        self.move_to("#/active")
        active_todos_count = self.get_active_todos_count()
        assert active_todos_count == 2
        self.move_to("#/completed")
        complete_todos_count = self.get_comlete_todos_count()
        assert complete_todos_count == 1

    def test_clear_all_completed_todos(self):
        """
        Тест проверки очистки всех завершенных задач
            Предварительное условие:
        1. Список задач состоит из 2 активных задач
            Шаги:
        1. Открыть браузер и перейти на главную страницу
        2. Проверить отсутствие нопки Clear completed
        3. Отметить 1 задачу как завершенную
        4. Перейти в раздел Completed
        5. Проверить наличие 1 завершенной задачи
        6. Нажать на ссылку Clear completed
            Ожидаемый результат:
        1. Отсутствие задач в разделе Completed
        2. Отсутствие завершенных задач в разделе Active
        3. Отсутствие завершенных задач в разделе All
        """
        self.create_todo(todo_titles[0])
        self.create_todo(todo_titles[1])
        self.change_todo_status(todo_titles[1])
        assert self.check_object_exist() is True
        self.move_to("#/completed")
        assert self.get_comlete_todos_count() == 1
        self.click_clear_completed_button()
        assert self.get_comlete_todos_count() == 0
        self.move_to("#/active")
        assert self.get_comlete_todos_count() == 0
        self.move_to("#/")
        assert self.get_comlete_todos_count() == 0

    def test_change_all_todo_status(self):
        """
        Тест на смену статуса всех задач (активные или завершенные)
            Предварительное условие:
        1. Список задач состоит из 2 активных задач.
            Шаги:
        1. Открыть браузер и перейти на главную страницу.
        2. Нажать на кнопку смену статуса всех задач.

            Ожидаемый результат:
        1. Количество задач в разделе All == 2 (2 завершенная)
        2. Количество задач в разделе Complete == 2
        3. Количество задач в разделе Active = 0
        """
        self.create_todo(todo_titles[0])
        self.create_todo(todo_titles[1])
        self.change_all_todo_status()
        self.move_to("#/active")
        active_todos_count = self.get_active_todos_count()
        assert active_todos_count == 0
        self.move_to("#/completed")
        complete_todos_count = self.get_comlete_todos_count()
        assert complete_todos_count == 2
        assert self.check_todo_exist(todo_titles[0]) is True
        assert self.check_todo_exist(todo_titles[1]) is True

    def test_update_todo_text(self):
        """
        Тест на обновление текста to-do
            Предварительноы условия:
        1. Список задач состоит из 2 элементов.
            Шаги:
        1. Открыть браузер и перейти на главную страницу.
        3. Дважды щелкните активный to-do, текст должен стать редактируемым.
        4. Ввести новое значение.
        5. Нажать клавишу ВВОД.
            Ожидаемый результат:
        1. Редактируемый элемент существует в списке задач.
        2. Текст редактируемого to-do изменился
        """
        self.create_todo(todo_titles[0])
        assert self.check_todo_exist(todo_titles[0]) is True
        new_todo_title = " and other..."
        self.edit_todo(todo_titles[0], new_todo_title)
        assert self.check_todo_exist(new_todo_title) is True
