from booking.booking import Booking
import traceback

try:
    with Booking(teardown=False) as bot:
        bot.land_first_page()
        # bot.change_currency(currency="GBP")
        bot.select_place_to_go('台北')
        bot.select_dates(check_in_date='2023-03-01', check_out_date='2023-03-21')
        bot.select_adults(4)
        bot.click_search()
        bot.apply_filtrations(3)
        bot.refresh()  # after filter, page changes
        bot.report_result()
        
except Exception as ex:
    if 'in PATH' in str(ex):
        print('Please make sure chromedriver.exe is in your system PATH.')
    else:
        print(f"{traceback.format_exc()}")
    
