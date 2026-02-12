import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pyautogui

from browser.selectors import profile_drop_down, logout_btn, username_field, password_field, login_btn


def wait(sec):
    time.sleep(sec)

# remove emoji
def remove_non_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def scroll_to_element(driver, element_obj):
    # Execute JavaScript to scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView();", element_obj)

def add_adblocker_to_chrome(driver, extension_url):
    # Go to the Chrome Web Store URL of the desired extension
    driver.get(extension_url)
    # Wait for the page to load
    wait(5)  # Adjust time as needed

    actions = ActionChains(driver)
    try:
        # Find the "Add to Chrome" button
        add_to_chrome_button = driver.find_element(By.XPATH, '//button[span[contains(text(),"Add to Chrome")]]')

        # Click the "Add to Chrome" button
        add_to_chrome_button.click()

        wait(8)
        pyautogui.press('tab', presses=1)
        wait(1)

        # Use PyAutoGUI to press Enter to confirm "Add to Extension"
        pyautogui.press('enter')

        # Wait for the "Add Extension" confirmation dialog
        wait(5)

    except Exception as e:
        print(f"An error occurred: {e}")

def close_last_tab(driver):
    if len(driver.window_handles) > 1:
        # Close last tab
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()

        # Switch back to first tab
        driver.switch_to.window(driver.window_handles[0])

def close_all_but_the_first_one(driver):
    # count tabs
    tabs = driver.window_handles

    if len(tabs) > 1:
        # close all except the first tab
        for t in tabs[1:]:
            driver.switch_to.window(t)
            driver.close()

        driver.switch_to.window(tabs[0])

def install_add_blocker(driver):
    add_adblocker_to_chrome(driver,
                            "https://chromewebstore.google.com/detail/adblock-plus-free-ad-bloc/cfhdojbkjhnklbpkdaibdccddilifddb")
    wait(25)
    close_last_tab(driver)


def logout(driver):

    try:
        profile = driver.find_element(By.XPATH, profile_drop_down)
        # element exists → use it
        scroll_to_element(driver, profile)
        profile.click()
        wait(2)
        driver.find_element(By.XPATH, logout_btn).click()
        wait(5)
    except NoSuchElementException:
        # element does not exist → handle gracefully
        profile = None

def login(driver, user):
    try:
        driver.find_element(By.XPATH, profile_drop_down)
        # print("Already logged in → skipping login")
    except NoSuchElementException:
        # print("Not logged in → performing login")
        # Username
        username = driver.find_element(By.XPATH, username_field)
        scroll_to_element(driver, username)
        username.send_keys(user['username'])
        # Password
        driver.find_element(By.XPATH, password_field).send_keys(user['password'])
        driver.find_element(By.XPATH, login_btn).click()