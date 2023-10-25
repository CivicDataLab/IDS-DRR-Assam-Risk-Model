#from WebDriver import WebDriver
from Utils import SeleniumScrappingUtils
import time 
import os
import warnings
from captcha import captcha
import pdb
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
import glob
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
warnings.filterwarnings("ignore", category=DeprecationWarning) 

year = sys.argv[1]
month = sys.argv[2]

month_start = str(int(month)-1)
month_end = str(int(month)-1)
if month_end in ['0','2','4','6','7','9','11']:
    date_end = '31'
elif month_end=='1':
    date_end='28'
else:
    date_end = '30'


if int(month)<10:
    month = '0'+str(month)
folder = year+'_'+str(month)
try:
    os.mkdir(os.getcwd()+'/Sources/TENDERS/scripts/scraper/scraped_recent_tenders/'+folder)
except:
    sys.exit(0)

try:
    os.mkdir(os.getcwd()+'/Sources/TENDERS/scripts/scraper/scraped_recent_tenders/concatinated_csvs')
except:
    pass

url = 'https://assamtenders.gov.in/nicgep/app?page=WebTenderStatusLists&service=page'
firefox_options = Options()
firefox_options.headless = True
service = Service('/snap/bin/firefox.geckodriver')
#browser = WebDriver()

os.chdir(os.getcwd()+"/Sources/TENDERS/scripts/scraper/scraped_recent_tenders")
dict_tables_type = {"Bids List": "Vertical","Technical Bid Opening Summary":"Horizontal",
                   "Technical Evaluation Summary Details":"Horizontal",
                    "Bid Opening Summary":"Horizontal",
                   "Finance Bid Opening Summary":"Horizontal",
                   "Financial Evaluation Bid List":"Vertical",
                   "Finance Evaluation Summary Details":"Horizontal",
                   "AOC":"Horizontal",
                   "Awarded Bids List":"Vertical",
                   "Tender Revocation List":"Vertical",
                   "Corrigendum Details":"Vertical"}

dict_tender_status = {'1': "To be Opened",
                      '2': "Technical Bid Opening",
                      '3': "Technical Evaluation",
                      '4': "Financial Bid Opening",
                      '5': "Financial Evaluation",
                      '6': "AOC",
                      '7': "Retender",
                      '8': "Cancelled"}

def captcha_input(xpath_image,xpath_input_text):
    captcha_text = captcha(browser,xpath_image)
    #pdb.set_trace()
    captcha_input_element = SeleniumScrappingUtils.get_page_element(browser,xpath_input_text)
    SeleniumScrappingUtils.input_text_box(browser, captcha_input_element,captcha_text)
    button = browser.find_element(By.XPATH, "//*[@id='Search']")
    button.click()
    invalid_string = browser.find_elements(By.CLASS_NAME,"error")
    if len(invalid_string)==0:
        pass
    else:
        while 'Invalid Captcha!' in invalid_string[0].text:
            captcha_text = captcha(browser,xpath_image)
            captcha_input_element = SeleniumScrappingUtils.get_page_element(browser,xpath_input_text)
            SeleniumScrappingUtils.input_text_box(browser, captcha_input_element,captcha_text)
            time.sleep(3)
            
            button = browser.find_element(By.XPATH, "//*[@id='Search']")
            button.click()

            invalid_string = browser.find_elements(By.CLASS_NAME,"error")
            if len(invalid_string)==0:
                break
            elif 'Invalid Captcha!' not in invalid_string[0].text:
                break
            else:
                pass

#Select tender status
for tender_status_id in range(6,7):
    browser = webdriver.Firefox(service=service, options=firefox_options)

    browser.get(url)
    wait = WebDriverWait(browser, 10)  # Wait up to 3 seconds
    tender_status_id = str(tender_status_id)
    print('tenderStatusid: ', dict_tender_status[tender_status_id])
    SeleniumScrappingUtils.select_drop_down(browser,'//*[@id="tenderStatus"]',tender_status_id) #3


    #Select date for tender scraping 
    #from date
    from_date_element = SeleniumScrappingUtils.get_page_element(browser, '//*[@id="frmSearchFilter"]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[3]/td[2]/a')
    from_date_element.click()
    #Select month - 0 means January
    SeleniumScrappingUtils.select_drop_down(browser,'//*[@id="Body"]/div[2]/div[1]/table/tbody/tr/td[2]/select',value=month_start)
    #Select year
    SeleniumScrappingUtils.select_drop_down(browser,'//*[@id="Body"]/div[2]/div[1]/table/tbody/tr/td[3]/select',value = year)
    #Select Date
    #SeleniumScrappingUtils.get_page_element(browser,'//*[@id="Body"]/div[2]/div[2]/table/tbody/tr[1]/td[7]').click()
    browser.find_element(By.XPATH, "//td[text()='1']").click()

    #to_date
    to_date_element = SeleniumScrappingUtils.get_page_element(browser, '//*[@id="frmSearchFilter"]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[3]/td[4]/a')
    to_date_element.click()
    #Select month
    SeleniumScrappingUtils.select_drop_down(browser,'//*[@id="Body"]/div[3]/div[1]/table/tbody/tr/td[2]/select',value=month_end)
    #Select year
    SeleniumScrappingUtils.select_drop_down(browser,'//*[@id="Body"]/div[3]/div[1]/table/tbody/tr/td[3]/select',value = year)
    #Select Date
    #SeleniumScrappingUtils.get_page_element(browser,'//*[@id="Body"]/div[3]/div[2]/table/tbody/tr[5]/td[3]').click()
    td_elements = browser.find_elements(By.XPATH, "//td[text()='{}']".format(date_end))
    td_elements[1].click()

    #break captcha
    captcha_input('//*[@id="captchaImage"]','//*[@id="captchaText"]')

    def scrape_view_more_details(browser,tender_id):
        view_more_details_element = SeleniumScrappingUtils.get_page_element(browser,'//*[@id="DirectLink"]')
        view_more_details_element.click()
        #time.sleep(3)
        #since we are opening the new window selenium needs to change the focus
    
        #all the table elements
        elem_not_found = True
        while elem_not_found:
            try:
                window_after = browser.window_handles[1]
                browser.switch_to.window(window_after)
                elem = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td')))
                elem_not_found = False
            except:
                pass
        tables = SeleniumScrappingUtils.get_multiple_page_elements(browser,'/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr/td/table')[0].find_elements(By.CSS_SELECTOR,"table")
        dict_table_section_head = {}
        for table_section_elements in tables:
            try:
                dict_table_section_head[table_section_elements.find_element(By.CLASS_NAME,"section_head").text] = table_section_elements
            except:
                continue
        for index, (keys, values) in enumerate(dict_table_section_head.items()):
            keys = keys.replace("/","")
            if keys == "Tender Documents":
                continue
            # elif keys == "Work /Item(s)":
            #     SeleniumScrappingUtils.extract_horizontal_table(values,tender_id +"_"+"Work_Item"+"_" + str(index),1)
            elif (keys.startswith("Cover Details") or keys == "Latest Corrigendum List" or keys.startswith("Other")):
                SeleniumScrappingUtils.extract_vertical_table(values,tender_id +"_"+keys+"_" + str(index),1)
            elif keys == "Payment Instruments":
                table_section = values.find_element(By.CSS_SELECTOR,"table")
                SeleniumScrappingUtils.extract_vertical_table(table_section,tender_id +"_"+keys+"_" + str(index),1)
            else:
                SeleniumScrappingUtils.extract_horizontal_table(values,tender_id +"_"+keys+"_" + str(index),1)
        path_to_save = "concatinated_csvs/"
        SeleniumScrappingUtils.concatinate_csvs(path_to_save,tender_id,dict_tender_status[tender_status_id])
        
        directory = os.getcwd()
        SeleniumScrappingUtils.remove_csvs(directory)
        window_after = browser.window_handles[0]
        browser.switch_to.window(window_after)

    def scrape_view_stage_summary(browser,tender_id,dict_tables_type):
        list_of_dict_tables_type = list(dict_tables_type.keys())
        SeleniumScrappingUtils.get_page_element(browser,'//*[@id="DirectLink_0"]').click()
        #time.sleep(3)
        
    
        #all the table elements
        elem_not_found = True
        while elem_not_found:
            try:
                window_after = browser.window_handles[1]
                browser.switch_to.window(window_after)
                elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'table_list')))
                sections = browser.find_elements(By.CLASS_NAME,"table_list")
                elem_not_found = False
            except:
                pass
        
        try:
            sections.append(browser.find_element_by_id("table_list"))
        except:
            pass
        try:
            sections.append(browser.find_element(By.CLASS_NAME,"list_table"))
        except:
            pass
        # elems = sections[0].find_elements_by_xpath('//a[@href]')
        # for index in elems:
        #     name = index.get_attribute("text")
        #     if ".pdf" in name or "BOQ Comparative Chart" in name:
        #         index.click()
        #         time.sleep(10)
        #         name = index.get_attribute("text").replace("/t","").replace("/n","").replace(" ","").replace("\t","").replace("\n","")
        #         if "BOQComparativeChart" in name:
        #             os.rename(name+".xlsx","concatinated_csvs/"+tender_id+"_"+name+".xlsx")
        #         else:
        #             try:
        #                 os.rename(name,"concatinated_csvs/"+tender_id+"_"+name)
        #             except:
        #                 time.sleep(50)
        #                 os.rename(name,"concatinated_csvs/"+tender_id+"_"+name)
        for index,name in enumerate(sections):
            if index == 0:
                SeleniumScrappingUtils.extract_horizontal_table(name,"Org_"+tender_id,0)
                continue 
            header_name = name.find_element(By.CLASS_NAME,"section_head").text
            if (header_name in list_of_dict_tables_type) & (dict_tables_type[header_name] == "Vertical"):
                SeleniumScrappingUtils.extract_vertical_table(name,header_name+"_"+tender_id,1)
            else:
                SeleniumScrappingUtils.extract_horizontal_table(name,header_name+"_"+tender_id,1)
        path_to_save = "concatinated_csvs/"
        try:
            SeleniumScrappingUtils.concatinate_csvs(path_to_save,"summary"+"_"+tender_id, dict_tender_status[tender_status_id])
        except:
            pass


        
    def get_table_links(browser,table_xpath):
        #pdb.set_trace()

        table = SeleniumScrappingUtils.get_page_element(browser,table_xpath)
        elements_list = table.find_elements(By.CSS_SELECTOR,"a")
        links = [element.get_attribute("href") for element in elements_list]
        rows = table.find_elements(By.CSS_SELECTOR,"tr")
        tender_ids = [row.find_element("xpath","td[2]").text for row in rows[1:-2]]
        try:
            next_page_link = table.find_elements("xpath",'//*[@id="loadNext"]')[0].get_attribute("href")
        except:
            next_page_link = ''
        return table,links,next_page_link,tender_ids

    def scrapeTender(browser,tender_ids,links,dict_tables_type,flag=None,):
        #pdb.set_trace()
        if (len(tender_ids) == 10)&(len(links)==10):
            pass
        else:
            links = links[:len(tender_ids)]
        #pdb.set_trace()
        for index,link in enumerate(links):
            browser.get(link)
            scrape_view_more_details(browser,tender_ids[index])
            scrape_view_stage_summary(browser,tender_ids[index],dict_tables_type)

            os.chdir("concatinated_csvs/")
            SeleniumScrappingUtils.concatinate_csvs("../{}/".format(folder),"final_"+tender_ids[index], dict_tender_status[tender_status_id])
            directory = os.getcwd()
            SeleniumScrappingUtils.remove_csvs(directory)
            os.chdir("../")
            directory = os.getcwd()
            SeleniumScrappingUtils.remove_csvs(directory)
        # SeleniumScrappingUtils.get_page_element(browser,'//*[@id="PageLink_20"]').click()

    if __name__ == "__main__":
            tender_ids_list = []
            table,links,next_page_link,tender_ids = get_table_links(browser,'//*[@id="tabList"]')
            scrapeTender(browser,tender_ids,links,dict_tables_type,"first")
            # try:
            #     scrapeTender(browser,tender_ids,links,dict_tables_type,"first")
            # except:
            #     print('Error1')
            #     pdb.set_trace()
            #     pass
            while len(next_page_link):
                print("next")
                browser.get(next_page_link)
                table,links,next_page_link,tender_ids = get_table_links(browser,'//*[@id="tabList"]')
                scrapeTender(browser,tender_ids,links,dict_tables_type)
                # try:
                #     scrapeTender(browser,tender_ids,links,dict_tables_type)
                # except:
                #     print('Error2')
                #     pdb.set_trace()
                #     pass
            browser.quit()