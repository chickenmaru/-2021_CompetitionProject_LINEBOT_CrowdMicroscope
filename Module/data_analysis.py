from math import cos
from math import sin
import math
import json
import random
import Module.doaction as doaction

Teamplates_Dirname = "Teamplates"

def Rad(d):
    return d * math.pi / 180.0

def GetDistance(lat1_txt, lng1_txt, lat2_txt, lng2_txt):
    lat1 = float(lat1_txt)
    lng1 = float(lng1_txt)
    lat2 = float(lat2_txt)
    lng2 = float(lng2_txt)
    EARTH_REDIUS = 6378.137
    radLat1 = Rad(lat1)
    radLat2 = Rad(lat2)
    a = radLat1 - radLat2
    b = Rad(lng1) - Rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(sin(a/2), 2) + cos(radLat1) * cos(radLat2) * math.pow(sin(b/2), 2)))
    s = s * EARTH_REDIUS
    return s

def Weather30Hr(citynum) :
    time = ['','','']
    rain_chance = ['','','']
    wx = ['','','']
    cci = ['','','']
    maxt = ['','','']
    mint = ['','','']

    data =  json.load(open('Cwb_Data//cwb_weather.json','r',encoding='utf-8'))

    location = data['cwbopendata']['dataset']['location'][citynum]['locationName']
    
    for j in range(3) :
        get = data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][0]['time'][j]['startTime'].split('T') 
        getdate = get[0]
        gethour = get[1].split('+') 
        time[j] = getdate + ' ' + gethour[0]
        rain_chance[j] = data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][4]['time'][j]['parameter']['parameterName']
        wx[j] =          data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][0]['time'][j]['parameter']['parameterName']
        cci[j] =          data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][3]['time'][j]['parameter']['parameterName']
        maxt[j] =        data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][1]['time'][j]['parameter']['parameterName']
        mint[j] =        data['cwbopendata']['dataset']['location'][citynum]['weatherElement'][2]['time'][j]['parameter']['parameterName']
        RenewWeatherTeamplate(location,time,rain_chance,wx,cci,maxt,mint)

def RenewWeatherTeamplate(location,time,rain_chance,wx,cci,maxt,mint):
    path = Teamplates_Dirname + "//" + "weather_teamplate.json"
    data =  json.load(open(path,'r'))
    
    for i in range(3) :
        data['contents'][i]['header']['contents'][0]['contents'][0]['text'] = location
        data['contents'][i]['header']['contents'][1]['text'] = time[i]
        data['contents'][i]['header']['contents'][2]['contents'][1]['text']  = rain_chance[i]+"%"
        a = rain_chance[i]
        if a == "0": 
            a = "0.01"
        data['contents'][i]['header']['contents'][3]['contents'][0]['width'] = a + "%"
        data['contents'][i]['body']['contents'][0]['contents'][0]['text']  = wx[i]
        data['contents'][i]['body']['contents'][1]['contents'][0]['text']  = cci[i]
        data['contents'][i]['body']['contents'][2]['contents'][1]['text'] = maxt[i]+"°C"
        data['contents'][i]['body']['contents'][3]['contents'][1]['text'] = mint[i]+"°C"

    f = open(path,'w')
    json.dump(data,f)
    f.close()

def RenewGPS(db,LineID,Lat,Lon) :
    data = db.GetOneData("Position","*","LineID",LineID)
    if data != None :
        db.ChangeData("Position","Lat,Lon,TimeStamp",f"{Lat},{Lon},'{doaction.GetTime()}'","LineID",LineID) 
    else :
        doaction.AddNewGPS(db,LineID,Lat,Lon)

def FindNextStep(db,LineID):
    data = db.GetOneData("Progress","*","LineID",LineID)
    if data != None :
       return data[2]
    else :
       doaction.AddNewWorknum(db,LineID)
       return -1

def RenewWorknum(db,LineID,worknum) :
    db.ChangeData("Progress","Worknum,TimeStamp",f"{worknum},'{doaction.GetTime()}'","LineID",LineID) 

def RenewNearStores(db,LineID,Lat,Lon) :
    data = db.GetOneData("NearStores","*","LineID",LineID)
    if data != None :
        db.ChangeData("NearStores","Lat,Lon,TimeStamp",f"{Lat},{Lon},'{doaction.GetTime()}'","LineID",LineID) 
    else :
        doaction.AddNewNearStores(db,LineID,Lat,Lon)

def RenewSiteTemplate2():
    path1 = Teamplates_Dirname + "//" + "oneresult.json"
    path2 = Teamplates_Dirname + "//" + "site_template2.json"

    apidata = json.load(open(path1,mode="r",encoding="utf-8"))
    data =  json.load(open(path2,mode="r",encoding="utf-8"))
    
    sitename = apidata['0']['location']
    sitestory = apidata['0']['intro']
    sitenlat = apidata['0']['lat'] 
    sitenlon = apidata['0']['lon'] 
    sitecategoryid = apidata['0']['id']
    cityID = apidata['0']['city_id']  

    populationPercentage = doaction.population(sitecategoryid)
    [humidity,rainProbability,apparrentemp] = doaction.WeatherElement(cityID,sitenlat,sitenlon) #新增回傳值 濕度
    recommendScore = doaction.GradingRecommendScore(apparrentemp,rainProbability,populationPercentage)
    
    data['body']['contents'][0]['text'] = sitename
    data['body']['contents'][1]['text'] = "降雨機率: " + str(rainProbability) + "%"      
    data['body']['contents'][2]['text'] = "體感溫度: " + str(round(apparrentemp,1)) + "°C"     
    data['body']['contents'][3]['text'] = "目前濕度: " + str(humidity) +"%"
    data['body']['contents'][4]['text'] = "目前人流: " + str(populationPercentage) + "%"      
    newstring=""

    """
    str_len = len(sitestory)

    if str_len < 300 :
       sitestory = sitestory[0:len(str_len)]
    else :
       str_len = regex.dsf()
       sitestory = sitestory[0:str_len] 
    """

    if(len(sitestory)>=300):
        for i in range(150,300):
            if(sitestory[i]=="。"):
                x=i
                break               
        for i in range(x):
            newstring += sitestory[i]
        newstring += "..."
        sitestory = newstring

    data['body']['contents'][6]['contents'][1]['width'] = str(recommendScore)+"%"
    data['body']['contents'][7]['contents'][0]['text'] = str(recommendScore)+"%" 
    data['body']['contents'][8]['contents'][0]['action']['text'] = sitestory   
    
    f = open(path2,'w')
    json.dump(data,f)
    f.close()

def RenewNearSiteTemplate2():
    path1 = Teamplates_Dirname + "//" + "fiveresult.json"
    path2 = Teamplates_Dirname + "//" + "site_near_template2.json"

    apidata = json.load(open(path1,mode="r",encoding="utf-8"))
    data =  json.load(open(path2,mode="r",encoding="utf-8"))

    sitename = ['','','','','']
    sitestory = ['','','','','']
    sitenlat = ['','','','',''] 
    sitenlon = ['','','','',''] 
    sitecategoryid = [0,0,0,0,0] 
    sitecityID = [0,0,0,0,0] 

    for i in range (5):
        x=str(i)
        sitename[i] = apidata[x]['location']
        sitestory[i] = apidata[x]['intro']
        sitenlat[i] = apidata[x]['lat']
        sitenlon[i] =  apidata[x]['lon'] 
        sitecategoryid[i] = apidata[x]['id']
        sitecityID[i] = apidata[x]['city_id']
    
    for i in range(5): 
        populationPercentage = doaction.population(sitecategoryid[i])
        [humidity,rainProbability,apparrentemp] = doaction.WeatherElement(sitecityID[i],sitenlat[i],sitenlon[i]) #新增回傳值 濕度
        recommendScore = doaction.GradingRecommendScore(apparrentemp,rainProbability,populationPercentage)
    
        data["contents"][i]['body']['contents'][0]['text'] = sitename[i]
        data["contents"][i]['body']['contents'][1]['text'] = "降雨機率: " + str(rainProbability) + "%"      
        data["contents"][i]['body']['contents'][2]['text'] = "體感溫度: " + str(round(apparrentemp,1)) + "°C" 
        data["contents"][i]['body']['contents'][3]['text'] = "目前濕度: " + str(humidity) +"%"         
        data["contents"][i]['body']['contents'][4]['text'] = "目前人流: " + str(populationPercentage) + "%"  
        
        if(len(sitestory[i])>=300):
            newstring=""
            for j in range(150,300):
                if(sitestory[i][j]=="。"):
                    x=j
                    break               
            for j in range(x):
                newstring += sitestory[i][j]
            newstring += "..."
            sitestory[i] = newstring


        data['contents'][i]['body']['contents'][6]['contents'][0]['width'] = str(recommendScore)+"%"
        data['contents'][i]['body']['contents'][7]['contents'][0]['text'] = str(recommendScore)+"%" 
        data['contents'][i]['body']['contents'][8]['contents'][1]['contents'][0]['action']['text'] = sitestory[i]
    
    f = open(path2,'w')
    json.dump(data,f)
    f.close()