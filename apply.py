from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.alert import Alert
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os


def apply_to(driver, links):
    for i in range(len(links)):
        driver.get(links[i])
        try:
            wait = WebDriverWait(driver, 300)
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
            wait.until(EC.visibility_of_element_located((By.ID, "shownext"))).click()
            wait.until(
                EC.visibility_of_element_located((By.ID, "radio-44674-No"))
            ).click()
            wait.until(
                EC.visibility_of_element_located((By.ID, "radio-61829-No"))
            ).click()
            wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "custom_44925_1291_fname_slt_0_44925-button_text")
                )
            ).click()
            wait.until(EC.visibility_of_element_located((By.ID, "ui-id-5"))).click()
            wait.until(EC.visibility_of_element_located((By.ID, "shownext"))).click()
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
            wait.until(EC.visibility_of_element_located((By.ID, "AddCLLink"))).click()
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
            wait.until(EC.visibility_of_element_located((By.ID, "shownext"))).click()
            wait.until(
                EC.visibility_of_element_located((By.ID, "attachmentWidget"))
            ).find_element(By.CLASS_NAME, "UnderLineLink").click()
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
            wait.until(EC.element_to_be_clickable((By.ID, "shownext"))).click()
            wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//h1[text()='References']",
                    )
                )
            )
            wait.until(EC.element_to_be_clickable((By.ID, "shownext"))).click()
            wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//h1[text()='EEO Form - Gender and Hispanic/Latino']",
                    )
                )
            )
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait.until(EC.element_to_be_clickable((By.ID, "shownext"))).click()
            wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//h1[text()='EEO form - Race']",
                    )
                )
            )
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait.until(EC.element_to_be_clickable((By.ID, "shownext"))).click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait.until(EC.element_to_be_clickable((By.ID, "save"))).click()
        except Exception as e:
            print(e)
        driver.get(links[i])
    return "Done"
