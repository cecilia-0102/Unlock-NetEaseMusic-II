# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00B0E7F1CB5D41DDFA0437DFD78EFA94F2A0C2C8C193BE337D16E6DED9851F32F8DF9C1DCE80E0D785930444998FD0FE6014A5A17A842B4F1CBCB9D7780C9740E7ABD4B4FBEA5A975E0FA14E246E7D9615B98BADCC05658D5248F7D73BA97C5464E251465607AF4889A8424E33BE8EFFCEB1296FFB109EF80482AE646D78EB415F11BF213ED62138BE8B4E0EB8C4F83AD4B5038C60C244442AB08A559E961B9C46F83D245FBDE69CF12C2FDDAD019A5251787E622E41293E7017699B771175F14C1A85C6417AAE885D1FD6630CFDD18B997D5F7E2690ABD4E7CA1C7A969494FF5EFE759354A2A617049E7A3C5972935DBC066F781E0736AF8C85E71236A9E3F9E76116565D95DBB6529C21AF89573486933A60D7FFFA040B9D68552EBAC9984CE471F7E70522143F035D6E4F13CAC0E0FBA789EF6FD9C9AC76823046916DFDD5AAB13FA48587A47C0467E313D41222946F448F327244FC5CB94E3C6620FDA6C542"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
