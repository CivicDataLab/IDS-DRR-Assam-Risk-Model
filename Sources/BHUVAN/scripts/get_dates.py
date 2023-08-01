from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

firefox_options = Options()
firefox_options.headless = True

bhuvan_url = "https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php?id=flood"

service = Service('/snap/bin/firefox.geckodriver')
driver = webdriver.Firefox(service=service, options=firefox_options)

# navigate to the desired website
driver.get(bhuvan_url)
time.sleep(5) #sleep for 5 secs as the website is defaulting to Delhi a few seconds after loading.
 
# The required dropdown of States is in an iframe. Switch to it to avoid NoSuchElement error
driver.switch_to.frame("toolid")

state_dropdown_element = Select(driver.find_element("id", "rf"))


# Select an option by its option value - Assam(id100_0)
state_dropdown_element.select_by_value('id100_0')

# All dates are under a div element with id  minus100
element = driver.find_element("id", "minus100")
# Get all the elements available with tag name 'p'
elements = element.find_elements(By.TAG_NAME, 'div')

dates = []
for e in elements:
    date = e.text.strip()
    date = date.replace(r'/','_')
    date = date.replace('Hr', '')
    date = date.replace('-', '_')
    date_parts = date.split('_')
    if len(date_parts) == 4:
        # The time is present in the string
        day, month, year, time = date_parts
        new_date_string = f'{year}_{day}_{month}_{time}'
    else:
        # The time is not present in the string
        day, month, year = date_parts
        new_date_string = f'{year}_{day}_{month}'
    
    dates.append(new_date_string)

print(dates)