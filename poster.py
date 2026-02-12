import random

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from browser.browser import chrome_driver
from browser.selectors import new_topic_field, subject_field, textarea_field, submit_btn
from browser.utilities import install_add_blocker, wait, close_all_but_the_first_one, login, scroll_to_element, logout
from browser.users import get_user
from database.model import get_unposted_title_number, get_unposted_title_all, update_title
from generator import generate_article
from prompts import article_prompt
from importer.populate import category_descriptions, forums, get_titles

driver = chrome_driver()

def driverQuit():
    driver.quit()

def get_category_description(forum):
    for category_description in category_descriptions:
        if list(category_description.keys())[0] == forum:
            return category_description[forum]

    return None

def get_random_forum():
    return random.choice(forums)

def post(total_number_of_articles):
    
    driver.maximize_window()

    number_of_article_posted = 0

    try:
        # install add blocker
        install_add_blocker(driver)

    except Exception as e:
        print(e)


    # # Get total number of articles to post
    # total_unposted_titles = get_unposted_title_number(forum)
    #
    # # if total_number_of_articles greater than total_unposted_titles then set total_number_of_articles = total_unposted_titles
    # if total_number_of_articles > total_unposted_titles:
    #    total_number_of_articles = total_unposted_titles

    # else continue posting one by one until equal to desired number of articles
    while number_of_article_posted < total_number_of_articles:

        # get random forum from available ones
        forum = get_random_forum()

        if get_unposted_title_number(forum) < 100:
           get_titles(forum)

        titles = get_unposted_title_all(forum, 1)
        print(forum)
        for title in titles:

            if number_of_article_posted >= total_number_of_articles:
                break

            try:
                content = generate_article(article_prompt,title['title'],get_category_description(forum))
                wait(5)
                # Open a new window
                close_all_but_the_first_one(driver)
                # Posting website url
                driver.get("https://www.bdchakri.com")
                wait(5)
                login(driver, get_user())
                wait(5)
                # Forum XPATH
                exp_forum = driver.find_element(By.XPATH, title['xpath'])
                scroll_to_element(driver, exp_forum)
                exp_forum.click()
                wait(3)
                driver.find_element(By.XPATH, new_topic_field).click()
                wait(2)
                subj = driver.find_element(By.XPATH, subject_field)
                scroll_to_element(driver, subj)
                # Subject
                subj.send_keys(title['title'])
                textarea = driver.find_element(By.XPATH, textarea_field)
                textarea.click()
                # check for duplicate
                wait(3)
                result = driver.find_element(By.ID, "prime_subject_check_ajax_results")
                if result.text.strip():
                    update_title(title['id'])
                    # go back to home
                    driver.find_element(By.XPATH, "//a[contains(text(),'Home')]").click()
                else:
                    scroll_to_element(driver, textarea)
                    textarea.send_keys(content)
                    driver.find_element(By.XPATH, submit_btn).click()
                    wait(5)
                    update_title(title['id'])
                    driver.find_element(By.XPATH, "//a[contains(text(),'Home')]").click()

                # count article posted
                number_of_article_posted += 1
                print(f"Number Article Posted : {number_of_article_posted}")
                # logout
                logout(driver)

            except NoSuchElementException as e:
                print(f"Location: post(), BackTrace: {e}")

    else:
        print(f"Posted Articles: {number_of_article_posted}")
