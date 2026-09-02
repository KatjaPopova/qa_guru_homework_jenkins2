from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Calendar:
    MONTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")
    YEAR_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")

    def __init__(self, driver, wait, input_locator):
        self.driver = driver
        self.wait = wait
        self.input_locator = input_locator

    def select_date(self, day: str, month: str, year: str):
        self.wait.until(EC.element_to_be_clickable(self.input_locator)).click()

        month_select = self.wait.until(EC.element_to_be_clickable(self.MONTH_SELECT))
        month_select.click()

        month_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f".//option[@value='{month}']")))
        month_option.click()

        year_select = self.wait.until(EC.element_to_be_clickable(self.YEAR_SELECT))
        year_select.click()

        year_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f".//option[@value='{year}']")))
        year_option.click()

        # у дней классы вида ".react-datepicker__day--015" для 15 и ".react-datepicker__day--005" для 5
        day_padded = f"0{day}" if len(day) == 1 else day
        day_locator = (
            By.CSS_SELECTOR,
            f".react-datepicker__day--{day_padded}:not(.react-datepicker__day--outside-month)"
        )
        self.wait.until(EC.element_to_be_clickable(day_locator)).click()
