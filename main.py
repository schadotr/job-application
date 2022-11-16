import os
import configparser
import run_bot
from send_mail import Sendmail
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

FILE_ATTRIBUTE_HIDDEN = 0x02

username = ""
password = ""


def write_hidden(file_name, data):
    """
    Cross platform hidden file writer.
    """
    with open(file_name, "w") as f:
        f.write(data)


def main():
    mail_object = Sendmail(username=username)
    html_text = """\
        <html>
            <body>
                <p>Hi <b>{}</b>,<br>
                    The bot has started your applications. You will recieve a duo push shortly!!
                </p>
            </body>
        </html>
        """.format(
        username
    )
    # mail_object.send_text_mail(
    #     html_text, "[Status of Job Applications]"
    # )
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.headless = False
    options.page_load_strategy = "normal"
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    run_bot.run_bot(username, password, driver)


if __name__ == "__main__":
    if os.path.isfile("credentials.txt"):
        config = configparser.ConfigParser(interpolation=None)
        config.read("credentials.txt")
        username = config.get("credentials", "username")
        password = config.get("credentials", "password")
    else:
        username = input("Enter username : ")
        password = input("Enter password : ")
        data = "[credentials]\nusername: {}\npassword: {}".format(username, password)
        write_hidden("credentials.txt", data)
    main()
