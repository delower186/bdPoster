from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager




def chrome_driver():
    chrome_options = webdriver.ChromeOptions()

    # Optional: avoid detection, maximize window, disable GPU, etc.
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Chrome setup with proxy (if you have one)
    # chrome_options.add_argument("--proxy-server=http://your_proxy:port")
    # Chrome setup with proxy
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
