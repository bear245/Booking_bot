import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
import os
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.by import By


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"K:\Work\GitHub\Selenium", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += r"K:\Work\GitHub\Selenium"
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        accept_cookies = self.find_element(
            by=By.ID,
            value="onetrust-accept-btn-handler")
        accept_cookies.click()

    def change_currency(self, currency=None):
        currency_element = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[data-modal-aria-label="Выберите валюту"]')
        currency_element.click()
        selected_currency_element = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')
        selected_currency_element.click()

    def change_language(self, language=None):
        language_element = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[data-tooltip-text="Выберите язык"]')
        language_element.click()
        selected_language_element = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'a[data-lang="{language}"]')
        selected_language_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(by=By.ID, value='ss')
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.find_element(
            by=By.CSS_SELECTOR,
            value='li[data-i="0"]')
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'td[data-date="{check_in_date}"]')
        check_in_element.click()
        check_out_element = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'td[data-date="{check_out_date}"]')
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.find_element(
            by=By.ID,
            value='xp__guests__toggle')
        selection_element.click()
        while True:
            decrease_adults_element = self.find_element(
                by=By.CSS_SELECTOR,
                value='button[aria-label="Взрослых: уменьшить количество"]')
            decrease_adults_element.click()
            # If the value of adults reaches 1, then we should get out of the loop
            adults_value_element = self.find_element(
                by=By.ID,
                value='group_adults')
            adults_value = adults_value_element.get_attribute('value')  # Give back adults count
            if int(adults_value) == 1:
                break
        increase_adults_element = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[aria-label="Взрослых: увеличить количество"]')
        for _ in range(count - 1):
            increase_adults_element.click()

    def select_children(self, count=1):
        increase_kids_element = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[aria-label="Детей: увеличить количество"]')
        for _ in range(count):
            increase_kids_element.click()

    def set_children_age(self, age=1):
        select_box = self.find_element(by=By.NAME, value='age')
        select_box.click()
        select_age = select_box.find_element(
            by=By.CSS_SELECTOR,
            value=f'option[value="{age}"]')
        select_age.click()

    def click_search(self):
        search_button = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[type="submit"]')
        search_button.click()

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.sort_price_lowest_first()
        filtration.apply_star_rating(3, 4)
        filtration.apply_budget(4)

    def report_results(self):
        hotel_boxes = self.find_element(
            by=By.ID,
            value='search_results_table')
        report = BookingReport(hotel_boxes)
        table = PrettyTable(field_names=["Hotel Name", "Hotel Price", "Hotel Score"])
        table.add_rows(report.pull_deal_box_attributes())
        print(table)
