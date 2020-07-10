import os
from selenium import webdriver


class TestToDo():
    def setup(self):
        capabilities = {
            "browserName": "chrome",
            "version": "80.0",
            "enableVNC": True,
            "enableVideo": False
        }

        self.driver = webdriver.Remote(
            command_executor=os.environ.get('SELENOID'),
            desired_capabilities=capabilities)

        self.driver.get("http://todomvc.com/examples/react/#/")

    def teardown(self):
        self.driver.close()
        print("basic teardown into class")

