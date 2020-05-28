from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import csv
import re

#setting driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument('--disable-gpu')

#creating driver
driver = webdriver.Chrome(options=options)

url = "https://es.indeed.com"
driver.get(url)

wait = WebDriverWait(driver, 5)
#searching in a bar
search_bar = driver.find_element_by_name("q")
search_bar.clear()
#type your job, also the location is taken --> ex: data analyst dublin
keyword = "data analyst madrid"
search_bar.send_keys(keyword)
search_bar.send_keys(Keys.RETURN)

driver.current_url


links = []
while True:    
    new_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".jobtitle.turnstileLink ")))
    links.extend([l.get_attribute("href") for l in new_links])

    try: #EC needed as otherwise the element was not clickable
        next_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'agination')]/li[last()]/a")))
        #ActionChains is needed as Indeed opens a small window and it is needed to be closed to continue
        ActionChains(driver).move_to_element(next_page).click().perform()
    except TimeoutException:
        print("links scraped")
        break

positions = []
companies = []
days = []
conditions = []
for l in links:
    driver.get(l)
    positions.append(driver.find_element_by_xpath("//h3[contains(@class, 'jobsearch-JobInfoHeader-title')]").text)
    companies.append(driver.find_element_by_xpath("//div[contains(@class, 'icl-u-lg-mr--sm icl-u-xs-mr--xs')]").text)
    #release day
    meta = driver.find_element_by_xpath("//div[contains(@class, 'jobsearch-JobMetadataFooter')]").text
    #change días to days or your language translation
    release_date = "días"
    search = re.search(f"(\d+).*({release_date})", str(meta))
    if search:
        release = "".join([search.group(1)," ",search.group(2)])
    else:
        release = "today/yesterday"
    days.append(release)
    #my condition -- I wanted jobs that included python, change or add the conditions you'd like
    condition = "ython"
    if condition in driver.page_source:
        conditions.append("python")
    else:
        conditions.append("nop")

#saving in csv
with open('indeed.csv', 'w', newline='') as csvfile:
    fieldnames = ["job", "position", "company", "release day", "contains"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for link, position, company, release, condition in zip(links, positions, companies, days, conditions):
        writer.writerow({"job": link, "position":position, "company":company, "release day":release, "contains": condition})
print("csv file available")

    