#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pyrebase

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

auth= firebase.auth()


#get the valid email and password from the user
email = input("Please Enter Your Email : ")
password = input("Please Enter Your Password : ")

#and authenticate the user 
user = auth.create_user_with_email_and_password(email, password)
print("User Created Successfully")


# In[24]:


#get the valid email and password from the user
email = input("Please Enter Your Email : ")
password = input("Please Enter Your Password : ")


# In[32]:


firebase = pyrebase.initialize_app(config)

db = firebase.database()
data = {"name":"Parwiz Forogh"}

db.child("vehicles").push(data)
print("Data added to real time database ")

db = firebase.database()
data = {"name":"Parwiz Forogh"}

db.child("users").push(data)
print("Data added to real time database ")


# In[ ]:




