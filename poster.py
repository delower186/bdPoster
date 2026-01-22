from browser import utilities
from browser.browser import chrome_driver
from browser.utilities import install_add_blocker, wait
from db.model import get_unposted_title_number, get_unposted_title_all
from generator import generate_article
from prompts import article_prompt
from importer.populate import category_descriptions


def post(total_number_of_articles, forum):
    driver = chrome_driver()
    driver.maximize_window()

    number_of_article_posted = 0

    try:
        # install add blocker
        install_add_blocker(driver)

    except Exception as e:
        print(e)


    # Get total number of articles to post
    total_unposted_titles = get_unposted_title_number(forum)

    # if total_number_of_articles greater than total_unposted_titles then set total_number_of_articles = total_unposted_titles
    if total_number_of_articles > total_unposted_titles:
       total_number_of_articles = total_unposted_titles

    # else continue posting one by one until equal to desired number of articles
    while total_number_of_articles >= number_of_article_posted:
        for title in get_unposted_title_all(forum, total_number_of_articles):
            try:
                content = generate_article(article_prompt,title['title'],category_descriptions[0][title['forum']])
                wait(5)
                # Open a new window
                utilities.close_all_but_the_first_one(driver)
                # Posting website url
                driver.get("https://www.bdchakri.com")
                wait(5)
            except Exception as e:
                print(e)
