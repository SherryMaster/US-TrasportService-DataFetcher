import itertools
import os
import random
import urllib.request
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium_stealth import stealth
import pandas as pd
import pyautogui as pg
import whisper
import warnings
import winsound

warnings.filterwarnings("ignore")

current_country = "Canada"
blacklisted_countries = {"United States": 0,
                         "United Kingdom": 0,
                         "Canada": 0,
                         "Brazil": 0,
                         "Ireland": 0,
                         "Mexico": 0,
                         "New Zealand": 0,
                         "Portugal": 0,
                         "South Africa": 0}

trascriber = whisper.load_model("base")


class UsTsBot():
    def __init__(self, end_num: int):

        self.start_number = 0
        self.end_number = end_num

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("debuggerAddress", "localhost:9222")

        self.driver = webdriver.Chrome(options=self.options, service=Service("C:\Development\chromedriver.exe"))

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def switch_urban_vpn(self):
        global current_country
        x = 1560
        y = 230
        y2 = 270

        for key, value in blacklisted_countries.items():
            if value != 0:
                blacklisted_countries[key] = value - 1

        blacklisted_countries[current_country] = 6

        print("Vpn Selection for countries:")

        for country, value in blacklisted_countries.items():
            if value != 0:
                print(f"    ❌{country} for {value} times")
            else:
                print(f"    ✔{country} are eligible")

        countries = ["United States", "United Kingdom", "Canada", "Brazil",
                     "Ireland", "Mexico", "New Zealand", "Portugal", "South Africa"]
        selected_country = random.choice(countries)

        while current_country == selected_country or blacklisted_countries[selected_country] != 0:
            selected_country = random.choice(countries)

        current_country = selected_country

        pg.hotkey("alt", "n")

        sleep(5)

        pg.moveTo(x, y)
        pg.click()

        pg.write(current_country, interval=0.1)

        pg.moveTo(x, y2)
        pg.click()

        sleep(4)
        print(f"🛡VPN Connected to: {current_country} 🛡")

        pg.hotkey("alt", "n")

    def switch_urban_vp(self):
        x = 1560
        y = 230
        y2 = 270

        pg.hotkey("alt", "n")

        sleep(3)

        pg.moveTo(x, y)
        pg.click()

        united_countries = ["United States", "United Kingdom"]

        pg.write(random.choice(united_countries), interval=0.1)

        pg.moveTo(x, y2)
        pg.click()

        sleep(4)

        pg.hotkey("alt", "n")

    def set_viewport_size(self, width, height):
        window_size = self.driver.execute_script("""
            return [window.outerWidth - window.innerWidth + arguments[0],
              window.outerHeight - window.innerHeight + arguments[1]];
            """, width, height)
        self.driver.set_window_size(*window_size)
        print(f"📺 Viewport size set to: {width}x{height}")

    def get_current_number(self):
        try:
            with open("current_number.txt", "r") as f:
                self.start_number = int(f.read()) + 1
            print(f"Search start number is set to: {self.start_number}")
        except FileNotFoundError:
            self.start_number = int(input("Enter start number: "))
            print(f"Search start number is set to: {self.start_number}")
        # finally:
        #     self.end_number = int(input("Enter end number: "))
        #     print(f"Search end number is set to: {self.end_number}")

    def goto_us_ts(self):
        print("Go to US-TS!")
        self.driver.get("https://li-public.fmcsa.dot.gov/LIVIEW/pkg_carrquery.prc_carrlist")

    def send_keys_to_docket(self, docket_number):
        print("Send keys to docket number!")
        self.driver.find_element(By.NAME, "n_docketno").send_keys(docket_number)

    def switch_to_captcha_iframe(self):
        print("Switch to captcha iframe!")
        self.driver.switch_to.default_content()
        iframe = self.driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        self.driver.switch_to.frame(iframe)
        print("Got inside captcha!")

    def click_on_captcha_box(self):
        print("Click on captcha box!")
        box = self.driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border')
        box.click()
        print("Clicked on captcha!")

    def check_for_captcha_check(self):
        mark = self.driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-spinner')

        if mark.get_attribute('style') == 'display: none; animation-play-state: running; opacity: 1;':
            return "Captcha completed!"
        elif mark.get_attribute('style') == 'display: none; animation-play-state: running; opacity: 0; transform: ' \
                                            'scale(0);':
            return "Captcha appeared!"
        else:
            return "Checking..."

    def solve_captcha(self):
        self.switch_to_captcha_solving_frame()
        sleep(0.1)
        self.click_on_audio_button()
        sleep(1)
        link = self.get_audio_link()
        sleep(0.1)
        self.play_audio()
        text = self.transcribe_audio(link)
        self.input_trascribed_audio(text)
        sleep(1)

    def switch_to_captcha_solving_frame(self):
        self.driver.switch_to.default_content()
        iframe = self.driver.find_element(By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]')
        self.driver.switch_to.frame(iframe)

        print("Switched to captcha solving frame!")

    def click_on_audio_button(self):
        max_tries = 5
        while max_tries > 0:
            try:
                audio_button = self.driver.find_element(By.ID, 'recaptcha-audio-button')
                audio_button.click()
                break
            except:
                max_tries -= 1
                print(f"🎧Audio button not found! Tries left: {max_tries}")
                winsound.Beep(1500, 150)

            sleep(1)

        if max_tries == 0:
            self.switch_urban_vpn()
            raise Exception("Audio button not found!")

        print("Audio button clicked!")

    def get_audio_link(self):
        # for i in range(10):
        #     self.driver.find_element(By.CLASS_NAME, 'rc-doscaptcha-header-text')
        max_tries = 5
        while max_tries > 0:
            try:
                audio = self.driver.find_element(By.ID, 'audio-source')
                audio_link = audio.get_attribute('src')
                break
            except:
                max_tries -= 1
                print(f"🔉🔗 Audio link not found! Tries left: {max_tries}")
                winsound.Beep(1000, 150)
            sleep(1)
        if max_tries == 0:
            self.switch_urban_vpn()
            raise Exception("Audio link not found!")

        print(f"Audio link is: {audio_link}")
        return audio_link

    def play_audio(self):
        self.driver.find_element(By.ID, ':2').click()

    def download_audio(self, audio_link):
        print("Downloading audio!")
        urllib.request.urlretrieve(audio_link, f"./Audios/audio_{self.start_number}.mp3")
        print("Audio downloaded!")

    def transcribe_audio(self, link):
        print("Transcribing audio!")
        with open('.temp', 'wb') as f:
            f.write(requests.get(link).content)
        result = trascriber.transcribe(".temp")
        print(f"------------\n📜Transcribed audio📜: {result['text'].strip()}\n------------")
        return result['text'].strip()

    def input_trascribed_audio(self, text):
        print("Inputting the transcribed audio!")
        audio_input = self.driver.find_element(By.ID, 'audio-response')
        audio_input.send_keys(text, Keys.ENTER)
        print("Audio inputted!")

    def check_audio_error_message(self):
        error_heading = self.driver.find_element(By.CLASS_NAME, 'rc-audiochallenge-error-message')
        if error_heading.get_attribute('style') == 'display:none':
            return False
        else:
            return True

    def get_to_default_content(self):
        self.driver.switch_to.default_content()

    def click_on_search_button(self):
        print("Click on search button!")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def record_found(self):
        try:
            red_heading = self.driver.find_element(By.XPATH, '/html/body/font/center[1]/font/b')
            if "no record" in red_heading.text.lower():
                print("No record found!\n-----------------------------\n")
                return False
        except:
            print("Record found!")
            return True

    def click_on_html_button(self):
        print("Click on html button!")
        html_button = self.driver.find_element(By.XPATH,
                                               '/html/body/font/table[2]/tbody/tr[2]/td[8]/center/font/form/input[3]')
        html_button.click()

    def get_table_data(self):
        print("Get table data!")
        warning = self.driver.find_element(By.XPATH, '/html/body/font/table[4]')
        us_dot = self.driver.find_element(By.XPATH, '/html/body/font/table[3]/tbody/tr[1]/td[1]').text
        docket_number = self.driver.find_element(By.XPATH, '/html/body/font/table[3]/tbody/tr[1]/td[2]').text
        legal_name = self.driver.find_element(By.XPATH, '/html/body/font/table[3]/tbody/tr[2]/td').text
        buisness_address = ""
        telephone = ""
        mail_address = ""
        common_authority_status = ""
        contract_authority_status = ""
        broker_authority_status = ""
        common_application_pending = ""
        contract_application_pending = ""
        broker_application_pending = ""
        property_ = ""
        passenger_ = ""
        household_goods = ""
        private = ""
        enterprise = ""
        bipd_insurance_required = ""
        cargo_insurance_required = ""
        bond_insurance_required = ""
        bipd_insurance_onfile = ""
        cargo_insurance_onfile = ""
        bond_insurance_onfile = ""

        print(f"⚠--{warning.text}--⚠")
        if "OUT OF SERVICE" in warning.text:
            legal_name = "OUT OF SERVICE"
        elif "pending insurance cancellation" in warning.text:
            legal_name = "PENDING INSURANCE CANCELLATION"
        else:
            print("fetching table data...")
            buisness_address = self.driver.find_element(By.XPATH,
                                                        '/html/body/font/table[5]/tbody/tr[3]/td[1]').text.replace("\n",
                                                                                                                   " ")
            telephone = self.driver.find_element(By.XPATH, '/html/body/font/table[5]/tbody/tr[3]/td[2]').text
            mail_address = self.driver.find_element(By.XPATH,
                                                    '/html/body/font/table[5]/tbody/tr[3]/td[3]').text.replace("\n",
                                                                                                               " ")
            common_authority_status = self.driver.find_element(By.XPATH,
                                                               '/html/body/font/table[6]/tbody/tr[2]/td[1]').text
            contract_authority_status = self.driver.find_element(By.XPATH,
                                                                 '/html/body/font/table[6]/tbody/tr[3]/td[1]').text
            broker_authority_status = self.driver.find_element(By.XPATH,
                                                               '/html/body/font/table[6]/tbody/tr[4]/td[1]').text
            common_application_pending = self.driver.find_element(By.XPATH,
                                                                  '/html/body/font/table[6]/tbody/tr[2]/td[2]').text
            contract_application_pending = self.driver.find_element(By.XPATH,
                                                                    '/html/body/font/table[6]/tbody/tr[3]/td[2]').text
            broker_application_pending = self.driver.find_element(By.XPATH,
                                                                  '/html/body/font/table[6]/tbody/tr[4]/td[2]').text
            property_ = self.driver.find_element(By.XPATH, '/html/body/font/table[7]/tbody/tr[2]/td[1]').text
            passenger_ = self.driver.find_element(By.XPATH, '/html/body/font/table[7]/tbody/tr[2]/td[2]').text
            household_goods = self.driver.find_element(By.XPATH, '/html/body/font/table[7]/tbody/tr[2]/td[3]').text
            private = self.driver.find_element(By.XPATH, '/html/body/font/table[7]/tbody/tr[2]/td[4]').text
            enterprise = self.driver.find_element(By.XPATH, '/html/body/font/table[7]/tbody/tr[2]/td[5]').text
            bipd_insurance_required = self.driver.find_element(By.XPATH,
                                                               '/html/body/font/table[8]/tbody/tr[2]/td[1]').text
            cargo_insurance_required = self.driver.find_element(By.XPATH,
                                                                '/html/body/font/table[8]/tbody/tr[3]/td[1]').text
            bond_insurance_required = self.driver.find_element(By.XPATH,
                                                               '/html/body/font/table[8]/tbody/tr[4]/td[1]').text
            bipd_insurance_onfile = self.driver.find_element(By.XPATH,
                                                             '/html/body/font/table[8]/tbody/tr[2]/td[2]').text
            cargo_insurance_onfile = self.driver.find_element(By.XPATH,
                                                              '/html/body/font/table[8]/tbody/tr[3]/td[2]').text
            bond_insurance_onfile = self.driver.find_element(By.XPATH,
                                                             '/html/body/font/table[8]/tbody/tr[4]/td[2]').text

            print("Got table data!")

        return {
            "US DOT": us_dot,
            "Docket Number": docket_number,
            "Legal Name": legal_name,
            "Business Address": buisness_address,
            "Telephone": telephone,
            "Mail Address": mail_address,
            "Common Authority Status": common_authority_status,
            "Contract Authority Status": contract_authority_status,
            "Broker Authority Status": broker_authority_status,
            "Common Application Pending": common_application_pending,
            "Contract Application Pending": contract_application_pending,
            "Broker Application Pending": broker_application_pending,
            "Property": property_,
            "Passenger": passenger_,
            "Household Goods": household_goods,
            "Private": private,
            "Enterprise": enterprise,
            "BIPD Insurance Required": bipd_insurance_required,
            "Cargo Insurance Required": cargo_insurance_required,
            "Bond Insurance Required": bond_insurance_required,
            "BIPD Insurance Onfile": bipd_insurance_onfile,
            "Cargo Insurance Onfile": cargo_insurance_onfile,
            "Bond Insurance Onfile": bond_insurance_onfile
        }

    def fill_form(self, data):
        print("Fill the form!")
        docs_url = "https://docs.google.com/forms/d/e/1FAIpQLSf8Cm_aNH1ITuV_xVmn3Smb3NEM_Y8a8fTVJx_dd7tiWVDiRA/viewform"
        self.driver.get(docs_url)
        print("Arrived at docs url!")
        while True:
            try:
                print("Entering data...")
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['US DOT'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Docket Number'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Legal Name'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Business Address'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Telephone'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Mail Address'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Common Authority Status'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Contract Authority Status'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[9]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Broker Authority Status'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[10]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Common Application Pending'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[11]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Contract Application Pending'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[12]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Broker Application Pending'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[13]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Property'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[14]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Passenger'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[15]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Household Goods'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[16]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Private'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[17]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Enterprise'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[18]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['BIPD Insurance Required'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[19]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Cargo Insurance Required'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[20]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Bond Insurance Required'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[21]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['BIPD Insurance Onfile'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[22]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Cargo Insurance Onfile'])
                self.driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[23]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                    data['Bond Insurance Onfile'])
                break
            except:
                print("Retrying...")
        # submit the form
        print("Submitting form...")
        self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
        while True:
            try:
                success = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[3]')
                if "Your response has been recorded." in success.text:
                    print("Success! 🎉🌟\n-----------------------------\n")
                    break
            except:
                print("Waiting for submission...")
                sleep(0.2)
