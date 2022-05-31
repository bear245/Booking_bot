from booking.booking import Booking
import booking.constants as const

try:
    with Booking(teardown=False) as bot:
        bot.land_first_page()
        bot.change_currency(const.CURRENCY)
        bot.change_language(const.LANGUAGE)
        bot.select_place_to_go(const.PLACE_TO_GO)
        bot.select_dates(check_in_date=const.CHECK_IN,
                         check_out_date=const.CHECK_OUT)
        bot.select_adults(const.ADULTS)
        bot.select_children(const.CHILDREN)
        bot.set_children_age(const.CHILDREN_AGE)
        bot.click_search()
        bot.apply_filtration()
        bot.refresh()
        bot.report_results()

except Exception as e:
    if 'in PATH' in str(e):
        print("Please add to PATH your Selenium Drivers")
    else:
        raise
