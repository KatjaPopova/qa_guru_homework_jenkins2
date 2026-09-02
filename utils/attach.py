import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.remote.webdriver import WebDriver


def add_screenshot(driver: WebDriver):
    png = driver.get_screenshot_as_png()

    allure.attach(
        body=png,
        name="screenshot",
        attachment_type=AttachmentType.PNG,
        extension=".png",
    )


def add_logs(driver: WebDriver):
    logs = driver.execute(
        "getLog",
        {"type": "browser"},
    )["value"]

    log = "".join(f"{text}\n" for text in logs)

    allure.attach(
        body=log,
        name="browser_logs",
        attachment_type=AttachmentType.TEXT,
        extension=".log",
    )


def add_html(driver: WebDriver):
    html = driver.page_source

    allure.attach(
        body=html,
        name="page_source",
        attachment_type=AttachmentType.HTML,
        extension=".html",
    )


def add_video(driver: WebDriver):
    session_id = driver.session_id
    video_url = (
        f"https://selenoid.qa.guru/video/{session_id}.mp4"
    )

    html = (
        "<html><body>"
        "<video width='100%' height='100%' controls autoplay>"
        f"<source src='{video_url}' type='video/mp4'>"
        "</video>"
        "</body></html>"
    )

    allure.attach(
        body=html,
        name=f"video_{session_id}",
        attachment_type=AttachmentType.HTML,
        extension=".html",
    )