from twitterUserInfo import username, password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class Twitter:
    def __init__(self, username, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en, n-US'})
        self.browser = webdriver.Chrome('chromedriver.exe', options=self.browserProfile)
        self.username = username
        self.password = password

    def signIn(self):
        self.browser.get('https://twitter.com/login')
        time.sleep(2)

        username_input = self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        username_input.send_keys(username)

        password_input = self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def search(self, hashtag):
        self.browser.maximize_window()
        time.sleep(2)

        searchInput = self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div''[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input')
        searchInput.send_keys(hashtag)
        time.sleep(2)

        searchInput.send_keys(Keys.ENTER)
        time.sleep(2)

        result = []

        list1 = self.browser.find_elements_by_xpath('//div[@data-testid="tweet"]/div[2]/div[2]')
        time.sleep(2)
        print('count: ' + str(len(list1)))

        for item in list1:
            result.append(item.text)

        loopCounter = 0
        last_height = self.browser.execute_script('return document.documentElement.scrollHeight')

        while True:
            if loopCounter > 5:
                break

            self.browser.execute_script('window.scrollTo(0,document.documentElement.scrollHeight);')
            time.sleep(2)
            new_height = self.browser.execute_script('return document.documentElement.scrollHeight')

            if last_height == new_height:
                break

            last_height = new_height
            loopCounter += 1

            list1 = self.browser.find_elements_by_xpath('//div[@data-testid="tweet"]/div[2]/div[2]')
            time.sleep(2)
            print('count: ' + str(len(list1)))

            for item in list1:
                result.append(item.text)

        count = 1
        for item in result:
            print(f'--------------------')
            print(f'{count}-{item}')
            count += 1
            print('**********************')

        count = 1
        with open('tweets.txt', 'w', encoding='utf-8') as file:
            for item in result:
                file.write(f'{count}- {item} + "\n"')
                count += 1

    def close_chrome(self):
        self.browser.close()


twitter = Twitter(username, password)

# login
twitter.signIn()

# search
twitter.search('bilgisayar')

twitter.close_chrome()
