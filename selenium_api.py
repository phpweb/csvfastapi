import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from . import app
from app.models import *

driver_path = os.environ.get('CHROME_DRIVER_PATH', None)
tv_username = os.environ.get('TV_USERNAME', None)
tv_password = os.environ.get('TV_PASSWORD', None)
url = "https://www.tradingview.com/crypto-screener/#signin"
# tv_trend_csv_download_path = os.environ.get('TV_TREND_CSV_DOWNLOAD_PATH', None)
tv_trend_csv_download_path = app.config.get('TV_DOWNLOAD_PATH')


class SeleniumAutomation:
    def __init__(self):
        print('download path')
        print(app.config.get('TV_DOWNLOAD_PATH'))
        self.tv_trend_csv_download_path = app.config.get('TV_DOWNLOAD_PATH')
        self.chrome_options = webdriver.ChromeOptions()
        preferences = {"download.prompt_for_download": False,
                       "download.default_directory": self.tv_trend_csv_download_path,
                       "download.directory_upgrade": True,
                       "profile.default_content_settings.popups": 0,
                       "profile.default_content_setting_values.notifications": 2,
                       "profile.default_content_setting_values.automatic_downloads": 1
                       }
        self.chrome_options.add_experimental_option("prefs", preferences)
        self.driver = webdriver.Chrome(executable_path=driver_path, chrome_options=self.chrome_options)
        self.driver_path = os.environ.get('CHROME_DRIVER_PATH', None)
        self.tv_username = os.environ.get('TV_USERNAME', None)
        self.tv_password = os.environ.get('TV_PASSWORD', None)
        self.login_url = "https://www.tradingview.com/crypto-screener/#signin"

    def login(self):
        self.driver.get(self.login_url)
        self.driver.set_window_size(1920, 1057)
        self.driver.find_element_by_class_name("tv-signin-dialog").click()
        self.driver.find_element_by_class_name("js-show-email").click()
        self.driver.find_element_by_name('username').send_keys(self.tv_username)
        self.driver.find_element_by_name('password').send_keys(self.tv_password)
        self.driver.find_element_by_class_name('tv-button__loader').click()
        return self.driver

    def download_tv_trend_csv(self):
        self.login()
        element = self.driver.find_element_by_xpath('//div[@title="Export screener data to a CSV file"]')
        time.sleep(1)
        element.click()
        time.sleep(2)
        return self.driver

    def download_tv_trend_csv_2(self):
        self.login()
        self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".tv-screener-toolbar__button--filters"))))
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".tv-screener-search__input").send_keys("change")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".js-filter-field-change .tv-screener-dialog__selectbox-caption").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".tv-control-select__option:nth-child(3) > .tv-control-select__option-wrap").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".js-filter-field-change .tv-screener-dialog__filter-field-text").send_keys("5")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".js-filter-field-change15 > .tv-screener-dialog__filter-field-content").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".tv-dialog__close > svg").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".tv-screener-toolbar__button-icon--export").click()
        return self.driver

    def open_chart(self, driver):
        driver.execute_script("window.scrollTo(0,0)")
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Chart")))
        element.click()
        return driver

    def test_timeframe_5m(self, driver, ticker):
        driver.execute_script("window.scrollTo(0,0)")
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#header-toolbar-symbol-search > .js-button-text"))
        )
        element.click()

        ticker_select_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@id=\'overlap-manager-root\']/div/div/div[2]/div/div[2]/div/input"))
        )
        ticker_select_element.clear()
        time.sleep(1)
        print("ticker after clear")
        print(ticker)
        ticker_select_element.send_keys(ticker)
        time.sleep(1)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".itemRow-ZzQNZGNo:nth-child(1) > .symbolDescription-ZzQNZGNo"))
        )
        element.click()

        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#header-toolbar-intervals .value-2y-wa9jT"))
        )
        element.click()

        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(6) .label-2IihgTnv"))
        )
        element.click()

        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#header-toolbar-alerts > .js-button-text"))
        )
        element.click()

        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".js-main-series-select-wrap .tv-control-select__control-inner"))
        )
        element.click()

        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 ".i-opened .tv-dropdown-behavior__item:nth-child(2) > .tv-control-select__option-wrap"))
        )
        element.click()

        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".tv-control-textarea"))
        )
        element.click()

        # set web hook
        checkbox_element_label = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".tv-alert-dialog__fieldset-value-item:nth-child(4) .tv-control-checkbox__label"))
        )
        time.sleep(1)
        # checkbox_element_label.click()
        time.sleep(1)
        checkbox_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".tv-alert-dialog__fieldset-value-item:nth-child(4) .tv-control-checkbox__input"))
        )
        time.sleep(1)
        if checkbox_element.get_attribute('checked'):
            print('Check box is already selected')
        else:
            checkbox_element_label.click()

        time.sleep(1)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.NAME, "webhook-url"))
        )
        time.sleep(1)
        element.clear()
        time.sleep(1)
        element.send_keys("https://google.com")

        element = driver.find_element(By.CSS_SELECTOR, ".tv-control-textarea")
        actions = ActionChains(driver)
        actions.double_click(element).perform()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".tv-control-textarea").clear()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".tv-control-textarea").send_keys(
            "{    \"passphrase\": \"testmeast\",    \"time\": \"{{timenow}}\",    \"exchange\": \"{{exchange}}\",    \"ticker\": \"{{ticker}}\",    \"timeframe\": \"5m\",    \"bar\": {        \"time\": \"{{time}}\",        \"open\": \"{{open}}\",        \"high\": \"{{high}}\",        \"low\": \"{{low}}\",        \"close\": \"{{close}}\",        \"volume\": \"{{volume}}\"    },    \"strategy\": {        \"position_size\": \"{{strategy.position_size}}\",        \"order_action\": \"{{strategy.order.action}}\",        \"order_contracts\": \"{{strategy.order.contracts}}\",        \"order_price\": \"{{strategy.order.price}}\",        \"order_id\": \"{{strategy.order.id}}\",        \"market_position\": \"{{strategy.market_position}}\",        \"market_position_size\": \"{{strategy.market_position_size}}\",        \"prev_market_position\": \"{{strategy.prev_market_position}}\",        \"prev_market_position_size\": \"{{strategy.prev_market_position_size}}\"    }}")
        driver.find_element(By.CSS_SELECTOR, ".tv-button__loader").click()

    def download_csv_file_and_set_alerts(self):
        csv_file_driver = self.download_tv_trend_csv_2()
        csv_file_name = self.tv_trend_csv_download_path + 'crypto_' + datetime.today().strftime(
            '%Y-%m-%d') + '.csv'
        time.sleep(1)
        df = pd.read_csv(csv_file_name)
        df = df[(df['Moving Averages Rating'] == 'Strong Buy')]
        # df = df[(df['Description'] == 'BINANCE')]
        df = df[(df['Ticker'].str.endswith('USDT', na=False))]
        print(df)
        if len(df['Ticker']) > 0:
            driver = self.open_chart(csv_file_driver)
            for ticker in df['Ticker']:
                saved_signal = TvScreenerSignals.query.filter_by(symbol=ticker).first()
                persist_tv_screener_signals(symbol=ticker)
                if saved_signal is None:
                    time.sleep(2)
                    self.test_timeframe_5m(driver, ticker)
            time.sleep(3)
            driver.quit()

        os.remove(csv_file_name)
