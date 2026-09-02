import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


load_dotenv()


@pytest.fixture()
def driver():
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    if not login or not password:
        pytest.fail("Проверь LOGIN и PASSWORD в файле .env")

    options = Options()
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Remote(
        command_executor=(
            f"https://{login}:{password}"
            "@selenoid.qa.guru/wd/hub"
        ),
        options=options,
    )

    print("\nRemote session ID:", driver.session_id)

    yield driver

    driver.quit()
