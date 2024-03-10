"""
testing of channels and websockets:
requires chromedriver and Chrome.
it is possible to set it up with
the gecko web driver to work with Firefox

for testing the chat app,
remember to go to settings.py and
uncomment the sqlite3 db and
comment-out the other two dbs 
(production and development)
run command: python3 manage.py test chat.tests

source: https://channels.readthedocs.io/en/stable/topics/testing.html
with some modifications
"""
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class ChatTests(ChannelsLiveServerTestCase):
    """
    a selenium-driven test suite to test
    the functionality of the chat app
    """

    serve_static = True  # emulate StaticLiveServerTestCase

    @classmethod
    def setUpClass(cls):
        """
        setup class
        """
        super().setUpClass()
        try:
            # NOTE: Requires chromedriver binary to be installed in $PATH
            cls.driver = webdriver.Chrome()
        except Exception:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        """
        teardown class
        """
        cls.driver.quit()
        super().tearDownClass()

    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        """
        test message is visible in chatroom
        """
        try:
            self._enter_chat_room("Diagnosis_Discussion")

            self._open_new_window()
            self._enter_chat_room("Diagnosis_Discussion")

            # does dr. Griffin's message appear in his own window?
            self._switch_to_window(0)
            self._post_message("hello, dr.Simpson")
            WebDriverWait(self.driver, 5).until(
                lambda _: "hello, dr.Simpson" in self._chat_log_value,
                "test#1: Message was not received by window 1 from window 1",
            )

            self.assertTrue(
                "hello, dr.Simpson" in self._chat_log_value,
                "test#1: Message was improperly received by window 2 from window 1",
            )
            # does dr. Griffin's message appear in dr. Simpson's window?
            self._switch_to_window(1)
            WebDriverWait(self.driver, 5).until(
                lambda _: "hello, dr.Simpson" in self._chat_log_value,
                "test#1: Message was not received by window 2 from window 1",
            )

            self.assertTrue(
                "hello, dr.Simpson" in self._chat_log_value,
                "test#1: Message was improperly received by window 2 from window 1",
            )
        except Exception:
            super().tearDownClass()
            raise
        finally:
            self._close_all_new_windows()

    def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        """
        tests message is confined to one room
        """
        try:
            self._enter_chat_room("Diagnosis_Discussion")

            self._open_new_window()

            # members in different chat rooms should not experience cross-talk
            self._enter_chat_room("Research_News")
            self._switch_to_window(0)
            self._post_message("hello, world")
            WebDriverWait(self.driver, 2).until(
                lambda _: "hello, world" in self._chat_log_value,
                "test#2: Message was not received by window 1 from window 1",
            )

            self._switch_to_window(1)
            self._post_message("good-bye, world")
            WebDriverWait(self.driver, 2).until(
                lambda _: "good-bye, world" in self._chat_log_value,
                "test#2: Message was not received by window 2 from window 2",
            )
            self.assertTrue(
                "hello, world" not in self._chat_log_value,
                "test#2: Message was improperly received by window 2 from window 1",
            )
        except Exception:
            super().tearDownClass()
            raise
        finally:
            self._close_all_new_windows()

    # === utility functions===

    # this method does not directly test
    # the <select> and <options> elements.
    # it treats the element as if it were
    # a text input field of a form in order
    # to navigate to the chat room.
    # I have not found a way to adapt
    # the selenium select methodology
    # to test the <select> and <options> elements
    # for a websockets/ASGI setup
    # ref: https://www.selenium.dev/documentation/webdriver/support_features/select_lists/
    def _enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + "/chat/" + room_name)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        WebDriverWait(self.driver, 2).until(
            lambda _: room_name in self.driver.current_url,
            "Room page did not load: %s" % self.driver.current_url,
        )

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self._switch_to_window(-1)

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self._switch_to_window(-1)
            self.driver.execute_script("window.close();")
        if len(self.driver.window_handles) == 1:
            self._switch_to_window(0)

    def _switch_to_window(self, window_index):
        self.driver.switch_to.window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message, Keys.ENTER).perform()

    @property
    def _chat_log_value(self):
        return self.driver.find_element(
            by=By.CSS_SELECTOR, value="#chat-log"
        ).get_property("value")
