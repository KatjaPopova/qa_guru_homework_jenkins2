import os
from urllib.parse import quote

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import attach

load_dotenv()


@pytest.fixture(scope="function")
def driver(request):
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    if not login:
        pytest.fail("Переменная LOGIN не передана")

    if not password:
        pytest.fail("Переменная PASSWORD не передана")


    encoded_login = quote(login, safe="")
    encoded_password = quote(password, safe="")

    options = Options()
    options.add_argument("--window-size=1920,1080")

    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "148.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=(
            f"https://{encoded_login}:{encoded_password}"
            "@selenoid.qa.guru/wd/hub"
        ),
        options=options,
    )

    yield driver

    attach.add_screenshot(driver)
    attach.add_html(driver)
    attach.add_logs(driver)
    attach.add_video(driver)

    driver.quit()
