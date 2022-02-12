import time
from datetime import datetime
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from config import get_settings


class LoginOnly:
    def __init__(self):
        self.settings = get_settings()
        service = Service(self.settings.chrome_driver_path)
        self.tv_trend_csv_download_path = self.settings.tv_trend_csv_download_path
        self.csv_file_name_volume_15m = self.tv_trend_csv_download_path + 'crypto_' + datetime.today().strftime(
            '%Y-%m-%d') + '.csv'
        preferences = {"download.prompt_for_download": False,
                       "download.default_directory": self.tv_trend_csv_download_path,
                       "download.directory_upgrade": True,
                       "profile.default_content_settings.popups": 0,
                       "profile.default_content_setting_values.notifications": 2,
                       "profile.default_content_setting_values.automatic_downloads": 1
                       }
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_experimental_option("prefs", preferences)

        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)

        self.vars = {}
        self.screener_login_url = "https://www.tradingview.com/crypto-screener/#signin"
        self.general_login_url = "https://www.tradingview.com/"
        self.tv_username = "ramentwickler"
        self.tv_password = "Hasan1020!"

    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def for_general_login(self):
        self.driver.get(self.general_login_url)
        self.driver.set_window_size(1920, 1055)
        self.driver.find_element(By.CSS_SELECTOR, ".tv-header__user-menu-button > svg").click()
        time.sleep(0.500)
        self.driver.find_element(By.CSS_SELECTOR, ".item-2IihgTnv").click()
        time.sleep(0.500)
        self.driver.find_element(By.CSS_SELECTOR, ".js-show-email").click()
        self.driver.find_element(By.NAME, "username").send_keys(self.tv_username)
        self.driver.find_element(By.NAME, "password").send_keys(self.tv_password)
        self.driver.find_element(By.CSS_SELECTOR, ".tv-button__loader").click()

    def another_one_for_screener_login(self):
        self.driver.get(self.screener_login_url)
        self.driver.set_window_size(1920, 1057)
        self.driver.find_element(By.CSS_SELECTOR, ".tv-signin-dialog").click()
        self.driver.find_element(By.CSS_SELECTOR, ".js-show-email").click()
        self.driver.find_element(By.NAME, 'username').send_keys(self.tv_username)
        self.driver.find_element(By.NAME, 'password').send_keys(self.tv_password)
        self.driver.find_element(By.CSS_SELECTOR, '.tv-button__loader').click()
        return self.driver

    def download_tv_trend_csv(self):
        # self.login()
        # element = self.driver.find_element_by_xpath('//div[@title="Export screener data to a CSV file"]')
        element = self.driver.find_element(By.XPATH, '//div[@title="Export screener data to a CSV file"]')
        time.sleep(1)
        element.click()
        time.sleep(2)
        return self.driver

    def download_oscillators_csv(self, time_frame='15 minutes'):
        time.sleep(1)
        element = self.driver.find_element(By.XPATH, '//div[@data-set="oscillators"]')
        element.click()
        time.sleep(1)
        element = self.driver.find_element(By.XPATH, '//div[@title="Time Interval"]')
        time.sleep(1)
        element.click()
        time.sleep(1)
        element = self.driver.find_element(By.XPATH, f'//div[@title="{time_frame}"]')
        time.sleep(1)
        element.click()
        time.sleep(2)
        element = self.driver.find_element(By.XPATH, '//div[@title="Export screener data to a CSV file"]')
        time.sleep(1)
        element.click()
        time.sleep(2)
        return self.driver

    def download_relative_volume_trends(self, time_frame='15 minutes'):
        self.another_one_for_screener_login()
        sleep_time = 0.5
        time.sleep(sleep_time)
        element = self.driver.find_element(By.XPATH, '//div[@title="Screens"]')
        element.click()
        # element = self.driver.find_element(By.XPATH, '//span[text()="VolumeFxCanli"]')
        element = self.driver.find_element(By.XPATH, '//div[@data-set="2806115"]')
        element.click()
        element = self.driver.find_element(By.XPATH, '//div[text()="VolumeFxCanli"]')
        time.sleep(sleep_time)
        element.click()
        time.sleep(sleep_time)
        element = self.driver.find_element(By.XPATH, '//div[@title="Time Interval"]')
        time.sleep(sleep_time)
        element.click()
        time.sleep(sleep_time)
        element = self.driver.find_element(By.XPATH, f'//div[@title="{time_frame}"]')
        time.sleep(sleep_time)
        element.click()
        # time.sleep(sleep_time)
        element = self.driver.find_element(By.XPATH, '//div[@title="Export screener data to a CSV file"]')
        # time.sleep(sleep_time)
        element.click()
        return self.driver

    def download_csv_file_and_set_alerts_volume_15m(self):
        self.download_relative_volume_trends()
        time.sleep(2)
        self.driver.quit()
        df = pd.read_csv(self.csv_file_name_volume_15m)
        df = df[(df['Ticker'].str.endswith('USDT', na=False))]
        df = df[(df['Moving Averages Rating'] == 'Strong Buy')]
        print(df)
        os.remove(self.csv_file_name_volume_15m)
        # if len(df['Ticker']) > 0:
        #     driver = self.open_chart(csv_file_driver)
        #     for ticker in df['Ticker']:
        #         saved_signal = TvScreenerSignals.query.filter_by(symbol=ticker).first()
        #         persist_tv_screener_signals(symbol=ticker)
        #         if saved_signal is None:
        #             time.sleep(2)
        #             self.test_timeframe_5m(driver, ticker)
        #     time.sleep(3)
        #     driver.quit()


# lg = LoginOnly()
# print(lg.tv_trend_csv_download_path)
# lg.test_lavida()
# lg.another_one_for_screener_login()
# lg.download_tv_trend_csv()
# lg.download_oscillators_csv()
# lg.download_relative_volume_trends()
# lg.download_csv_file_and_set_alerts_volume_15m()
