import pytest
from tests.base import TestToDo


@pytest.mark.first
class TestSmoke(TestToDo):
    def test_smoke(self):
        self.driver.get("http://todomvc.com/examples/react/#/")
        assert "React • TodoMVC" == self.driver.title
