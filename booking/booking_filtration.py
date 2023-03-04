import booking.constants as const
from selenium import webdriver


class BookingFiltration:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        
    def apply_start_rating(self, star_value):
        # star_filtraton_box = self.driver.find_elements_by_xpath('//*[@id="filter_group_class_:R1cq:"]')
        filter_lable_elements = self.driver.find_elements_by_xpath('//div[@data-testid="filters-group-label-content"]')
        

        for star_element in filter_lable_elements:
            if star_element.text.strip() == f'{star_value} 星級':
                star_element.click()
                break

    def sort_price_lowest_first(self):
        sort_element = self.driver.find_element_by_xpath('//button[@data-testid="sorters-dropdown-trigger"]')
        sort_element.click()
        
        lowest_first_element = self.driver.find_element_by_xpath('//button[@data-id="price"]')
        lowest_first_element.click()