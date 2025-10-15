import re

# 是說縣市天氣嗎
def Weather(txt) :
    regex = re.compile(r'(市天氣|縣天氣)')
    match = regex.search(txt)
    if match != None :
        return True
    else :
        return False

# 是說hello嗎
def Hello(txt) :
    regex = re.compile(r'(嗨)|(你好)|(您好)|(Hi)|(hi)|(Hello)|(hello)')
    match = regex.search(txt)
    if match != None :
        return True
    else :
        return False

def Start(txt) :
    regex = re.compile(r'(查詢)|(搜尋)')
    match = regex.search(txt)
    if match != None :
        return True
    else :
        return False

def NearSite(txt):
    regex = re.compile(r'(附近有什麼)') 
    match = regex.search(txt)
    if match != None :
        return True
    else :
        return False

def AskPlaceInfo(txt):
    regex = re.compile(r'(我有明確目的地)') 
    match = regex.search(txt)
    if match != None :
        return True
    else :
        return False

def AskDestnation(txt) :
    regex = re.compile(r'(有哪裡可以去)')
    match = regex.search(txt)
    if match != None :
        return True
    else :
        return False

def PlaceNearSite(txt):
    regex = re.compile(r'(景點附近有啥)')
    match = regex.search(txt)
    if match != None :
        return True
    else :
        return False

def FindStrIn(name,target):
    regex = re.compile(name)
    match = regex.search(target)
    if match != None :
        return True
    else :
        return False

fun_list = [
            Weather,
            Hello,
            Start,
            NearSite,
            AskPlaceInfo,
            AskDestnation,
            PlaceNearSite
           ]

def ExistOrNot(get_text):
    for i in range(len(fun_list)) :
        if fun_list[i](get_text) :
           return i
    return -1
