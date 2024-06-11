import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException


ID = os.getenv("IGUSER")
PASS = os.getenv("IGPASS")
TARGET_ACC = "annemar809"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


class InstaFollower:

    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        self.driver.get(f"https://www.instagram.com/{TARGET_ACC}")

        try:
            # Click on login button
            self.wait.until(ec.presence_of_element_located((
                By.XPATH,
                "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/section/nav/div[2]/div/div/div[2]/div/div/div[2]/div[1]/a"
            ))).click()
        except TimeoutException:
            pass

        # Enter Credentials and login
        self.wait.until(ec.presence_of_element_located((By.NAME, "username"))).send_keys(ID)
        self.wait.until(ec.presence_of_element_located((By.NAME, "password"))).send_keys(PASS)
        self.driver.find_element(
            By.XPATH,
            value="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button"
        ).click()

        # Deny Saving login info
        self.wait.until(ec.presence_of_element_located((
            By.XPATH,
            "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div"
        ))).click()

    def find_followers_and_follow(self):
        def follow(accounts):
            for account in accounts:
                try:
                    follow_button = account.find_element(By.TAG_NAME, value="button")
                    if follow_button.text == "Follow":
                        follow_button.click()
                    time.sleep(.5)
                except NoSuchElementException:
                    pass

        # Get total follower count
        tot_followers = int(self.wait.until(ec.presence_of_element_located((
            By.XPATH,
            "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span"
        ))).get_attribute("title").replace(",", ""))
        print(f"Total Followers: {tot_followers}")

        # Click on followers
        self.wait.until(ec.presence_of_element_located((
            By.XPATH,
            "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a"
        ))).click()

        # Get the scrollable window
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "_aano")))
        scroll = self.driver.find_element(By.CLASS_NAME, value="_aano")
        time.sleep(3)

        # Get the list of followers
        if len(scroll.find_elements(By.XPATH, value="div")) == 3:
            acc = scroll.find_elements(By.XPATH, value="div[2]/div/div")
            follow(acc)

        else:
            j = 0
            for i in range(round(tot_followers/12)):
                if i > 10:
                    break
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
                acc = scroll.find_elements(By.XPATH, value="div[1]/div/div")
                follow(acc[j:])
                j = len(acc)
                time.sleep(2)
                print(j)


bot = InstaFollower()
bot.login()
bot.find_followers_and_follow()
