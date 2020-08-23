from time import sleep
from selenium import webdriver

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class InstaBot:

    def __init__(self, executable_path, firefox_binary, marionette=False):
        self.cap = DesiredCapabilities().FIREFOX
        self.cap["marionette"] = marionette
        self.browser = webdriver.Firefox(executable_path=executable_path,
                                         firefox_binary=firefox_binary)
        self.browser.get('https://www.instagram.com/')

    def __search(self, search_item):
        search = self.browser.find_element_by_css_selector("input[placeholder='Search']")
        search.send_keys(search_item)
        link_elems = self.browser.find_element_by_css_selector('a.yCE8d')
        link_elems.click()

    def __open_first_post(self):
        post = self.browser.find_element_by_css_selector("a")
        post.click()

    def __like_post(self):
        like = self.browser.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button')
        like.click()

    def __next_post(self):
        next_photo = self.browser.find_element_by_css_selector("a._65Bje.coreSpriteRightPaginationArrow")
        next_photo.click()

    def __follow_rec(self, i):
        if i < 10:
            followers_div = self.browser.find_element_by_css_selector("button.sqdOP.L3NKy.y3zKF")
            followers_div.click()
            sleep(1)
            self.__follow_rec(i + 1)

    # log in your account
    def log_in(self, username, password):
        username_input = self.browser.find_element_by_css_selector("input[name='username']")
        password_input = self.browser.find_element_by_css_selector("input[name='password']")

        username_input.send_keys(username)
        password_input.send_keys(password)

        login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()

    # like posts on hashtag
    def like_posts(self, hashtag):
        self.__search(hashtag)
        self.__open_first_post()
        for i in range(30):
            self.__like_post()
            self.__next_post()

    # follow accounts and like three post
    def follow_profiles(self, acc, limit):
        self.__search(acc)
        followers = self.browser.find_element_by_css_selector('a.-nal3 ')
        followers.click()

        for i in range(limit):
            div = self.browser.find_element_by_css_selector("div.PZuss")
            li_list = div.find_elements_by_css_selector("li")
            li_list[i].find_element_by_css_selector("a.FPmhX.notranslate._0imsa").click()
            if self.browser.find_elements_by_css_selector("div.v1Nh3.kIKUG._bz0w"):
                follow = self.browser.find_elements_by_css_selector("span.vBF20._1OSdk")[0]
                follow.click()
                post = self.browser.find_elements_by_css_selector("div.v1Nh3.kIKUG._bz0w")[0]
                post.click()
                if len(self.browser.find_elements_by_css_selector("div.v1Nh3.kIKUG._bz0w")) < 3:
                    self.__like_post()
                else:
                    for j in range(3):
                        self.__like_post()
                        self.__next_post()

                self.browser.find_elements_by_css_selector(
                    "div.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG")[0].click()
                self.__search(acc)
                followers = self.browser.find_element_by_css_selector('a.-nal3 ')
                followers.click()
            else:
                self.browser.back()


if __name__ == '__main__':
    ex_path = ''                    # path to geckodriver
    firefox_binary = ''             # path to firefox
    bot = InstaBot(ex_path, firefox_binary)
    bot.log_in("username", "password")
