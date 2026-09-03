import logging
import os

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.calendar import Calendar

logger = logging.getLogger(__name__)


class StudentRegistrationPage:
    # =========================
    # ЛОКАТОРЫ
    # =========================

    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    USER_NUMBER = (By.ID, "userNumber")
    DATE_INPUT = (By.ID, "dateOfBirthInput")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    UPLOAD_PICTURE = (By.ID, "uploadPicture")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    STATE_DROPDOWN = (By.ID, "state")
    CITY_DROPDOWN = (By.ID, "city")
    SUBMIT = (By.ID, "submit")

    CLOSE_BANNER = (By.XPATH, "//*[@id='fixedban']/div/div/button")

    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")
    RESULT_TABLE = (By.CLASS_NAME, "table-responsive")

    # =========================
    # ИНИЦИАЛИЗАЦИЯ
    # =========================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        self.calender = Calendar(driver, self.wait, self.DATE_INPUT)

    # =========================
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # =========================
    @allure.step("Открыть страницу регистрации студента")
    def open(self):
        self.driver.get(self.URL)
        return self

    @allure.step("Удалить элементы, перекрывающие форму")
    def _close_commercial_banner(self):
        removed = self.driver.execute_script("""
            let removedCount = 0;

            const fixedban = document.getElementById('fixedban');
            if (fixedban) { fixedban.remove(); removedCount++; }

            const footer = document.querySelector('footer');
            if (footer) { footer.remove(); removedCount++; }

            return removedCount;
        """)
        logger.info("Removed %s blocking elements (fixedban/footer)", removed)

    @allure.step("Открыть и подготовить страницу регистрации")
    def open_and_prepare(self):
        with allure.step("Открыть страницу и убрать баннеры"):
            self.open()
            self._close_commercial_banner()

    @allure.step("Нажать кнопку Submit")
    def submit(self):
        with allure.step("Нажать Submit"):
            submit_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT))
            self.driver.execute_script("arguments[0].click();", submit_button)

    # =========================
    # ЗАПОЛНЕНИЕ ПОЛЕЙ
    # =========================

    @allure.step("Ввести имя: {first_name}")
    def enter_first_name(self, first_name):
        self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME)).send_keys(first_name)

    @allure.step("Ввести фамилию: {last_name}")
    def enter_last_name(self, last_name):
        self.wait.until(EC.element_to_be_clickable(self.LAST_NAME)).send_keys(last_name)

    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        self.wait.until(EC.element_to_be_clickable(self.EMAIL)).send_keys(email)

    @allure.step("Выбрать пол с номером: {gender_number}")
    def select_gender(self, gender_number):
        gender_locator = (By.CSS_SELECTOR, f"label[for='gender-radio-{gender_number}']")
        self.wait.until(
            EC.element_to_be_clickable(gender_locator)
        ).click()

    @allure.step("Ввести номер телефона: {phone}")
    def enter_phone(self, phone):
        self.wait.until(EC.element_to_be_clickable(self.USER_NUMBER)).send_keys(phone)

    @allure.step("Выбрать дату рождения: {day} {month} {year}")
    def select_date(self, day, month, year):
        self.calender.select_date(day=day, month=month, year=year)

    @allure.step("Выбрать предмет: {subject}")
    def enter_subject(self, subject):
        subject_input = self.wait.until(EC.element_to_be_clickable(self.SUBJECTS_INPUT))
        subject_input.send_keys(subject)
        subject_input.send_keys(Keys.ENTER)

    @allure.step("Выбрать хобби с номером: {hobby_number}")
    def select_hobby(self, hobby_number):
        hobby_locator = (By.CSS_SELECTOR, f"label[for='hobbies-checkbox-{hobby_number}']")
        self.wait.until(EC.element_to_be_clickable(hobby_locator)).click()

    @allure.step("Загрузить файл: {file_name}")
    def upload_file(self, file_name):
        file_path = os.path.abspath(file_name)
        self.wait.until(EC.presence_of_element_located(self.UPLOAD_PICTURE)).send_keys(file_path)

    @allure.step("Ввести адрес: {address}")
    def enter_address(self, address):
        self.wait.until(EC.element_to_be_clickable(self.CURRENT_ADDRESS)).send_keys(address)

    @allure.step("Выбрать штат: {state_name}")
    def select_state(self, state_name):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        self.wait.until(EC.element_to_be_clickable(self.STATE_DROPDOWN)).click()

        state_option = (By.XPATH, f"//div[text()='{state_name}']")

        self.wait.until(EC.element_to_be_clickable(state_option)).click()

    @allure.step("Выбрать город: {city_name}")
    def select_city(self, city_name):
        self.wait.until(EC.element_to_be_clickable(self.CITY_DROPDOWN)).click()

        city_option = (By.XPATH, f"//div[text()='{city_name}']")

        self.wait.until(EC.element_to_be_clickable(city_option)).click()

    # =========================
    # ЗАПОЛНЕНИЕ ТОЛЬКО ОБЯЗАТЕЛЬНЫХ ПОЛЕЙ
    # =========================

    @allure.step("Заполнить обязательные поля")
    def fill_required_fields(self, first_name, last_name, gender, phone):
        with allure.step("Заполнить обязательные поля"):
            self.enter_first_name(first_name)
            self.enter_last_name(last_name)
            self.select_gender(gender)
            self.enter_phone(phone)

    # -------------------------
    # ВСПОМОГАТЕЛЬНЫЕ ПРОВЕРКИ
    # -------------------------

    @allure.step("Проверить окно успешной отправки формы")
    def check_success_modal(self):
        with allure.step("Проверить окно успешной отправки"):
            modal = self.wait.until(
                EC.visibility_of_element_located(self.MODAL_TITLE)
            )
            assert modal.text == "Thanks for submitting the form"

    def is_success_modal_opened(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.MODAL_TITLE))
            return True

        except TimeoutException:
            return False

    @allure.step("Проверить наличие текста в таблице результатов: {text}")
    def check_user_in_table(self, text):
        table = self.driver.find_element(*self.RESULT_TABLE)
        assert text in table.text
