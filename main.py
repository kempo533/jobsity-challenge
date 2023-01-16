from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(options=chrome_options)

dict_list = []

for i in range(1,13):
    base_url = f'https://endeavor.org/catalyst/?_paged={i}/'
    driver.get(base_url)

    buttons = driver.find_elements(By.CLASS_NAME, 'js-accordion-button')

    companies = []

    # Get the other class name, which is the company name
    for button in buttons:
        company_name = button.get_attribute('class').split()[1]
        companies.append(company_name)

    for company in companies:
        print(f'Searching {company}')
        company_url = base_url + f'#{company}'
        driver.get(company_url)  
        time.sleep(1)

        funding_data = {}
        funding_data['company'] = company
        funding_data['fund'] = driver.find_element(By.CLASS_NAME, 'fund').text
        funding_data['financing-round'] = driver.find_element(By.CLASS_NAME, 'financing-round').text
        funding_data['year-invested'] = driver.find_element(By.CLASS_NAME, 'year-invested').text

        dict_list.append(funding_data)

driver.quit()

# Load data into a DataFrame to process it
df = pd.DataFrame(dict_list, dtype=object).fillna('')
df.to_csv(r"C:\Users\kemp5\Documents\Python Projects\web-scrapper-challenge\results.csv", index = False)

