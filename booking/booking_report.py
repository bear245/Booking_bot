# This file is going to include methods that will parse
# The specific data that we need from each one of the deal boxes.
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class BookingReport:
    def __init__(self, boxes_section_element: WebDriver):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            by=By.CSS_SELECTOR,
            value='div[data-testid="property-card"]')

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            # Pulling the hotel name
            hotel_name = deal_box.find_element(
                by=By.CSS_SELECTOR,
                value='div[data-testid="title"]').get_attribute('innerHTML').strip()
            # Pulling the hotel price
            hotel_price = deal_box.find_element(
                by=By.CSS_SELECTOR,
                value='div[data-testid="price-and-discounted-price"]').text
            # Putting the hotel review score
            hotel_score = deal_box.find_element(
                by=By.CSS_SELECTOR,
                value='div[data-testid="review-score"]').text[0:3]

            collection.append([hotel_name, hotel_price, hotel_score])
        return collection
