from tests.base import TestToDo
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class ToDoPage(TestToDo):
    def get_todo_input(self):
        todo_input = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                (By.XPATH, "/html/body/section/div/header/input"))
        )
        return todo_input

    def create_todo(self, todo_title):
        todo_input = self.get_todo_input()
        todo_input.send_keys(todo_title)
        todo_input.send_keys(Keys.ENTER)

    def change_todo_status(self, todo_title):
        checkbox = self.driver.find_elements_by_xpath(
            f"//label[contains(text(), '{todo_title}')]/preceding-sibling::input[@type='checkbox']")
        checkbox[0].click()

    def change_all_todo_status(self):
        toggle_all = self.driver.find_elements_by_xpath("//label[@for='toggle-all']")
        toggle_all[0].click()

    def click_clear_completed_button(self):
        toggle_all = self.driver.find_elements_by_xpath(
            "//button[contains(text(),'Clear completed') and @class='clear-completed']")
        toggle_all[0].click()

    def check_object_exist(self):
        exist_object = self.driver.find_elements_by_xpath("//button[@class='clear-completed']")
        if exist_object:
            return True
        else:
            return False

    def delete_todo(self, todo_title):
        label = self.driver.find_elements_by_xpath(
            f"//label[contains(text(), '{todo_title}')]")
        action = ActionChains(self.driver).move_to_element(label[0]).perform()
        delete_button = self.driver.find_elements_by_xpath(
            f"//label[contains(text(), '{todo_title}')]/following-sibling::button")
        delete_button[0].click()

    def edit_todo(self, todo_title, new_title):
        element = self.driver.find_element(By.XPATH, f"//label[contains(.,'{todo_title}')]")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.XPATH, f"//input[@value='{todo_title}']").send_keys(new_title)
        self.driver.find_element(By.XPATH, f"//input[@value='{todo_title}']").send_keys(Keys.ENTER)

    def move_to(self, link_name):
        self.driver.find_element(By.XPATH,
                                 f"//a[contains(@href, '{link_name}')]").click()

    def get_todos_count_string(self):
        parent_lement = self.driver.find_element_by_class_name("todo-count")
        todos_count, _, word1, word2 = parent_lement.find_elements_by_xpath(".//*")
        todos_count_string = f"{todos_count.text} {word1.text} {word2.text}"
        return todos_count_string

    def get_todos_count_num(self):
        todos_count_string = self.get_todos_count_string()
        todos_count_num = todos_count_string.split(' ')[0]
        return todos_count_num

    def get_all_todos_count(self):
        all_todos = self.driver.find_elements_by_xpath("//ul[@class='todo-list']/*")
        return len(all_todos)

    def get_comlete_todos_count(self):
        completed_todos = self.driver.find_elements_by_xpath("//ul[@class='todo-list']/li[@class='completed']")
        return len(completed_todos)

    def get_active_todos_count(self):
        active_todos = self.driver.find_elements_by_xpath("//ul[@class='todo-list']/li[@class='']")
        return len(active_todos)

    def check_todo_exist(self, todo_title, completed=False):
        if completed:
            param = "/[@class='completed']"
        else:
            param = ''
        checkbox = self.driver.find_elements_by_xpath(
            f"/{param}/div[@class='view']/label[contains(text(), '{todo_title}')]")
        if checkbox:
            return True
        else:
            return False
