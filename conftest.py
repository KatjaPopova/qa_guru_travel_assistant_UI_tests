import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.main_page import MainPage
from pages.travel_assistant_page import TravelAssistantPage


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.tutu.ru",
        help="Base URL of the application"
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )


@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--window-size=1920,1080")

    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")

    prefs = {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 2
    }
    options.add_experimental_option("prefs", prefs)

    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    yield browser

    allure.attach(
        browser.get_screenshot_as_png(),
        name="final_screenshot",
        attachment_type=allure.attachment_type.PNG
    )

    browser.quit()


@pytest.fixture
def main_page(driver, request):
    base_url = request.config.getoption("--base-url")
    page = MainPage(driver)
    page.open(base_url)
    return page


@pytest.fixture
def travel_assistant_widget(main_page):
    main_page.open_cap_chat()
    return TravelAssistantPage(main_page.driver)
