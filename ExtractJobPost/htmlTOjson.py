from attr import attrib
from bs4 import BeautifulSoup as bs


import re

import pandas as pd
import numpy as np

from datetime import date

from random import randint
from time import sleep

import datetime

e = datetime.datetime.now()

import json
import os
from os import path
os.chdir(r'D:\\code & projects\\python\\NLP\\ExtractJobPost')
# print(os.getcwd())

import sqlalchemy
# DB Connection
engine = sqlalchemy.create_engine('sqlite:///FragranceMonitor.db/')


def write_data(file, data):
    with open (file, "a", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Appending to the File
def append_data(filename, data):

    listObj = []
 
    # Check if file exists
    if path.isfile(filename) is False:
      raise Exception("File not found")
 
    # Read JSON file
    with open(filename) as fp:
        listObj = json.load(fp)
 
    # Verify existing list
    # print(listObj)

    # print(type(listObj))
 
    listObj.append(data)
 
    # Verify updated list
    # print(listObj)
 
    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file, 
                            indent=4,  
                            separators=(',',': '))
 
    print('Successfully appended to the JSON file')        

print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))

source = open("Job.html", "r", encoding="utf-8")
soup = bs(source, 'lxml')

try: # run this code
        
        
        # if we do not know where we are starting from
        #div = soup.findAll(name='code') 
        #for detail in div:
            #print(detail.name, detail.tag, detail.attrs)

        # Post
        tag = "div"
        attrib = {"id": "job-details"}

        div = soup.findAll(name=tag, attrs=attrib) 
        for detail in div:
            post = detail.text

            # match double space but not space at the end of a string followed by a new line
            pattern = "(?!\s\n)\s\s"
            stage1 = re.sub(pattern, '', post)

            # white space at start of string
            pattern = "^\s"
            stage2 = re.sub(pattern, '', stage1)

            # Lookahead conditional: eliminates blank lines and white space at start of string
            pattern = "^\s(?=\w)"
            stage3 = re.sub(pattern, '', stage2)

            # replace \n (new line) with \\n so text becomes JSON compliant.
            pattern = "\n"
            post = re.sub(pattern, '\\n', stage3).strip()

            # print(post)
        
        # Job Type
        tag = "li"
        attrib = {"class": "jobs-unified-top-card__job-insight"}

        results = []
        li = soup.findAll(name=tag, attrs=attrib) 
        for detail in li:
            # if we do not know where we are starting from
            # print(detail.name, detail.tag, detail.attrs)
            
            jobType = detail.text.strip()
            results.append(jobType)
            print(jobType)

        # # Sector
        # li class="jobs-unified-top-card__job-insight"
        # span


        # Position & Location
        # code style="display: none"
        # from json find title
        position = ""
        location = ""

        tag = "code"

        li = soup.findAll(name=tag) 
        for detail in li:
            # if we do not know where we are starting from
            # print(detail.name, detail.tag, detail.attrs)
            
            s = detail.text
            # print(s)
            data = json.loads(s)

            # check for parent key
            if "data" in data:
                # loop all internal keys
                for key in data["data"]:
                    # find the key we want
                    # Position
                    if key == "title":
                        position = data["data"]["title"]
                        print(position)

                    # Location
                    if key == "formattedLocation":
                        location = data["data"]["formattedLocation"]
                        print(location)

            # stop looping once data is found, to avoid errors
            if position and location:
                break

        # Company	
        # a class="ember-view t-black t-normal">
        tag = "a"
        attrib = {"class": "ember-view t-black t-normal"}

        a = soup.findAll(name=tag, attrs=attrib) 
        for detail in a:
            # if we do not know where we are starting from
            # print(detail.name, detail.tag, detail.attrs)
            
            company = detail.text.replace('\n','').strip()
            print(company)  


        jobType = results[0].split('·')[0].strip()
        
        # some lazy people leave this blank
        jobLevel = ""
        if all(char in results[0] for char in ['·']): 
            jobLevel = results[0].split('·')[1].strip()
        

        companySize	= results[1].split('·')[0].strip()
        sector = results[1].split('·')[1].strip()

        postDict = {"position": position, 
                    "jobType":jobType,
                    "jobLevel":jobLevel,
                    "company" : company, 
                    "sector":sector,
                    "companySize":companySize,
                    "location": location,
                    "jobType": jobType,
                    "post": post}

        append_data("SavedJobPosts.json", postDict)

except Exception as E:
    print(E)

else: # no exceptions, then run this code
    1


