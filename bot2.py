import configparser
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
from os.path import abspath, dirname, join
import os
import requests


path = join(dirname(abspath(__file__)))

logging.basicConfig(
    filename=join(path, "logs.log"),
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)
if not os.path.exists(join(path, "job_description")):
    os.makedirs(join(path, "job_description"))


def apply_to(driver, links, retry_list):
    global asuid, username
    for i in range(len(links)):
        logging.info(
            "Start application for Job ID : {}".format(
                parse_qs(urlparse(links[i]).query)["jobid"][0]
            )
        )
        driver.get(links[i])
        try:
            wait = WebDriverWait(driver, 300)
            html_source = driver.page_source
            job_title = wait.until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "jobtitleInJobDetails")
                )
            ).text
            job_title = job_title.replace(r'/', " ")
            job_br_id = wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "position3InJobDetails")
                )
            )[1].text
            if len(driver.find_elements(by=By.ID, value="appLbl")) > 0:
                with open(join(path, "applied_jobs.txt"), "a+") as file_writer:
                    parsed_url = urlparse(links[i])
                    applied_job_id = parse_qs(parsed_url.query)["jobid"][0]
                    file_writer.write(applied_job_id + "\n")
                    file_writer.close()
                try:
                    html_writer = open(
                        join(
                            path,
                            "job_description",
                            "{}.html".format(job_title + "_" + job_br_id),
                        ),
                        "a+",
                        encoding="utf-8"
                    )
                    html_writer.write(html_source)
                    html_writer.close()
                except e:
                    print(e)
                continue
            wait.until(
                EC.visibility_of_element_located((By.ID, "applyFromDetailBtn"))
            ).click()
            wait.until(EC.visibility_of_element_located((By.ID, "startapply"))).click()
            try:
                wait.until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "ui-checkbox"))
                ).find_element(By.CLASS_NAME, "checked")
            except Exception:
                wait.until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "ui-checkbox"))
                ).click()
            shownext = wait.until(EC.visibility_of_element_located((By.ID, "shownext")))
            driver.execute_script("arguments[0].scrollIntoView();", shownext)
            driver.execute_script("arguments[0].click();", shownext)
            wait.until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "ui-radio"))
            )[1].find_element(by=By.TAG_NAME, value="input").click()
            wait.until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "ui-radio"))
            )[2].find_element(by=By.TAG_NAME, value="input").click()
            wait.until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "ui-radio"))
            )[4].find_element(by=By.TAG_NAME, value="input").click()
            wait.until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "ui-radio"))
            )[7].find_element(by=By.TAG_NAME, value="input").click()
            # wait.until(
            #     EC.visibility_of_element_located((By.ID, "radio-44674-No"))
            # ).click()
            # wait.until(
            #     EC.visibility_of_element_located((By.ID, "radio-61829-No"))
            # ).click()
            wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "custom_44925_1291_fname_slt_0_44925-button_text")
                )
            ).click()
            wait.until(EC.visibility_of_element_located((By.ID, "ui-id-5"))).click()
            asuid_ = wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "custom_42313_1291_fname_txt_0")
                )
            ).get_attribute("value")
            if asuid_ != asuid:
                wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, "custom_42313_1291_fname_txt_0")
                    )
                ).send_keys(asuid)
            asurite = wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "custom_42236_1291_fname_txt_0")
                )
            ).get_attribute("value")
            if asurite != username:
                wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, "custom_42236_1291_fname_txt_0")
                    )
                ).send_keys(username)
            shownext = wait.until(EC.visibility_of_element_located((By.ID, "shownext")))
            driver.execute_script("arguments[0].scrollIntoView();", shownext)
            driver.execute_script("arguments[0].click();", shownext)
            wait.until(
                EC.visibility_of_element_located((By.ID, "AddResumeLink"))
            ).click()
            wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "profileBuilder"))
            )
            wait.until(
                EC.visibility_of_element_located((By.ID, "btnSelectedSavedRC"))
            ).click()
            wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "FileListPadding"))
            ).find_elements(By.CLASS_NAME, "rbtButtons")[-1].click()
            wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "Marginbottom20"))
            ).find_element(By.TAG_NAME, "button").click()
            driver.switch_to.default_content()
            cover_letter_link = wait.until(
                EC.visibility_of_element_located((By.ID, "AddCLLink"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", cover_letter_link)
            driver.execute_script("arguments[0].click();", cover_letter_link)
            wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "profileBuilder"))
            )
            wait.until(
                EC.visibility_of_element_located((By.ID, "btnSelectedSavedRC"))
            ).click()
            wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "ResumeList"))
            ).find_elements(By.CLASS_NAME, "rbtButtons")[-1].click()
            wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "Marginbottom20"))
            ).find_element(By.TAG_NAME, "button").click()
            driver.switch_to.default_content()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            shownext = wait.until(EC.visibility_of_element_located((By.ID, "shownext")))
            driver.execute_script("arguments[0].scrollIntoView();", shownext)
            driver.execute_script("arguments[0].click();", shownext)
            add_files_link = wait.until(
                EC.visibility_of_element_located((By.ID, "attachmentWidget"))
            ).find_element(By.CLASS_NAME, "UnderLineLink")
            driver.execute_script("arguments[0].scrollIntoView();", add_files_link)
            driver.execute_script("arguments[0].click();", add_files_link)
            wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "profileBuilder"))
            )
            wait.until(
                EC.visibility_of_element_located((By.ID, "btnSelectedSavedRC"))
            ).click()
            total_file_uploads = (
                wait.until(
                    EC.visibility_of_element_located(
                        (By.CLASS_NAME, "resumeListContainer")
                    )
                )
                .find_element(By.ID, "FileList")
                .find_elements(By.CLASS_NAME, "checkbox")
            )
            for checkbox in total_file_uploads:
                wait.until(EC.visibility_of(checkbox)).click()
            wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "Marginbottom20"))
            ).find_element(By.TAG_NAME, "button").click()
            driver.switch_to.default_content()
            shownext = wait.until(EC.visibility_of_element_located((By.ID, "shownext")))
            driver.execute_script("arguments[0].scrollIntoView();", shownext)
            driver.execute_script("arguments[0].click();", shownext)
            wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//h1[text()='References']",
                    )
                )
            )
            shownext = wait.until(EC.visibility_of_element_located((By.ID, "shownext")))
            driver.execute_script("arguments[0].scrollIntoView();", shownext)
            driver.execute_script("arguments[0].click();", shownext)
            wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//h1[text()='EEO Form - Gender and Hispanic/Latino']",
                    )
                )
            )
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            shownext = wait.until(EC.visibility_of_element_located((By.ID, "shownext")))
            driver.execute_script("arguments[0].scrollIntoView();", shownext)
            driver.execute_script("arguments[0].click();", shownext)
            wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//h1[text()='EEO form - Race']",
                    )
                )
            )
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            shownext = wait.until(EC.visibility_of_element_located((By.ID, "shownext")))
            driver.execute_script("arguments[0].scrollIntoView();", shownext)
            driver.execute_script("arguments[0].click();", shownext)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            save = wait.until(EC.visibility_of_element_located((By.ID, "save")))
            driver.execute_script("arguments[0].scrollIntoView();", save)
            driver.execute_script("arguments[0].click();", save)
        except Exception as e:
            print(e)
            logging.info(
                "Error occurred for Job ID : {}".format(
                    parse_qs(urlparse(links[i]).query)["jobid"][0]
                )
            )
            retry_list.add(links[i])
            continue
        try:
            logging.info(
                "Completed application for Job ID : {}".format(
                    parse_qs(urlparse(links[i]).query)["jobid"][0]
                )
            )
            html_writer = open(
                join(
                    path, "job_description", "{}.html".format(job_title + "_" + job_br_id)
                ),
                "a+",
                encoding="utf-8",
            )
            html_writer.write(html_source)
            html_writer.close()
            with open(join(path, "applied_jobs.txt"), "a+") as file_writer:
                parsed_url = urlparse(links[i])
                applied_job_id = parse_qs(parsed_url.query)["jobid"][0]
                file_writer.write(applied_job_id + "\n")
                file_writer.close()
        except e:
            continue
    return "Done"


def perform_login(USERNAME, PASSWORD, driver, login_attempt):
    if login_attempt == 5:
        exit()
    try:
        wait = WebDriverWait(driver, 300)
        driver.get("https://students.asu.edu/employment/search")
        driver.find_element(by=By.CSS_SELECTOR, value=".space-bot-md button").click()
        driver.find_element(by=By.ID, value="username").send_keys(USERNAME)
        driver.find_element(by=By.ID, value="password").send_keys(PASSWORD)
        wait.until(EC.presence_of_element_located((By.NAME, "submit"))).click()
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "duo_iframe")))
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "auth-button"))).click()
        driver.switch_to.default_content()
    except Exception as e:
        perform_login(USERNAME, PASSWORD, driver, login_attempt + 1)
        driver.close()
        driver.quit()


def run_job_lister(USERNAME, PASSWORD, driver):
    wait = WebDriverWait(driver, 300)
    perform_login(USERNAME, PASSWORD, driver, 0)
    wait.until(EC.presence_of_element_located((By.ID, "responsiveCandZoneLink")))

    applied_job_ids = set()
    if os.path.exists(join(path, "applied_jobs.txt")) is False:
        file_ = open(join(path, "applied_jobs.txt"), "a+")
        file_.close()
    with open(join(path, "applied_jobs.txt"), "r+") as file_writer:
        for line in file_writer:
            applied_job_ids.add(line.rstrip("\n"))

    driver.get("https://students.asu.edu/employment/search")
    driver.find_element(by=By.CSS_SELECTOR, value=".space-bot-md button").click()
    wait.until(
        EC.presence_of_element_located((By.ID, "searchControls_BUTTON_2"))
    ).click()
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "ladda-spinner")))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "SaveSearchLink")))
    totaljobs = driver.find_element(by=By.CLASS_NAME, value="sectionHeading").text[:3]
    links = []
    job_ids = set()
    for i in range(int(totaljobs)):
        if (i + 1) % 50 == 0:
            wait.until(EC.presence_of_element_located((By.ID, "showMoreJobs"))).click()
        link = wait.until(
            EC.presence_of_element_located((By.ID, "Job_" + str(i)))
        ).get_attribute("href")
        links.append(link)
        parsed_url = urlparse(link)
        job_id = parse_qs(parsed_url.query)["jobid"][0]
        job_ids.add(job_id)
    new_postings = job_ids.difference(applied_job_ids)
    print(len(new_postings))
    new_links = []
    for posting in new_postings:
        for link in links:
            if posting in link:
                new_links.append(link)
    return new_links


def run_bot(USERNAME, PASSWORD, driver):
    links = run_job_lister(USERNAME, PASSWORD, driver)
    retry_list = set()
    apply_to(driver, links, retry_list)
    retry_count = 0
    while len(retry_list) != 0:
        retry_copy = retry_list.copy()
        if retry_count == 3:
            break
        for job in retry_list:
            if apply_to(driver, list(retry_copy), retry_list) == "Done":
                retry_list.remove(job)
        retry_count = retry_count + 1
    driver.close()
    driver.quit()


username = ""
password = ""
asuid = ""


def write_hidden(file_name, data):
    """
    Cross platform hidden file writer.
    """
    with open(file_name, "w") as f:
        f.write(data)


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.headless = True
    options.page_load_strategy = "normal"
    options.add_experimental_option("detach", True)
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    except:
        driver.quit()
    run_bot(username, password, driver)


if __name__ == "__main__":
    if os.path.isfile(join(path, "credentials.txt")):
        config = configparser.ConfigParser(interpolation=None)
        config.read(join(path, "credentials.txt"))
        username = config.get("credentials", "username")
        password = config.get("credentials", "password")
        asuid = config.get("credentials", "asuid")
    else:
        username = input("Enter asurite : ")
        password = input("Enter password : ")
        asuid = input("Enter ASU ID : ")
        data = "[credentials]\nusername: {}\npassword: {}\nasuid: {}".format(
            username, password, asuid
        )
        write_hidden(join(path, "credentials.txt"), data)
    response = requests.get(
        "https://schadotr.pythonanywhere.com/auth?username={}".format(
            username
        )
    ).json()
    if response["isValid"] is False:
        exit()
    main()
