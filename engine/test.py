from cfg.config import config,CHROME_PATH
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime

print("TESTING")

wd_options = Options()
wd_options.add_argument("--headless")
# wd_options.add_argument('--no-sandbox')
wd_options.add_argument('--disable-dev-shm-usage')  

print("STARTING CHROME")

wd = webdriver.Remote(CHROME_PATH, DesiredCapabilities.CHROME,options=wd_options)
# wd = webdriver.Chrome("./engine/chromedriver.exe",options=wd_options)
source="https://ndh.vn"

pagination_url = config[source]["pagination_url"]
xpath_configuration = config[source]["xpath"]

page_url = pagination_url.format("cổ phiếu",2)

print("GETTING PAGE")

wd.get(page_url)
post_dates = wd.find_elements_by_xpath(xpath_configuration["post_dates"])

for post_date in post_dates:
    date_str = post_date.get_attribute("innerText")
    date_elements = date_str.split(" ")[1].split("/")

    now = datetime.datetime.now()
    if len(date_elements) == 0:
        date_elements.append(now.day)
    if len(date_elements) == 1:
        date_elements.append(now.month)
    if len(date_elements) == 2:
        date_elements.append(now.year)
    
    print(tuple([int(element) for element in date_elements]))