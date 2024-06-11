import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

FORM_URL = "https://forms.gle/u8pWBL2z3Z6kftYj8"
PROPERTY_LISTING = "https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment&cityName=Mumbai&BudgetMin=10000"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


class DataEntryJobAutomation:

    def __init__(self):
        self.property_addresses = []
        self.property_prices = []
        self.property_links = []

    def get_listings(self):
        result = requests.get(PROPERTY_LISTING)
        soup = BeautifulSoup(result.text, "html.parser")

        self.property_addresses = [item.text.removeprefix("2 BHK Apartment for Rent in ") for item in soup.select(selector=".mb-srp__card--title")]
        self.property_prices = [item.text for item in soup.select(selector=".mb-srp__card__price--amount")]
        self.property_links = [item["href"] for item in soup.select(selector=".mb-srp__card__society--name")]

    def fill_form(self):
        driver = webdriver.Chrome(chrome_options)
        wait = WebDriverWait(driver, 10)
        driver.get(FORM_URL)

        for address, price, links in zip(self.property_addresses, self.property_prices, self.property_links):
            wait.until(ec.presence_of_element_located((By.ID, "i1")))
            driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(address)
            driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(price)
            driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(links)
            driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span").click()
            wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a"))).click()


data_entry = DataEntryJobAutomation()
data_entry.get_listings()
data_entry.fill_form()
