import random

from ProjFunc import *

bot = UsTsBot(end_num=1000)
bot.get_current_number()


def check_captcha():
    captcha_status = bot.check_for_captcha_check()
    if captcha_status == "Checking...":
        print(captcha_status)
        sleep(1)
        check_captcha()
    elif captcha_status == "Captcha completed!":
        print(captcha_status)
        bot.get_to_default_content()
        pass
    elif captcha_status == "Captcha appeared!":
        print(captcha_status)
        bot.solve_captcha()
        bot.get_to_default_content()


while bot.start_number <= bot.end_number:
    try:
        x = 500
        y = random.randint(500, 1000)
        bot.set_viewport_size(x, y)
        print(f"Current Number: {bot.start_number}")
        bot.goto_us_ts()
        sleep(0.75)

        bot.send_keys_to_docket(docket_number=bot.start_number)
        sleep(0.2)

        bot.switch_to_captcha_iframe()
        sleep(0.2)

        bot.check_for_captcha_check()
        sleep(1)

        bot.click_on_captcha_box()
        sleep(0.2)

        print("Checking for captcha...")
        check_captcha()
        sleep(0.2)

        bot.click_on_search_button()
        sleep(1)

        if bot.record_found():

            bot.click_on_html_button()
            sleep(0.1)

            data = bot.get_table_data()

            bot.fill_form(data)
        else:
            pass

        with open("current_number.txt", "w") as file:
            file.write(str(bot.start_number))
        bot.start_number += 1
    except:
        pass

print("Done!")
