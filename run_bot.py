from apply import apply_to
from send_mail import Sendmail
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.alert import Alert
from urllib.parse import urlparse
from urllib.parse import parse_qs
import os


def run_job_lister(USERNAME, PASSWORD, driver):
    wait = WebDriverWait(driver, 300)
    driver.get("https://students.asu.edu/employment/search")
    driver.find_element(
        by=By.CSS_SELECTOR, value=".space-bot-md button"
    ).click()
    driver.find_element(by=By.ID, value="username").send_keys(USERNAME)
    driver.find_element(by=By.ID, value="password").send_keys(PASSWORD)
    wait.until(EC.presence_of_element_located((By.NAME, "submit"))).click()
    wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "duo_iframe"))
    )
    wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "auth-button"))
    ).click()
    driver.switch_to.default_content()
    wait.until(
        EC.presence_of_element_located((By.ID, "responsiveCandZoneLink"))
    ).click()
    wait.until(EC.presence_of_element_located((By.ID, "dashBoard"))).click()
    wait.until(
        EC.presence_of_element_located((By.ID, "applicationTab"))
    ).click()
    try:
        wait.until(
            EC.invisibility_of_element_located(
                (By.CLASS_NAME, "ApplicationCounts")
            )
        )
        driver.find_elements(by=By.CLASS_NAME, value="applicationsSection")[
            0
        ].click()
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "CollapsedUnfinishedApplications")
            )
        )
        saved_job_element_list = driver.find_elements(
            by=By.CLASS_NAME, value="CollapsedUnfinishedApplications"
        )[
            len(
                driver.find_elements(
                    by=By.CLASS_NAME, value="CollapsedUnfinishedApplications"
                )
            )
            - 1
        ].find_elements(
            by=By.CLASS_NAME, value="jobCard"
        )
        for element in saved_job_element_list:
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "cardFooter"))
            ).find_elements(By.TAG_NAME, "a")[1].click()
        driver.find_elements(by=By.CLASS_NAME, value="applicationsSection")[
            0
        ].click()
    except Exception:
        print("An Exception Occurred!!")
    driver.find_elements(by=By.CLASS_NAME, value="applicationsSection")[
        1
    ].click()
    element_list = driver.find_elements(
        by=By.CLASS_NAME, value="CollapsedAppliedApplications"
    )[
        len(
            driver.find_elements(
                by=By.CLASS_NAME, value="CollapsedAppliedApplications"
            )
        )
        - 1
    ].find_elements(
        by=By.CLASS_NAME, value="jobCard"
    )
    applied_job_ids = set()
    for element in element_list:
        applied_job_ids.add(
            element.find_element(By.TAG_NAME, "h2").get_attribute("id")[17:]
        )
    driver.get("https://students.asu.edu/employment/search")
    driver.find_element(
        by=By.CSS_SELECTOR, value=".space-bot-md button"
    ).click()
    wait.until(
        EC.presence_of_element_located((By.ID, "searchControls_BUTTON_2"))
    ).click()
    wait.until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "ladda-spinner"))
    )
    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "SaveSearchLink"))
    )
    totaljobs = driver.find_element(
        by=By.CLASS_NAME, value="sectionHeading"
    ).text[:3]
    links = []
    with open("applied_jobs.txt", "a+") as f:
        for job in applied_job_ids:
            f.write(job + "\n")
        
    job_ids = set()
    for i in range(int(totaljobs)):
        if (i + 1) % 50 == 0:
            wait.until(
                EC.presence_of_element_located((By.ID, "showMoreJobs"))
            ).click()
        link = wait.until(
            EC.presence_of_element_located((By.ID, "Job_" + str(i)))
        ).get_attribute("href")
        links.append(link)
        parsed_url = urlparse(link)
        job_id = parse_qs(parsed_url.query)["jobid"][0]
        job_ids.add(job_id)
    print(len(job_ids))
    new_postings = job_ids.difference(applied_job_ids)
    new_links = []
    for posting in new_postings:
        for link in links:
            if posting in link:
                new_links.append(link)
    return new_links


def applications_complete(driver, USERNAME):
    driver.get("https://students.asu.edu/employment/search")
    driver.find_element(
        by=By.CSS_SELECTOR, value=".space-bot-md button"
    ).click()
    time.sleep(15)
    driver.find_element(by=By.ID, value="responsiveCandZoneLink").click()
    driver.find_element(by=By.ID, value="dashBoard").click()
    time.sleep(1)
    driver.find_element(by=By.ID, value="applicationTab").click()
    time.sleep(15)
    driver.save_screenshot("{}.png".format(USERNAME))


def run_bot(USERNAME, PASSWORD, driver):
    links = run_job_lister(USERNAME, PASSWORD, driver)
    print(links)
    # mail_object = Sendmail(username=USERNAME)
    # html_text = """\
    #             <html>
    #             <body>
    #                 <p>Hi <b>{}</b>,<br>
    #                 The bot will apply to {} jobs!!
    #                 </p>
    #             </body>
    #             </html>
    #         """.format(
    #     USERNAME, len(links)
    # )
    # mail_object.send_text_mail(html_text, "[Total no. of applications]")
    apply_to(driver, links)
    # applications_complete(driver, USERNAME)
    # mail_object.send_compelete_mail()
    driver.close()
    driver.quit()
