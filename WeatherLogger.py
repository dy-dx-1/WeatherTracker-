from bs4 import BeautifulSoup
import requests
import re
from useful_functions import clean_tags, whitespace_destroyer
import openpyxl
from datetime import datetime


URL = "https://weather.gc.ca/city/pages/qc-147_metric_e.html"  # URL of site

# Getting the html info of the page and storing it
web_page = requests.get(url=URL)

# Getting the 'clean' hmtl code with soup
soup = BeautifulSoup(web_page.content, 'html.parser')

# we are looking for the 'most close to surface' way to get to what we want, if you take a too precise id, soup won't see it
week_data = soup.find(id='container')
# and you will get 'None' when trying to .find, so just open inspector and don't use the pointer, move around in the preopened <div>¨until you find the one that contains
# what you want with all the other stuff to filter out after

# find all the data inside the things with the class (here this class represents
data_for_day = week_data.find_all(class_='col-sm-4 brdr-rght-city')
# the 2 first 'boxes' of info)

# VERY IMPORTANT - TOOK 2 HOURS. Use return to then be able to assign the result to data 1 / see useful functions.py
data1 = clean_tags(data_for_day)

# Since the class is diff for the last square of info
data_for_day = week_data.find_all(class_="dl-horizontal wxo-conds-col3")
# no need to do first loop cause there will be only one box (square with info) with this class

data2 = clean_tags(data_for_day)

filtered_total = (str(data1).strip() + str(data2.strip())).strip()
filtered_total = whitespace_destroyer(filtered_total) 
# Now, let's get the important stuff and put it in variables
# premier item est la température, deuxième le dew point
infoDict = {}

info = re.findall(r'Temperature:(.+?)°C', filtered_total)
infoDict["Temperature"] = info[0]

info = re.findall(r'Condition:(\w+)Pressure:', filtered_total)
infoDict["Condition"] = info[0]

info = re.findall(r"Pressure:(\d+\.\d{1,2}kPa)", filtered_total)
infoDict["Pressure"] = info[0]

info = re.findall(r"Humidity:(\d{2}%)", filtered_total)
infoDict["Humidity"] = info[0]

info = re.findall(r"Wind:(\w{1,3}.+?km/h)", filtered_total)
infoDict["Wind"] = info[0]  # still have to treat it a bit more

try: 
    info = re.findall(r"WindChill:(.+?)Visibility:", filtered_total)
    Stemp = info[0]  # Temp sensation before removing the Fahrenheit
    signfinder = re.findall("-", Stemp) 

    if len(signfinder) == 0:        # FIX IF NECESSARy/ INDEX MAY BE WRONG 
        if len(Stemp) == 4:
            Sensation = Stemp[:2]
        elif len(Stemp) == 3:
            Sensation = Stemp[1]
                
    else:
        if len(Stemp) == 5 or len(Stemp) == 6:
            Sensation = Stemp[:3]
        elif len(Stemp) == 4:
            Sensation = Stemp[:2]
        else:
            print("Problem 2")
    WindChill_Available = True

except IndexError:
    Sensation = "Not available"  # this is either due to an error or it's just not available cause it's not winter 
    WindChill_Available = False 
 

# All of this to separate the Celsius from Fahrenheit and store it in Sensation
infoDict["Sensation"] = Sensation

excel = openpyxl.load_workbook(filename="Weather_Tracker.xlsx")

page = excel.active

# Noting time of data taking
time = str(datetime.now())[:16]
count = str((page["Q1"].value)+1)

Tecell = 'A' + count
Ccell = 'C'+ count
Pcell = 'E' + count
Hcell = 'G'+ count
Wscell = 'I'+ count
Wccell = 'K'+ count
Tcell = 'M'+ count
Dcell = 'O' + count


page[Tecell] = float(infoDict['Temperature'])
page[Ccell] = infoDict['Condition']
page[Pcell] = infoDict['Pressure']
page[Hcell] = infoDict['Humidity']
page[Wscell] = infoDict['Wind']
if WindChill_Available: 
    page[Wccell] = int(infoDict['Sensation'])
else: 
    page[Wccell] = str(infoDict['Sensation'])
page[Tcell] = time
page[Dcell] = int(time[8:10])
page["Q1"] = int(count)


excel.save("Weather_Tracker.xlsx")
