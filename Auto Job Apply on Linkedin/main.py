import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def close_popup():
    """Closes the popup window"""
    try:
        wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/button"))).click()
    except StaleElementReferenceException:
        wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/button"))).click()


user_id = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
job_title_keyword = input("What type of job you are looking for?\n").replace(" ", "%20")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"https://www.linkedin.com/jobs/search/?currentJobId=3728098089&f_AL=true&geoId=102713980&keywords={job_title_keyword}&location=India&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true")
wait = WebDriverWait(driver=driver, timeout=5, ignored_exceptions=[StaleElementReferenceException])

# Click sign in button
driver.find_element(By.XPATH, value="/html/body/div[1]/header/nav/div/a[2]").click()

# Sign in
wait.until(ec.presence_of_element_located((By.ID, "username"))).send_keys(user_id)
driver.find_element(By.ID, value="password").send_keys(password)
driver.find_element(By.XPATH, value='//*[@id="organic-div"]/form/div[3]/button').click()

# All the jobs listed
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[1]/div/ul/li[25]")))
jobs_list = driver.find_elements(By.XPATH, value="/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[1]/div/ul/li")

total_applications_submitted = 0
for i, job in enumerate(jobs_list):
    wait.until(ec.element_to_be_clickable(job)).click()
    wait.until(ec.element_to_be_clickable(job)).click()
    print(f"Job: {i + 1}")

    try:  # Find easy apply button
        # Easy apply button
        wait.until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/button"))).click()
        print("Try 1: (a)")
    except TimeoutException:  # If not found then goto next job
        print("Except 1: (a)")
        continue

    try:  # Go through the info and resume page
        # Contact info next button
        driver.find_element(By.XPATH, value="/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button").click()
        print("Try 2: (a)")
        # Resume page next button
        driver.find_element(By.XPATH, value="/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]").click()
        print("Try 2: (b)")
    except NoSuchElementException:  # If submit button is available then submit the application and got next job
        try:
            # Uncheck follow button
            driver.find_element(By.XPATH, value="/html/body/div[3]/div/div/div[2]/div/div/form/footer/div[1]/label").click()
            print("Except 2: (a)")
            # Submit application button
            driver.find_element(By.XPATH, value="/html/body/div[3]/div/div/div[2]/div/div/form/footer/div[3]/button").click()
            print("Application Successful")
            print("Except 2: (b)")
            time.sleep(1)
            close_popup()
            print("Except 2: (c)")
            total_applications_submitted += 1
            continue
        except NoSuchElementException:
            print("Except 2: (d)")
            continue

    try:  # Submit the application
        # Uncheck follow button
        driver.find_element(By.XPATH, value="/html/body/div[3]/div/div/div[2]/div/div[2]/div/footer/div[1]/label").click()
        print("Try 3: (a)")
        # Submit application button
        driver.find_element(By.XPATH, value="/html/body/div[3]/div/div/div[2]/div/div[2]/div/footer/div[3]/button[2]").click()
        print("Application Successful")
        print("Try 3: (b)")
        time.sleep(1)
        close_popup()
        print("Try 3: (c)")
        total_applications_submitted += 1
    except NoSuchElementException:  # If submit button is not available then close the window and discard the contents
        close_popup()
        print("Except 3: (a)")
        # Discard
        driver.find_element(By.XPATH, value="/html/body/div[3]/div[2]/div/div[3]/button[1]").click()
        print("Except 3: (b)")

print(f"{total_applications_submitted=}")
