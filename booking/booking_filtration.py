# This file will include a class with instance methods.
# That will be responsible to interact with our website
# After we have some results, to apply filtrations.
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        """
        This function applies filtration by the number of hotel stars in the search result.
        :param star_values: List of desired numbers of stars
        :return:
        """
        for star_value in star_values:
            star_filtration_box = self.driver.find_element(
                by=By.CSS_SELECTOR,
                value=f'div[data-filters-item="class:class={star_value}"]')
            star_filtration_box.click()

    def apply_budget(self, budget=3):
        """
        This function applies filtration by the desired budget in the search result.
        :param budget: int 3-Low, 4-Midle, 5-High budget
        :return:
        """
        budget_filtration_box = self.driver.find_element(
            by=By.CSS_SELECTOR,
            value=f'div[data-filters-item="pri:pri={budget}"]')
        budget_filtration_box.click()

    def sort_price_lowest_first(self):
        element = self.driver.find_element(
            by=By.CSS_SELECTOR,
            value='li[data-id="price"]')
        element.click()
