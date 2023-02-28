from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from faker import Faker
from faker.providers import person
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import random
import string
import json
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager


class GenerateRandom:
    @staticmethod
    def random_char(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))

    @staticmethod
    def nonce(length=4):
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
                self.locale = config['locale']
        except FileNotFoundError:
            print("No config.json found")
        self.outlook_url = "https://outlook.live.com/owa/?nlp=1&signup=1"
        self.chrome_options = Options()
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--log-level=3')
        self.chrome_options.headless = True
        self.fake = Faker(self.locale)
        self.gen = GenerateRandom()

    def is_visible(self, locator, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, locator)))
            return True
        except:
            return False

    def get_proxy(self):
        with open(self.proxy_file) as f:
            proxies = f.readlines()
            proxy = random.choice(proxies)
            return str(proxy)

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

def make_outlook(self):
    try:
        print("Outlook-Bot in AutoBot series, Coded by Error Error")
        print("Generating new account...")
        with webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options) as self.driver:
            proxy = self.get_proxy()
            self.chrome_options.add_argument('--proxy-server=socks://{}'.format(proxy))
            self.driver.get(self.outlook_url)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, 'iSignupAction')))
            if self.is_visible("phoneCountry") is True:
                pass
            time.sleep(0.5)
            self.driver.find_element_by_id("phoneCountry").click()
            time.sleep(0.5)
            self.driver.find_element_by_id("phoneCountry").send_keys("United States")
            time.sleep(0.5)
            self.driver.find_element_by_id("phoneCountry").send_keys(u'\ue007')
            time.sleep(1)
            if self.is_visible("PhoneNumber") is True:
                pass
            phone = self.fake.phone_number()
            self.driver.find_element_by_id("PhoneNumber").send_keys(phone)
            if self.is_visible("iSignupAction") is True:
                pass
            time.sleep(0.5)
            self.driver.find_element_by_id("iSignupAction").click()
            time.sleep(2)
            if self.is_visible("id__0-0") is True:
                pass
            else:
                return False
            print('Solving Captcha')
            self.solve_captcha()
            time.sleep(10)
            if self.is_visible("idBtn_Back") is True:
                self.driver.find_element_by_id("idBtn_Back").click()
                username = self.gen.random_char(10) + self.gen.nonce()
                password_input = self.gen.random_char(10) + self.gen.nonce()
                print("Account created: " + username + "@outlook.com")
                
                # Fill in account details
                self.driver.find_element_by_id("FirstName").send_keys(self.fake.first_name())
                self.driver.find_element_by_id("LastName").send_keys(self.fake.last_name())
                birth_month = Select(self.driver.find_element_by_id("BirthMonth"))
                birth_month.select_by_index(random.randint(1, 12))
                birth_day = Select(self.driver.find_element_by_id("BirthDay"))
                birth_day.select_by_index(random.randint(1, 28))
                birth_year = Select(self.driver.find_element_by_id("BirthYear"))
                birth_year.select_by_index(random.randint(1, 90))
                self.driver.find_element_by_id("iSignupAction").click()
                time.sleep(2)
                gender = random.choice(["M", "F", ""])
                if gender == "M":
                    self.driver.find_element_by_id("OtherGender").click()
                elif gender == "F":
                    self.driver.find_element_by_id("Female").click()
                self.driver.find_element_by_id("iSignupAction").click()
                time.sleep(2)
                
                # Submit the form
                if self.is_visible("iOptinEmail") is True:
                    self.driver.find_element_by_id("iOptinEmail").click()
                time.sleep(1)
                if self.is_visible("iSignupAction") is True:
                    self.driver.find_element_by_id("iSignupAction").click()
                time.sleep(1)
if self.driver.current_url == "https://outlook.live.com/mail/0/inbox":
    print("Account created successfully!")
else:
    print("Error creating account.")


def solve_captcha(self):
    try:
        if self.is_visible("hipTemplateContainer") is True:
            while True:
                print("Waiting for captcha...")
                wait(2)
                if self.is_visible("hipTemplateContainer") is False:
                    break
            print("Solved captcha!")
    except Exception as e:
        print("Error solving captcha: " + str(e))

def start(self, count):
    try:
        for i in range(count):
            print("Creating account #" + str(i + 1))
            while True:
                created = self.make_outlook()
                if created is True:
                    break
                wait(5)
    except Exception as e:
        print(e)
if name == "main":
r = Register()
r.start(1) # Specify how many accounts to generate.
                                                                           
