#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import pyrebase
import requests
import csv
import datetime
from PIL import Image
from pprint import pprint
import os
import re

driver = webdriver.Chrome('./chromedriver')
path = "in/"
dirs = os.listdir( path )
headers = ['Registering  ','Registering Authority', 'Registration No', 'Registration Date', 'Chassis No', 'Engine No', 'Owner Name', 'Vehicle Class', 'Fuel', 'MakerModel', 'FitnessREGN Upto', 'MV Tax upto', 'Insurance Upto', 'PUCC Upto', 'Emission norms', 'RC Status','Financed']

for filename in dirs:
    
    abs_filename = os.path.basename(filename)
    print("File Name: "+abs_filename+"\n")
    abs_filename = 'in/'+str(abs_filename)
    regions = ['in'] # Change to your country
    with open(abs_filename, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token 541c8820aad4d36e3a80a71ede91658445ec47f1'})
    try:
        plate = response.json()
        plate_no = str(plate['results'][0]['plate'])   #Reg_no is captured 
        plate_no = plate_no.upper()
        
    except:
        plate_no = "NOT Recognized"
        
    s = str(plate_no)
        
    if re.match(r'^[A-Z]{2}[0-9]{1}[A-Z]{2}', s, flags=0):
        s = s[:2]+'0'+s[2:]
        
    elif re.match(r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{3}$', s, flags=0):
        s = s[:6]+'0'+s[6:]
    elif re.match(r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{2}$', s, flags=0):
        s = s[:6]+'00'+s[6:]
    elif re.match(r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{1}$', s, flags=0):
        s = s[:6]+'000'+s[6:]
                
    plate_no = s
    print("Plate No. : "+str(plate_no)+"\n")
        
    
    status = "Failure"
    fields = []
     
    dt_string = datetime.datetime.now()
    
    fields.append(dt_string)
    
    driver.get("https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml")
    #driver.minimize_window()

    captcha = str(driver.find_element_by_id("capatcha").text)
              
    print("Captcha : "+str(captcha)+"\n")
    
    fields.append(captcha)

    captcha = captcha.split()

    if captcha[0].isdigit():
        equation = str("".join(captcha))
        captcha_result = eval(equation)
    else:
        if str(captcha[3]) == "greater":
            captcha_result = max(int(captcha[4]),int(captcha[6]))
        else:
            captcha_result = min(int(captcha[4]),int(captcha[6]))
        
    reg_no_search_bar =driver.find_element_by_id('regn_no1_exact')
    captcha_search_bar =driver.find_element_by_id('txt_ALPHA_NUMERIC')    
    
    #Regno generator 
    

    reg_no_search_bar.send_keys(plate_no)
    captcha_search_bar.send_keys(captcha_result)
    
    
    print("Captcha Result : "+str(captcha_result)+"\n")

    fields.append(captcha_result)

    time.sleep(1)
    search_button = driver.find_element_by_id('page-wrapper').find_element_by_tag_name('button')

    search_button.click()

    time.sleep(6)
    
    if re.match(r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$', plate_no, flags=0):
        fields.append("Valid Number Plate")
    else:
        fields.append(" ")

    
    try:
        if driver.find_element_by_id('resultPanel').text:
            status = "Success"
            print("Find Information : "+status+"\n")
            fields.append(status)

        rc_details = driver.find_element_by_id('rcDetailsPanel').text
        rc_details = rc_details.split("\n",1)[1];
        rc_details = rc_details.replace("1. ","")
        rc_details = rc_details.replace("Authority: "," :\n")
        rc_details = rc_details.split("\n")
        rc_details = [s.replace(':','') for s in rc_details]
        rc_details = [s.replace(' / ','') for s in rc_details]
        rc_details = [s.replace('/','') for s in rc_details]

    
        for r in rc_details:
            if r not in headers:
                fields.append(r)
            
    except:
        fields.append(status)
        fields.append(" ")
        fields.append(plate_no)
        
        
        
        
        
 #write to csv file
    fields.subList(21, fields.size()).clear();

    with open(r'captcha_samples.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        print("Appended to CSV file \n")
        print("___________________________________________________________")
    time.sleep(1)
    
   
driver.quit()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




