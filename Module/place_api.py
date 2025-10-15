import json
import requests
import re
import Module.regex as regex

Teamplates_Dirname = "Teamplates"

def getLocationFromUserInput(address,APIkey):
    url01 ="https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key="+APIkey #把使用者輸入的地名轉成經緯度
    geo_response = requests.get(url01)
    geo_text = geo_response.text
    geo_json = json.loads(geo_text)

    lat = str(geo_json['results'][0]['geometry']['location']['lat'])
    long = str(geo_json['results'][0]['geometry']['location']['lng'])
    return lat,long

def runapi(nlat,elong,worknum):
    search_len = [1,5]

    head = {'accept': 'application/json'}
    url = "https://www.travel.taipei/open-api/zh-tw/Attractions/All?nlat="+nlat+"3&elong="+elong+"&page=1"
    response = requests.get(url,headers=head)
    r_t = response.text
    r_t = r_t.replace('&nbsp','')
    r_t = r_t.replace(r"\r\n" ,r"")
    j_data = json.loads(r_t)
    
    my_dict = {}
    limit = search_len[worknum]
    index = 0

    while index < limit :
        temp_dict = {}
        addr = j_data['data'][index]['address']
        name = j_data['data'][index]['name']
        cityId,categoryId = FindCategoryId(j_data['data'][index]['category'],addr,name)

        if categoryId != -1 :
            temp_dict['location'] = name
            temp_dict['id']= categoryId              
            temp_dict['lat'] = j_data['data'][index]['nlat']
            temp_dict['lon'] = j_data['data'][index]['elong']
            temp_dict['city_id'] = cityId
            temp_dict['intro'] = j_data['data'][index]['introduction']
            my_dict[str(index)] = temp_dict
            index = index + 1

    # way add others
    if (worknum==0 and index!=0):
        path = Teamplates_Dirname + "//" + "oneresult.json"

        with open(path,'w',encoding='utf8') as ff:
            json.dump(my_dict, ff, ensure_ascii=False)
    elif(worknum==1):
        path = Teamplates_Dirname + "//" + "fiveresult.json"

        with open(path,'w',encoding='utf8') as ff:
            json.dump(my_dict, ff, ensure_ascii=False)

#藝文場館 15  #老街 13  #商圈 24 #自然景區 16 #宗教場所 14 #夜市 23
NewTaipeiSceneId = {
                '館'   : 15,
                '老街' : 13,
                '碼頭' : 13,
                '商圈' : 24,
                '中心' : 24,
                '市場' : 24,
                '公園' : 16,
                '山'   : 16,
                '濕地' : 16,
                '步道' : 16,
                '宮'   : 14,
                '廟'   : 14,
                '寺'   : 14,
                '夜市' : 23
}

SceneNum = [13,14,15,16,23,24]

def FindCategoryId(Category,addr,name) :

    if regex.FindStrIn("臺北市",addr) :

       for i in range(len(Category)) :
            for j in range(6) :
                if(Category[i]["id"] == SceneNum[j]) :
                    return 0,SceneNum[j]
       return 0,-1

    elif regex.FindStrIn("新北市",addr) :
        for key in NewTaipeiSceneId.keys() :
            if regex.FindStrIn(key,name) :
               return 1,NewTaipeiSceneId[key]
        return 1,-2   # -2 others

        


    
