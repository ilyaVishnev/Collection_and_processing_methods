from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import random
from ordered_set import OrderedSet
import copy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
import win32clipboard
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient




options = webdriver.ChromeOptions()
service=Service('chromedriver.exe')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options,service=service)

driver.get('https://mail.yandex.ru/?uid=1016096068#inbox')
wait = WebDriverWait(driver, 15,ignored_exceptions=[StaleElementReferenceException,TimeoutException])

button_enter=wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='Button2 Button2_type_link Button2_view_default Button2_size_m']")))
button_enter.click()

driver.implicitly_wait(5)

tab_button=wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='AuthLoginInputToggle-type']")))
tab_button.click()

button_password=wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@class='Button2 Button2_size_l Button2_view_action Button2_width_max Button2_type_submit']")))

login=driver.find_element(By.XPATH,"//input[@class='Textinput-Control']")
login.send_keys('vish.ilha@yandex.ru')

button_password.click()

button_password=wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@class='Button2 Button2_size_l Button2_view_action Button2_width_max Button2_type_submit']")))

password=driver.find_element(By.XPATH,"//input[@class='Textinput-Control']")
password.send_keys('Pobeda12!')

button_password.click()

last_height = driver.execute_script("return document.body.scrollHeight")
my_emails=list()

def get_text_from_mail(driver,href):
    driver.get(href)
    wait = WebDriverWait(driver, 15,ignored_exceptions=[StaleElementReferenceException,TimeoutException])
    full_text=wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='MessageBody_body_pmf3j react-message-wrapper__body']"))).text

    driver.back()
    return full_text


while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    try:

        wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@class='_nb-button-content']"))).click()

    except TimeoutException as ex:
        break    
    time.sleep(2)
    if new_height == last_height:
        break
    last_height = new_height
list_mails=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='mail-MessageSnippet-Wrapper']")))
for mail in list_mails: 
    time.sleep(5)
    e_mail={}
    e_mail["от кого"]= mail.find_element(By.XPATH,".//span[@class='mail-MessageSnippet-FromText']").text
    e_mail["дата отправки"]=mail.find_element(By.XPATH,".//span[@class='mail-MessageSnippet-Item_dateText']").text
    e_mail["тема письма"]=mail.find_element(By.XPATH,".//span[@class='mail-MessageSnippet-Item mail-MessageSnippet-Item_subject']").text
    
    try:
        href = mail.find_element(By.XPATH,".//a[@class='mail-MessageSnippet js-message-snippet toggles-svgicon-on-important toggles-svgicon-on-unread']").get_attribute("href")
    except NoSuchElementException as ex:
        href = mail.find_element(By.XPATH,".//a[@class='mail-MessageSnippet js-message-snippet toggles-svgicon-on-important toggles-svgicon-on-unread mail-MessageSnippet_type_widget mail-MessageSnippet-WidgetSubscriptions']").get_attribute("href")
    e_mail["текст письма полный"]=get_text_from_mail(driver,href)      
    my_emails.append(e_mail)    
# print(len(my_emails))    
# print(my_emails)

client = MongoClient('localhost', 27017)
client.testdb['yandex_mail'].insert_many(my_emails)

