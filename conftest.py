import os
from urllib.parse import quote

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()


@pytest.fixture(scope="function")
def driver(request):
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    if not login:
        pytest.fail("Переменная LOGIN не передана")

    if not password:
        pytest.fail("Переменная PASSWORD не передана")

    # Нужно, если в логине или пароле есть специальные символы.
    encoded_login = quote(login, safe="")
    encoded_password = quote(password, safe="")

    options = Options()
    options.add_argument("--window-size=1920,1080")

    options.set_capability(
        "selenoid:options",
        {
            "enableVNC": True,
            "enableVideo": True,
            "name": request.node.name,
        },
    )

    driver = webdriver.Remote(
        command_executor=(
            f"https://{encoded_login}:{encoded_password}"
            "@selenoid.qa.guru/wd/hub"
        ),
        options=options,
    )

    print(f"\nRemote session ID: {driver.session_id}")

    try:
        yield driver
    finally:
        driver.quit()
