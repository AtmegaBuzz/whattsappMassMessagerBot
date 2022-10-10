
'''
    Module will be used to clean duplicate already sent phonenumbers from a Spreadsheet

    Already sent phonenumbers are people who are already messaged by bot and currently their phone number
    is save in google contacts.

    so the google contact csv will be used to remove all duplicate ph numbers from give url in config.py

'''

import gspread 
import csv
from os.path import join



def clean_numbers(url):
   
    filename = join("assets",str(input("Saved Phone Csv: ")))


    gc = gspread.service_account(filename="cred.json")
    gsheet = gc.open_by_url(url)
    worksheet = gsheet.get_worksheet(0)
    phone_numbers = worksheet.col_values(1)


    # initializing the titles and rows list
    fields = []
    rows = []
    
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        fields = next(csvreader)
    
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
    
        # get total number of rows

    saved_phone_numbers = []
    found_save_numbers = []
    ph_indx = fields.index("Phone 1 - Value")
    for row in rows:
        saved_phone_numbers.append(row[ph_indx]) 

    for number in phone_numbers:
    
        if number in saved_phone_numbers:
            found_save_numbers.append(number)
        elif  "+"+number in saved_phone_numbers:
            found_save_numbers.append("+"+number)


    with open(join("assets","saved_number.txt"),'w') as f:
        
        for number in found_save_numbers:
            f.writelines(number+"\n")


    