from selenium import webdriver
from booking.booking_filtration import BookingFiltration
from booking_report import BookingReport
from prettytable import PrettyTable
import booking.constants as const
import os


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"D:\Projects\bot\chromedriver.exe",
                 teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(5)  # global implicitly wait
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            print('Browser is closing...')
            self.quit()
            print('Browser is closed!')

    def land_first_page(self):
        self.get(const.BASE_URL)
        try:
            login_modal = self.find_element_by_xpath(const.CLOSE_LOGIN_MODAL)
            login_modal.click()
        except Exception:  # NoSuchElementException
            pass

    def change_currency(self, target_currency=None):
        currency_element = self.find_element_by_css_selector(const.CHANGE_CURRENCY)
        currency_element.click()
        currencies = self.find_elements_by_xpath(const.ALL_CURRENCIES)

        for currency in currencies:
            if target_currency in currency.text:
                currency.click()
                break

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element_by_xpath(const.PLACE_TO_GO)
        search_field.clear()
        search_field.send_keys(place_to_go)

        autocompletes = self.find_elements_by_xpath('//span[@data-testid="autocomplete-icon-default"]')
        autocompletes[0].click()  # default to first

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element_by_xpath(f'//span[@data-date="{check_in_date}"]')
        check_in_element.click()
        check_out_element = self.find_element_by_xpath(f'//span[@data-date="{check_out_date}"]')
        check_out_element.click()

    def select_adults(self, target_adult_num=1):
        selection_element = self.find_element_by_xpath(const.OCCUPANCY_CONFIG)
        selection_element.click()

        adult_num_element = self.find_element_by_xpath(const.ADULT_NUM)
        current_adult_num = int(adult_num_element.text)

        if current_adult_num > target_adult_num:
            adjust_adults_element = self.find_element_by_xpath(const.ADULT_SUBSTRACT)
        elif current_adult_num < target_adult_num:
            adjust_adults_element = self.find_element_by_xpath(const.ADULT_ADD)

        for _ in range(abs(target_adult_num - current_adult_num)):
                adjust_adults_element.click()

    def click_search(self):
        search_button = self.find_element_by_xpath(const.SEARCH)
        search_button.click()

    def apply_filtrations(self, star_value):
        filtration = BookingFiltration(driver=self)
        filtration.apply_start_rating(star_value)
        filtration.sort_price_lowest_first()
        
    def report_result(self):
        hotel_boxes = self.find_element_by_id('hotellist_inner')
        
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=['Hotel Name', 'Hotel Price', 'Hotel Score']
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)