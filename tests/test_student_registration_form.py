import allure
import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.student_registration_page import StudentRegistrationPage


@allure.epic("DemoQA Practice Form")
@allure.feature("Student Registration Form")
@pytest.mark.ui
class TestStudentRegistration:

    # =========================
    # ПОЗИТИВНЫЕ ТЕСТЫ
    # =========================
    @allure.story("Submit form")
    @allure.title("Форма отправляется с обязательными полями")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("https://example.testrail.io/index.php?/cases/view/1", name="TC-1")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_successful_submit_with_required_fields(self, driver):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        with allure.step("Заполнить обязательные поля и отправить форму"):
            page.fill_required_fields("Петр", "Петров", gender=1, phone="8900000000")
            page.submit()

        with allure.step("Проверить успешную отправку и данные студента"):
            page.check_success_modal()
            page.check_user_in_table("Петр")
            page.check_user_in_table("Петров")

    @allure.story("Fill optional fields")
    @allure.title("Выбор всех доступных Subjects")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://example.atlassian.net/browse/PROJ-10", name="Task PROJ-10")
    @pytest.mark.positive
    @pytest.mark.regression
    def test_positive_select_all_subjects(self, driver):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        subjects = [
            "Maths",
            "Physics",
            "Chemistry",
            "Biology",
            "English",
            "Computer Science",
            "Economics",
            "History",
            "Hindi",
            "Civics",
            "Arts",
        ]

        with allure.step("Заполнить обязательные поля и выбрать все предметы"):

            page.fill_required_fields("Ivan", "Petrov", gender=1, phone="9998887766")

            for subject in subjects:
                page.enter_subject(subject)

        page.submit()

        with allure.step("Проверить выбранные предметы в результатах"):
            page.check_success_modal()

            for subject in subjects:
                page.check_user_in_table(subject)

    @allure.story("Fill optional fields")
    @allure.title("Выбор всех доступных Hobbies")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    @pytest.mark.regression
    def test_positive_select_all_hobbies(self, driver):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        with allure.step("Заполнить обязательные поля и выбрать все хобби"):
            page.fill_required_fields("Anna", "Ivanova", gender=2, phone="1112223344")

        page.select_hobby(1)
        page.select_hobby(2)
        page.select_hobby(3)

        page.submit()

        with allure.step("Проверить выбранные хобби в результатах"):
            page.check_success_modal()
            page.check_user_in_table("Sports")
            page.check_user_in_table("Reading")
            page.check_user_in_table("Music")

    @allure.story("Submit form with one hobby")
    @allure.title("Отправка формы с одним хобби (комбинации пола и хобби)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    @pytest.mark.regression
    @pytest.mark.parametrize("gender", [1, 2], ids=["male", "female"])
    @pytest.mark.parametrize("hobby", [1, 2, 3], ids=["sports", "reading", "music"])
    def test_submit_with_one_hobby(self, driver, gender, hobby):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        with allure.step("Заполнить форму, выбрать одно хобби и отправить"):
            page.fill_required_fields("Alex", "Test", gender=gender, phone="9000000000")
            page.select_hobby(hobby)
            page.submit()

        page.check_success_modal()

    @allure.story("Waits")
    @allure.title("Fluent wait: дождаться текста в таблице результата")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_fluent_wait_result_table_has_text(self, driver):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        with allure.step("Заполнить форму с хобби Sports и отправить"):
            page.fill_required_fields("Anna", "Ivanova", gender=2, phone="1112223344")
            page.select_hobby(1)  # Sports
            page.submit()

        wait = WebDriverWait(
            driver,
            timeout=6,
            poll_frequency=0.2,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException)
        )

        wait.until(EC.text_to_be_present_in_element(page.RESULT_TABLE, "Sports"))

        page.check_user_in_table("Sports")

    @allure.story("Maintenance")
    @allure.title("Пример: тест временно отключён (skip)")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.skip(reason="Временно отключили тест ( фича в разработке)")
    @pytest.mark.regression
    def test_disabled_example(self, driver):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        page.fill_required_fields("Skip", "Example", gender=1, phone="9000000000")
        page.submit()

        page.check_success_modal()

    # =========================
    # НЕГАТИВНЫЕ ТЕСТЫ
    # =========================
    @allure.story("Validation")
    @allure.title("Пустая форма не отправляется")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.issue("https://example.atlassian.net/browse/BUG-1", name="BUG-1 (пример)")
    @pytest.mark.negative
    @pytest.mark.smoke
    def test_negative_empty_form_not_submitted(self, driver):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        page.submit()

        assert page.is_success_modal_opened() is False

    @allure.story("Validation")
    @allure.title("Форма не отправляется без выбора пола")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.regression
    def test_negative_without_gender_not_submitted(self, driver):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        with allure.step("Заполнить обязательные поля, кроме пола"):
            page.enter_first_name("Ivan")
            page.enter_last_name("Petrov")
            page.enter_phone("9998887766")

        page.submit()

        assert page.is_success_modal_opened() is False

    @allure.story("Validation")
    @allure.title("Форма не отправляется с невалидным телефоном")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "case, phone",
        [
            ("empty", ""),
            ("too_short", "8904"),
            ("with_plus", "+79049153045"),
            ("only_letters", "abcdefghij"),
            ("numbers_and_letters", "89049abcde"),
            ("numbers_and_special symbols", "89049153!@"),
        ],
        ids=["empty", "too_short", "with_plus", "only_letters", "numbers_and_letters", "numbers_and_special symbols"]
    )
    def test_negative_invalid_phone_not_submitted(self, driver, case, phone):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        with allure.step(f"Кейс: {case}, phone='{phone}'"):
            page.fill_required_fields("Ivan", "Petrov", gender=1, phone=phone)
            page.submit()

        assert page.is_success_modal_opened() is False

    @allure.story("Validation")
    @allure.title("Известный баг (xfail): форма отправляется c номером телефона, состоящим из 10 нулей")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.xfail(reason="Известный баг: номер телефона состоит только из нулей")
    def test_known_bug_example(self, driver):
        page = StudentRegistrationPage(driver)
        page.open_and_prepare()

        page.fill_required_fields("Alex", "Test", gender=2, phone="0000000000")

        page.submit()

        assert page.is_success_modal_opened() is False
