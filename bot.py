"""
Author: Swapnil Shinde <Username:AtmegaBuzz>
contact: swapnilshinde9382@gmail.com
"""


import gspread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import os
from config import message,url,sleep_in_between, loading_sleep
from random import randint
from selenium.webdriver.chrome.options import Options

def completed_till()->int:

    '''
        return count of phone numbers which are done 
    '''
    try:
        with open("count.txt","r",encoding="utf8") as f:
            done_till_counter = f.read()
            if(done_till_counter.strip()==""):
                raise IOError
            
            done_till_counter = int(done_till_counter)

    except (FileNotFoundError,IOError):
        with open("count.txt","w",encoding="utf8") as f:
            done_till_counter = 0
            f.write("0")
    return done_till_counter

def run_bot():
    done_till_counter = completed_till()
    gc = gspread.service_account(filename="cred.json")
    gsheet = gc.open_by_url(url)
    worksheet = gsheet.worksheets()[0]
    phone_numbers = worksheet.col_values(1)
    names = worksheet.col_values(2)
    for _ in range(len(phone_numbers)-len(names)):
        names.append("")
    


    chrome_options = Options()
    path = os.path.join(os.getcwd(),"Selenium")
    chrome_options.add_argument(f"user-data-dir={path}") 
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument(f"user-data-dir=C:\\Users\\LENOVO\\Library\\Application Support\\Google\\Chrome\\wtsp") 
    chrome_options
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://web.whatsapp.com')

    
    try:
        while(True):
            WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div/canvas")))
            print("scan the code")
            sleep(5)
    except:
        print("scan not required")
        pass


    count = 0
    
    for index in range(done_till_counter,len(phone_numbers)):
        
        if(count==10):
            return True

        counter_file = open("count.txt","w",encoding="utf8")

        driver.get(f'https://web.whatsapp.com/send?phone=+{phone_numbers[index]}')
 
        for key in message:
            # sleep(100)
            if(key.split(",")[0]=="message"):
                
                message_ = message[key].replace("<name>",names[index])

                type_box = WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]")))
                
                message_lines = message_.split("\n")
                for message__ in message_lines:
                    type_box.send_keys(message__+Keys.SHIFT+Keys.ENTER)
                    # sleep(randint(1,5))
                # send
                WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"))).send_keys(Keys.RETURN)


            elif(key.split(",")[0]=="media"):
                WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div"))).click()
                WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input"))).send_keys(os.path.abspath("assets")+"\\"+message[key])
                WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div"))).click()
                                                                                
            
            elif(key.split(",")[0]=="document"):
                WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div"))).click()
                WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[4]/button/input"))).send_keys(os.path.abspath("assets")+"\\"+message[key])
                WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div"))).click()
                                            

            else:
                print("wrong key passed")
                continue
            
            sleep(sleep_in_between)
            
        counter_file.write(f"{index+1}")
        sleep(randint(10,20))
        print("done for",phone_numbers[index])



def __run_mainloop__():
    while(True):
        try:
            run_bot()
        except Exception as e:
            print("some err occured",e)
        sleep(50+randint(1,20))


__run_mainloop__()
