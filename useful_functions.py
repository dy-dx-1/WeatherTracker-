import re
import tkinter as tk

def clean_tags(data_list):
    for n in range(len(data_list)):             # for every box in the data
        data = str(data_list[n].get_text)       # get the text and convert from method to string 
        tags = re.findall('<.*?>', data)             # find all the tags 
        for tag in tags:                                 # take every tag from the regex findall and replace it in the unfiltered text with emptyness 
            data = data.replace(tag, '')
        if n == 0:   # if first turn 
            tempdata = data  # put what will become old data on second turn in var tempdata 
        else: 
            tempdata = tempdata + data  # else, add to temp data the old data 
    return tempdata    
        
def whitespace_destroyer(string): 
    string = string.replace(' ', '')
    string = string.replace('\n', '')
    string = string.replace('\r', '') # windows line jump thing    
    return string




