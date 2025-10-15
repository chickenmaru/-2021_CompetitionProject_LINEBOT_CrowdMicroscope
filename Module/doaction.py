import os
import requests
import json
import time
import numpy as np

# 底線暫時不用理會
import Setting.parameter as parameter
import Module.postgresql as postgresql

Setting_Dir_Name = "Setting"
Teamplates_Dirname = "Teamplates"
Others_Dirname = "Others"

def WeatherDownload() :
    auth_key = parameter.cwb_auth_key
    Cwb_Dirname = "Cwb_Data"
    filepath = Cwb_Dirname + '//' + 'cwb_weather.json'

    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=" + auth_key + "&downloadType=WEB&format=JSON"
    response = requests.get(url)

    if os.path.isfile(filepath):
      print("檔案存在。")
    else:
      print("檔案不存在。")
      os.mkdir(Cwb_Dirname)

    with open(filepath,'wb') as f:
        f.write(response.content)

def FindFlexMsg(file_name) :
    FlexMessage = json.load(open(Teamplates_Dirname + "//" + file_name + ".json",'r',encoding='utf-8'))
    return FlexMessage

def FindRichMenusId(headers) :
    file_name = "richmenu"
    rich_menu_data = json.dumps(FindFlexMsg(file_name)).encode('utf-8')
    dictt = json.loads(requests.request('POST', 'https://api.line.me/v2/bot/richmenu',headers=headers,data=rich_menu_data).text)
    return dictt['richMenuId']

def EnableRichMenu(Id,headers) :
    req = requests.request('POST', "https://api.line.me/v2/bot/user/all/richmenu/" + Id,headers=headers)
    return req.text

def DBInI() :
    settings_path = Setting_Dir_Name + "//" + "settings.json"

    with open(settings_path,'r') as f:
        setting_dict =  json.load(f)

    PDB = postgresql.PostgresDB(
        setting_dict["DbName"],
        setting_dict["DbUser"],
        setting_dict["DbPassword"],
        setting_dict["DbHost"],
        setting_dict["DbPort"]
    )

    # 上線後不與資料庫斷線?
    PDB.ConnectToDB()

    return PDB

def GetTime() :
    t = time.localtime()
    return time.strftime("%Y/%m/%d,%H:%M:%S",t)

def AddNewGPS(db,LineID,Lat,Lon) :
    db.AddData("Position","LineID,Lat,Lon,TimeStamp",f"'{LineID}','{Lat}','{Lon}','{GetTime()}'")

def AddNewWorknum(db,LineID) :
    db.AddData("Progress","LineID,Worknum,TimeStamp",f"'{LineID}','{-1}','{GetTime()}'")

def AddNewNearStores(db,LineID,Lat,Lon):
    db.AddData("NearStores","LineID,Lat,Lon,TimeStamp",f"'{LineID}','{Lat}','{Lon}','{GetTime()}'")

def WeatherElement(city_ID,lat,lon): #城市ID 經度 緯度 
    lat = float(lat)
    lon = float(lon)
    cwb_auth_key = parameter.cwb_auth_key
    
    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=" + cwb_auth_key + "&downloadType=WEB&format=JSON"
    response = requests.get(url)
    weather = response.text
    w_json = json.loads(weather)
        
    prep_prob = float(w_json['cwbopendata']['dataset']['location'][city_ID]['weatherElement'][4]['time'][0]['parameter']['parameterName'])
        
    location_path = Others_Dirname + "//" + "location.json"

    with open(location_path,'r',encoding = 'utf8') as f:
        loc = json.load(f)
    
    dist = []
    for i in range(len(loc['Sheet1'])):
        dist.append(np.sqrt((float(loc['Sheet1'][i]['經度'])-lon)**2 + \
                            (float(loc['Sheet1'][i]['緯度'])-lat)**2))

    pos = min(dist)
    obs_name = loc['Sheet1'][dist.index(pos)]['站名']
    print(obs_name)

    url01= 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization='+cwb_auth_key+'&format=JSON'+'&locationName='+obs_name+'&elementName=WDSD,TEMP,HUMD'
    print(url01)
    
    response01 =requests.get(url01)
    obs = response01.text
    obs_json = json.loads(obs)

    Temp = float(obs_json['records']['location'][0]['weatherElement'][1]['elementValue']) #溫度
    RH = float(obs_json['records']['location'][0]['weatherElement'][2]['elementValue'])*100  #相對濕度
    WS = float(obs_json['records']['location'][0]['weatherElement'][0]['elementValue'])  #風速

    error_flag = False

    #回傳值判斷是否為異常值，若異常，轉為malfunctioned字串
    if prep_prob <= -1:
       prep_prob = 'malfunctioned'
       error_flag = True

    if Temp <= -99:
        Temp = 'malfunctioned'
        error_flag = True

    if RH <= -1:
        RH = 'malfunctioned'
        error_flag = True

    if WS <= -1:
        WS = 'malfunctioned'
        error_flag = True

    if not error_flag :
        e = RH/100*6.105*np.e**(17.27*Temp/(237.7+Temp))   #這兩行是新增的
        AT = 1.04*Temp +0.2*e-0.65*WS-2.7 
    else :
        AT = 'malfunctioned'

    return prep_prob,AT

def GradingRecommendScore(AT,prep,population): #溫度(Temp) 濕度(RH) 風速(WS) 降雨機率(prep_prob) 人流(y)   這個方程式在算推薦指數
        
    if AT >=20. and AT <24.:
        grading01 = 25
    elif AT >= 16. and AT <20.:
        grading01 = 50
    elif AT>=24. and AT < 28.:
        grading01 = 50
    elif AT >= 12. and AT< 16.:
        grading01 = 75
    elif AT >= 28. and AT <32.:
        grading01 = 75
    elif AT<12. or AT > 32.:
        grading01 = 100
        
    # 判斷降雨幾率是否異常，若否，正常運算
    if prep == 'malfunctioned':
        grading02 = 0
    else:
        grading02 = prep
    
    grading03 = population
    
    if AT == 'malfunctioned' or prep == 'malfunctioned':
        overall = 0
    else:
        overall = (grading01+grading02+grading03)/3

    return round(overall,1)

def population(ID): 
    t = time.localtime()
    getTime = time.strftime("%H:%M",t)
    XX = getTime.split(':')

    frac = int(XX[1])//15
    x = int(XX[0])*4+frac

    if ID == 15 :
        #Art & Edu 
        y = -9.046*(10**-9)*x**6+3.305*(10**-6)*x**5-0.0004307*x**4+ \
            0.02393*x**3 - 0.5221*x**2 + 3.844*x - 3.433
    elif ID == 23:
        #Night Market
        y = 1.374*(10**-8)*x**6 - 4.071*(10**-6)*x**5+0.0004389*x**4- \
            0.0214*x**3 + 0.4941*x**2 - 4.845*x + 16.45
    elif ID == 13:
        #Old Street
        y = -2.067*(10**-9)*x**6 + 1.388*(10**-6)*x**5-0.0002392*x**4+ \
            0.01564*x**3-0.3817*x**2+3.355*x-6.692
    elif ID == 14:
        #Religion
        y = -1.24*(10**-10)*x**6 + 3.386*(10**-7)*x**5 - 5.512*(10**-5)*x**4+\
            0.001511*x**3 + 0.1003*x**2 - 2.554*x + 11.28
    elif ID == 24:    
        #Shopping
        y = 1.023*(10**-8)*x**6 - 2.26*(10**-6)*x**5 + 0.0001547*x**4-\
            0.003245*x**3 + 0.01834*x**2 - 0.06132*x + 2.029
    elif ID == 16:
        #Recreation
        y = -5.502*(10**-9)*x**6 + 2.096*(10**-6)*x**5-0.0002725*x**4+ \
            0.01427*x**3 -0.2553*x**2 + 1.113*x+3.656
    else:
        # Others
        y = 1.755*10**-9*x**6 + 1.051*10**-8*x*5 - 6.184*10**-5*x**4 +\
            0.005375*x**3 - 0.1071*x**2 + 0.3196*x +3.891

    if y <=0:
       y=0
    return round(y,1)