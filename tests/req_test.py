from selenium.common.exceptions import NoSuchElementException
from tests.base import TestToDo


class TestReq(TestToDo):
    def test_header(self):
        self.driver.get("http://todomvc.com/examples/react/#/")
        element = None
        try:
            element = self.driver.find_element_by_xpath("/html/body/section/div/section")
        except NoSuchElementException:
            pass
        assert element is None

    def test_footer(self):
        self.driver.get("http://todomvc.com/examples/react/#/")
        element = None
        try:
            element = self.driver.find_element_by_xpath("/html/body/section/div/footer")
        except NoSuchElementException:
            pass
        assert element is None

