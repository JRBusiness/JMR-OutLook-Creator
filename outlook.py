from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import csv
from faker import Faker
from faker.providers import person
import random
import string
from time import sleep as wait
import sys
from pyvirtualdisplay import Display
import json
from urllib.request import urlretrieve
import requests
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import time
import os

class GenerateRandom:
    def random_char(self, y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))

    def nonce(self, length=4):
        return ''.join([str(random.randint(0, 9)) for i in range(length)])


class Register:
    def __init__(self):
        try:
            with open('config.json') as json_data_file:
                config = json.load(json_data_file)
                self.using_recover = config['recovery']
                self.user_password = config['user_password']
                self.proxy_file = config['proxyfile']
                self.ac_token = config['anticaptchatoken']
                self.headless = config['headless']
                self.password = config['password']
                self.locale = config['locale']
        except FileNotFoundError:
            print("No config.json found")
        self.outlook_url = "https://outlook.live.com/owa/?nlp=1&signup=1"
        self.chrome_options = Options()
        if sys.platform == "linux" or sys.platform == "linux2":
            self.exe_path = "drivers/chromedriver"
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--disable-gpu')
            display = Display(visible=0, size=(800, 800))
            display.start()
        else:
            self.exe_path = "drivers/chromedriver.exe"
        # chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")
        if self.headless == "True":
            self.chrome_options.add_argument('--headless')
        self.fake = Faker(self.locale)
        self.gen = GenerateRandom()

    def is_visible(self, locator, timeout=30):
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, locator)))
            return True
        except TimeoutException:
            return False

    def get_proxy(self):
        with open(self.proxy_file) as f:
            proxies = f.readlines()
            proxy = random.choice(proxies)
            return str(proxy)

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return True

    def make_outlook(self):
        try:
            print("Outlook-Bot in AutoBot series, Coded by JBusiness")
            print("Generating new account...")
            self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.exe_path)
            proxy = self.get_proxy()
            self.chrome_options.add_argument('--proxy-server=socks://{}'.format(proxy))
            self.driver.get(self.outlook_url)
            if self.page_has_loaded() is True:
                if self.is_visible("CredentialsPageTitle") is True:
                    pass
                    print('Page Loaded')
            first, last = self.fake.first_name().rstrip(), self.fake.last_name().rstrip()
            username = first + last + str(self.gen.nonce(5))
            password_input = self.user_password
            self.driver.find_element_by_id("MemberName").send_keys(username)
            if self.is_visible("iSignupAction") is True:
                pass
            wait(0.5)
            self.driver.find_element_by_id("iSignupAction").click()
            wait(2)
            if self.is_visible("PasswordInput") is True:
                    pass
            self.driver.find_element_by_id("PasswordInput").send_keys(password_input)
            if self.is_visible("iSignupAction") is True:
                    pass
            wait(0.5)
            self.driver.find_element_by_id("iSignupAction").click()
            wait(1)
            if self.is_visible("FirstName") is True:
                    pass
            self.driver.find_element_by_id("FirstName").send_keys(first)
            self.driver.find_element_by_id("LastName").send_keys(last)
            if self.is_visible("iSignupAction") is True:
                    pass
            wait(0.5)
            self.driver.find_element_by_id("iSignupAction").click()
            wait(1)
            if self.is_visible("Country") is True:
                    pass
            country = requests.get('https://ipapi.co/country_name/', proxies={"http": "socks://" + proxy}).text
            countrygeo = Select(self.driver.find_element_by_id("Country"))
            countrygeo.select_by_visible_text(str(country))
            indexm = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
            indexd = random.randint(1, 28)
            indexy = random.randint(1980, 2000)
            birthM = Select(self.driver.find_element_by_id("BirthMonth"))
            birthM.select_by_visible_text(random.choice(indexm))
            birthD = Select(self.driver.find_element_by_id("BirthDay"))
            birthD.select_by_visible_text(str(indexd))
            birthY = Select(self.driver.find_element_by_id("BirthYear"))
            birthY.select_by_visible_text(str(indexy))
            self.driver.find_element_by_id("iSignupAction").click()
            wait(5)
            img = self.driver.find_elements_by_tag_name("img")[4]
            src = img.get_attribute('src')
            filename = str(int(time.time())) + ".png"
            urlretrieve(src, filename)
            file = open(filename, 'rb')
            wait(0.5)
            client = AnticaptchaClient(self.ac_token)
            task = ImageToTextTask(file)
            job = client.createTask(task)
            print("Submitting Captcha")
            job.join()
            cap = job.get_captcha_text()
            file.close()
            os.remove(filename)
            wait(0.5)
            self.driver.find_element_by_tag_name("input").send_keys(cap)
            wait(3)
            self.driver.find_element_by_id("iSignupAction").click()
            print("{}@outlook.com:{}:{}".format(username, self.user_password, country))
            account = {"username": username + "@outlook.com", "password": self.user_password, "country": country}
            with open("output/outlook_accounts.csv", 'a', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(account[i] for i in account)
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


if __name__ == "__main__":
    threads = []
    regBot = Register()
    print("Outlook Creator -- Coded by JBusiness")
    baba = int(input("How many account would you like to create?" + "\n"))
    if regBot.password == "jmrevolution":
        with open(regBot.proxy_file) as f:
            proxies = f.readlines()
            for i in range(baba):
                regBot.make_outlook()
            print("Finished.")
    else:
        print("Incorrect Password")
