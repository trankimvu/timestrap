from os import environ
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.core.management import call_command

from selenium.webdriver import Firefox as FirefoxDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class SeleniumTestCase(StaticLiveServerTestCase):
    def _flakyTestWrapper(self):
        testMethod = getattr(self, self.flakyTestMethodName)
        retries = 0
        while retries < 3:
            try:
                return testMethod()
            except Exception as e:
                print("\nRetrying flaky test %s" % self.flakyTestMethodName)
                retries += 1
                lastException = e
                sleep(1)
        raise lastException

    def run(self, result=None):
        self.flakyTestMethodName = self._testMethodName
        self._testMethodName = "_flakyTestWrapper"
        super().run(result)
        self._testMethodName = self.flakyTestMethodName

    @classmethod
    def setUpClass(cls):
        options = FirefoxOptions()
        if environ.get("MOZ_HEADLESS") != "0":
            # Setting environ var might seem redundant but some versions of firefox
            # and geckodriver fail to obey -headless properly
            environ["MOZ_HEADLESS"] = "1"
            options.add_argument("-headless")
        cls.driver = FirefoxDriver(firefox_options=options)
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(2)
        cls.driver.set_page_load_timeout(30)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        call_command("migrate", verbosity=0)
        call_command("fake", verbosity=0, iterations=1)

        self.logIn()

        super().setUp()

    def logIn(self):
        self.driver.get("%s%s" % (self.live_server_url, "/login/"))

        input_username = self.find("input-username")
        input_password = self.find("input-password")
        button_submit = self.find("button-submit")

        input_username.send_keys("admin")
        input_password.send_keys("admin")
        button_submit.click()

        self.find("app")

    def clear(self, element):
        # Selenium's clear command doesn't work
        value = element.get_attribute("value")
        for character in value:
            element.send_keys(Keys.BACK_SPACE)

    def find(self, id, element=None):
        # Our primary way of finding things
        if element:
            return element.find_element_by_id(id)
        else:
            return self.driver.find_element_by_id(id)

    def contains(self, string, element=None):
        # Finding things by a text string
        xpath = "//*[contains(text(), '%s')]" % (string,)
        if element:
            return element.find_element_by_xpath(xpath)
        else:
            return self.driver.find_element_by_xpath(xpath)

    def select(self, value, element):
        # Our select field uses the select2 jQuery plugin
        element = element.find_element_by_xpath("..")
        element_arrow = element.find_element_by_class_name(
            "select2-selection__arrow"
        )  # noqa: E501
        element_arrow.click()
        element_search = self.driver.find_element_by_class_name(
            "select2-search__field"
        )  # noqa: E501
        element_search.send_keys(value)
        element_search.send_keys(Keys.RETURN)
