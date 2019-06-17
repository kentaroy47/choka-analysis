
# import stuff
from bs4 import BeautifulSoup
import requests
import codecs
import urllib
import lxml.html as lh
import pandas as pd
import datetime
import numpy as np
from scraper import fetch_choka_list

def get_person(datas):
    ans = []
    length = len(datas)
    for data in datas:
        data = str(data)
        for i, d in enumerate(data):
            if d=="者" and data[i+1]=="数" and data[i+2]==":":
                if data[i+3:i+6].isdigit():
                    ans.append(int(data[i+3:i+6]))
                elif data[i+3:i+5].isdigit():
                    ans.append(int(data[i+3:i+5]))
                else:
                    ans.append(int(data[i+3:i+4]))
    return ans

def get_temp(datas):
    ans = []
    length = len(datas)
    for data in datas:
        data = str(data)
        for i, d in enumerate(data):
            if d=="水" and data[i+1]=="温" and data[i+2]=="】":
                if data[i+3:i+7].isdigit():
                    ans.append(int(data[i+3:i+7]))
                elif data[i+3:i+6].isdigit():
                    ans.append(int(data[i+3:i+6]))
                elif data[i+3:i+5].isdigit():
                    ans.append(int(data[i+3:i+5]))
                else:
                    ans.append(int(data[i+3:i+4]))
    return ans          

def convert_to_datetime(time):
    year = time[0:4]
    
    if time[5:7].isdigit():
        month = time[5:7]
    else:
        month = time[5]
    if int(month) < 10:
        offset = 0
    else:
        offset = 1
    try:
        if time[7+offset:9+offset].isdigit():
            day = time[7+offset:9+offset]
        else:
            day = time[7+offset]
    except:
        day = time[7+offset]
    return year+"/"+month+"/"+day

df = pd.DataFrame(columns=["date", "people", "temp", "fishname", "fishnum", "fishsize", "days"])


url = "https://www.fishing-v.jp/choka/choka_detail.php"
facility_id = "11284"
max_page = 1

for page in range(100):
    soup = fetch_choka_list(url, facility_id, max_page=max_page, page_number=page)
    
    #fishdate = 30*month
    #month = "{:02d}".format(month)
    #year = str(year)
    
    choka = soup.find_all("tr")
    #print(choka)
    
    # get misc items
    tempdata = soup.find_all("span")
    temp = get_temp(tempdata)
    
    data = soup.find_all("div", class_="speech-bubble padding")
    people = get_person(data)
    
    datedata = soup.find_all("li", class_="chokaBoxDate padding")
    date = []
    for d in datedata:
        date.append(convert_to_datetime(d.string))
    
    # extract fish information
    count = -1
    fishname = []
    fishnum = []
    fishsize = []
    for chokadata in choka:
        if not "choka_index" in str(chokadata):
            fish = chokadata.find_all("td")
            
            fishname.append(str(fish[1].string))
            try:
                fishnum.append(int(str(fish[2].string).split()[1][:-1]))
            except:
                fishnum.append(0)
            fishsize.append(str(fish[3].string))
        else:
            count += 1
            if not count == 0:
                try:
                    df2 = pd.DataFrame({ 'date' : pd.Timestamp(date[count-1]), #
                            'people' : people[count-1],
                            'temp' : temp[count-1],
                            'fishname' : fishname,
                            'fishnum' : fishnum,
                            'fishnum-avg' : np.array(fishnum)/people[count-1],
                            'fishsize' : fishsize})
                    df = df.append(df2, ignore_index=True)
                    fishname = []
                    fishnum = []
                    fishsize = []
                except:
                    # in case temp is error
                    df2 = pd.DataFrame({ 'date' : pd.Timestamp(date[count-1]), #
                            'people' : people[count-1],
                            'temp' : temp[count-2],
                            'fishname' : fishname,
                            'fishnum' : fishnum,
                            'fishnum-avg' : np.array(fishnum)/people[count-1],
                            'fishsize' : fishsize})

# save data to file.

"""
data pattern is in pandas dataframe

header:
date, people, temp

body:
fishname, fishnum, fishsize
fishname, fishnum, fishsize
...
 
"""
# write out
df.to_csv("fish.csv")
