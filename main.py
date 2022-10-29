"""
Author: Swapnil Shinde <Username:AtmegaBuzz>
contact: swapnilshinde9382@gmail.com
"""


from logging import exception
import os
import gspread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from config import (
    message,
    url,
    sleep_in_between,
    loading_sleep,
    ending_row
)
from random import randint
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from clean_sheet import clean_numbers

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
    worksheet = gsheet.get_worksheet(0)
    outgoing = gsheet.get_worksheet(1)
    
    phone_numbers = worksheet.col_values(1)[:ending_row]  # col of phone numbers
    names = worksheet.col_values(2)[:ending_row] # col of names
    ids = worksheet.col_values(3)[:ending_row] # col of ids

    for _ in range(len(phone_numbers)-len(names)):
        names.append("")
    
    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={os.path.join(os.getcwd(),'Selenium')}") 

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://web.whatsapp.com')

    
    try:
        while(True):
            WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div/canvas")))
            print("scan the code")
            sleep(4)
    except:
        print("scan not required")
        pass


    
    for index in range(done_till_counter,len(phone_numbers)):
        
        counter_file = open("count.txt","w",encoding="utf8")

        driver.get(f'https://web.whatsapp.com/send?phone=+{phone_numbers[index]}')

        try:
            for key in message:
                
                if(key.split(",")[0]=="message"):
                    
                    message_ = message[key].replace("<name>",names[index]).replace("<id>",ids[index])

                    type_box = WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]")))
                    
                    message_lines = message_.split("\n")
                    for message__ in message_lines:
                        type_box.send_keys(message__+Keys.SHIFT+Keys.ENTER)
                        sleep(randint(1,5))
                    # send
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"))).send_keys(Keys.RETURN)


                elif(key.split(",")[0]=="media"):
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div"))).click()
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input"))).send_keys(os.path.join(os.path.abspath("assets"),message[key]))
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div"))).click()
                                                                                    
                
                elif(key.split(",")[0]=="document"):
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div"))).click()
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[4]/button/input"))).send_keys(os.path.join(os.path.abspath("assets"),message[key]))
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div"))).click()
                                                

                else:
                    print("wrong key passed")
                    continue
                
                sleep(sleep_in_between)
                
            sleep(randint(10,20))
            print("done for",phone_numbers[index])
        except Exception as e:
            print(f"Failed for Number {phone_numbers[index]}",e)
            outgoing.append_row([phone_numbers[index],names[index],"failed"])
        finally:
            counter_file.write(f"{index+1}")

def __run_mainloop__():

    print("""
        1 = Send Whatsapp messages
        2 = Get already sended numbers
    """)

    choice = int(input("Choice: "))

    if choice==1:
        try:
            run_bot()
        except Exception as e:
            print("some err occured",e)
    elif choice==2:
        clean_numbers(url)

    else:
        print("invalid choice")

__run_mainloop__()
