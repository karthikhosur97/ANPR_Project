#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import pyrebase
import pyrebase
import requests
import csv
import os
import csv
import datetime
from PIL import Image
from pprint import pprint
import re
from tkinter import *
from twilio.rest import Client
import os, io
from google.cloud import vision
import pandas as pd
from urllib.request import urlretrieve
import urllib


# In[2]:




class App:    
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
 
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
 
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
         
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
 
        self.window.mainloop()
        
        
        
    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("vehicleplate.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
 
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
 
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
        self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
            
         # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
 
    # Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
cv2.destroyAllWindows


window = Tk()

window.title("Welcome to Indian Number Plate details app")

window.geometry('650x900')


driver = webdriver.Chrome('./chromedriver')
counter = 0 
while counter<1:
    counter = counter + 1
    regions = ['in'] # Change to your country
    with open("vehicleplate.jpg", 'rb') as fp:
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
        
    driver.get("https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml")
    #driver.minimize_window()


    captcha = driver.find_element_by_id("capatcha").find_element_by_tag_name('img')
    src = captcha.get_attribute('src')
    print(src)
    urllib.request.urlretrieve(src, "captcha.jpg")
    

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken-2.json"

    client = vision.ImageAnnotatorClient()

    file_name = 'captcha.jpg'
    image_path = file_name

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # construct an iamge instance
    image = vision.types.Image(content=content)

    # annotate Image Response
    response = client.text_detection(image=image)  # returns TextAnnotation
    df = pd.DataFrame(columns=['locale', 'description'])

    texts = response.text_annotations
    for text in texts:
        df = df.append(
            dict(
                locale=text.locale,
                description=text.description
            ),
            ignore_index=True
        )

    print(df['description'][0])
    captcha = df['description'][0]
    
    print("Captcha : "+str(captcha)+"\n")
    
    os.remove("vehicleplate.jpg")


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


    time.sleep(1)
    search_button = driver.find_element_by_id('page-wrapper').find_element_by_tag_name('button')

    search_button.click()

    time.sleep(3)
    
    try:
        if driver.find_element_by_id('resultPanel').text:
            status = "Success"
            print("Find Information : "+status+"\n")
            
        rc_details = driver.find_element_by_id('rcDetailsPanel').text
        rc_details = rc_details.split("\n",1)[1];
        rc_details = rc_details.replace("1. ","")
        rc_details = rc_details.replace("Authority: ","Authority:\n")
        rc_details = rc_details.split("\n")
        rc_details = [s.replace(':','') for s in rc_details]
        rc_details = [s.replace(' / ','') for s in rc_details]
        rc_details = [s.replace('/','') for s in rc_details]
        
    except:
        A=1

    n = len(rc_details)

    print(rc_details)

    headers = []

    for i in range(len(rc_details)):
    
        if i%2 == 0:
            headers.append(rc_details[i])

    print(headers)
    def Convert(lst): 
        res_dct = {lst[i]: lst[i + 1] for i in range(0,n-1,2)} 
        return res_dct 
          
    rc_details_dict = Convert(rc_details)
    rc_details_json = json.dumps(rc_details_dict)
    print(rc_details_json)

    rc_details_json_obj = json.loads(rc_details_json)
    config = {
    "apiKey": "AIzaSyBW5g22CfUqejW2O4F_DinPCHFhfc4vJSU",
    "authDomain": "anpr-15ebf.firebaseapp.com",
    "databaseURL": "https://anpr-15ebf.firebaseio.com",
    "projectId": "anpr-15ebf",
    "storageBucket": "anpr-15ebf.appspot.com",
    "messagingSenderId": "114786024077",
    "appId": "1:114786024077:web:656f6b7f97c51dad9200c4",
    "measurementId": "G-0MGT6CYTEY"
    }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    data = {
            "Registering Authority":rc_details_json_obj["Registering Authority"],
            "Registration No":rc_details_json_obj["Registration No"],
            "Registration Date":rc_details_json_obj["Registration Date"],
            "Chassis No": rc_details_json_obj["Chassis No"],
            "Engine No":rc_details_json_obj["Engine No"],
            "Owner Name":rc_details_json_obj["Owner Name"],
            "Vehicle Class":rc_details_json_obj["Vehicle Class"],
            "Fuel": rc_details_json_obj["Fuel"],
            "MakerModel": rc_details_json_obj["MakerModel"],
            "FitnessREGN Upto": rc_details_json_obj["FitnessREGN Upto"],
            "MV Tax upto":rc_details_json_obj["MV Tax upto"],
            "Insurance Upto":rc_details_json_obj["Insurance Upto"],
            "PUCC Upto": rc_details_json_obj["PUCC Upto"],
            "Emission norms": rc_details_json_obj["Emission norms"],
            "RC Status": rc_details_json_obj["RC Status"]
          }


    with open("sample.json", "a") as outfile: 
        json.dump(data, outfile) 
    data_id = rc_details_json_obj["Registration No"]

    db.child("users").child(data_id).push(data)
    print("Data added to real time database ")
    
driver.quit()




lines = 0

for key in data:
    lines = lines + 5
    lbl1 = Label(window, text=key, font=("Arial Bold", 25), pady = 7)
    lbl1.grid(column=0, row=lines)
    
    if key =="RC Status":
        if data[key] == "ACTIVE":
            lbl2 = Label(window, text=data[key],font=("Arial Bold", 15),fg="Green")
            lbl2.grid(column=1, row=lines)
        else:
            lbl2 = Label(window, text=data[key],font=("Arial Bold", 15),fg="Red")
            lbl2.grid(column=1, row=lines)
    else:
        lbl2 = Label(window, text=data[key],font=("Arial Bold", 15))
        lbl2.grid(column=1, row=lines)
        
        
        
  

window.mainloop()

client = Client("AC1e3d17dbb7ea4eabcc58e5004d83e31a", "b6cdd3e3a68a2899a9b3cabe34e9b089")

message_to_send = "The Vehicle Number " + plate_no + " is in your area"
client.messages.create(to="+919611131081", 
                       from_="+12057076409", 
                       body=message_to_send)  


# In[64]:





# In[4]:





# In[ ]:




