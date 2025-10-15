import Setting.parameter as parameter
import Module.regex as regex
import Module.line_tool as line_tool
import Module.data_analysis as data_analysis
# 底線暫時不用理會
import Module.doaction as doaction
import Module.scrapying as scrapying
import Module.place_api as place_api

from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
#...........................................................................................
App = Flask(__name__)
handler,line_bot_api = line_tool.LineBotSet()
DB = doaction.DBInI()
#...........................................................................................

@App.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    App.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def RegexResult(work_num,get_str,LineId) :
    if work_num == 0 :
        location = (get_str.split('天氣'))[0]
        if parameter.city.get(location,False) :
           citynum = int(parameter.city[location])
           doaction.WeatherDownload()
           data_analysis.Weather30Hr(citynum)
           return line_tool.FlexSendMessage('[天氣]',doaction.FindFlexMsg('weather_teamplate'))
        else :
           return line_tool.TextSendMessage("查無此縣市")
    elif work_num == 1 :   
        txt = "你好呀!"
        return line_tool.TextSendMessage(txt)
    elif work_num == 2 :   
        return line_tool.FlexSendMessage('[使用選擇]',doaction.FindFlexMsg('destination_choice_template'))
    elif work_num == 3 :
        data = DB.GetOneData("Position","*","LineID",LineId)
        if data == None :
           return line_tool.TextSendMessage("目前沒有記錄您的歷史資料唷")
        # lat : data[2] lon : data[3]
        place_api.runapi(data[2],data[3],1) 
        data_analysis.RenewNearSiteTemplate2()   
        return line_tool.FlexSendMessage('[附近景點資訊]',doaction.FindFlexMsg('site_near_template2'))
    elif work_num == 4 :   
        data_analysis.RenewWorknum(DB,LineId,0)
        return line_tool.TextSendMessage("請打入地點關鍵字吧~\n(如:信義威秀x；信義威秀影城○)")
    elif work_num == 5 : 
        return line_tool.TextSendMessage("我會根據您的最新定位位置推薦，請確認已更新定位資訊後，點選[附近有什麼]按鍵。\n定位啟用: (設定 > 隱私權 > 定位服務)")
    elif work_num == 6 : 
        data = DB.GetOneData("NearStores","*","LineID",LineId)
        if data == None :
           return line_tool.TextSendMessage("目前沒有記錄您的歷史資料唷")
        # lat : data[2] lon : data[3]
        #print(data[2],data[3])
        place_api.runapi(data[2],data[3],1) 
        data_analysis.RenewNearSiteTemplate2()   
        return line_tool.FlexSendMessage('[附近景點資訊]',doaction.FindFlexMsg('site_near_template2'))
    return None

def NextStep(worknum,get_str,LineId) :
    if worknum == 0 :
       data_analysis.RenewWorknum(DB,LineId,-1)
       lat,lon = place_api.getLocationFromUserInput(get_str,parameter.Google_api_key)
       data_analysis.RenewNearStores(DB,LineId,lat,lon)
       place_api.runapi(lat,lon,0)
       data_analysis.RenewSiteTemplate2()
       msg = []
       msg.append(line_tool.TextSendMessage("以下為 " + get_str + " 的資訊"))
       msg.append(line_tool.FlexSendMessage('[景點資訊]',doaction.FindFlexMsg('site_template2')))
       msg.append(line_tool.TextSendMessage("除了上述資訊外，我們還提供了與 " + get_str + " 相關的兩個小功能歐，一起來 try try看吧 ･◡･"))
       return msg
    elif worknum == 1:
       # here no work
       data_analysis.RenewWorknum(DB,LineId,-1)

       return line_tool.TextSendMessage("@@")

    return None
      
# 回應 TextMessage
@handler.add(line_tool.MessageEvent, message=line_tool.TextMessage)
def TextEcho(event):
    print(event.source.user_id)
    worknum = int(data_analysis.FindNextStep(DB,event.source.user_id))
    find = True

    if worknum != -1:
       reply_msg = NextStep(worknum,event.message.text,event.source.user_id)
    elif event.message.text == "說明":  
        reply_msg = line_tool.TextSendMessage("哈哈，暫時沒有說明。")
    elif event.message.text == "製作團隊" :
        reply_msg = line_tool.FlexSendMessage('[製作團隊]',doaction.FindFlexMsg('maker'))
    else :
        b = regex.ExistOrNot(event.message.text)
        if b != -1 :
           reply_msg = RegexResult(b,event.message.text,event.source.user_id)
        else :    
           find = False
    if find :
        line_bot_api.reply_message(event.reply_token,reply_msg)



# 回應 StickerMessage
@handler.add(line_tool.MessageEvent, message = line_tool.StickerMessage)
def StickerEcho(event):
    line_bot_api.reply_message(event.reply_token,line_tool.StickerSendMessage(package_id=1, sticker_id=2))

# 回應 LocationMessage
@handler.add(line_tool.MessageEvent, message = line_tool.LocationMessage)
def LocationEcho(event):
    address_txt = str(event.message.address)
    latitude_txt = str(event.message.latitude)
    longitude_txt = str(event.message.longitude)
    title_txt = str(event.message.title)
    msg = []
    txt = "了解! 我解讀您的位置在:\n" + address_txt + "\n" + latitude_txt + "\n"+ longitude_txt + "\n" + title_txt
    msg.append(line_tool.TextSendMessage(txt))
    txt = "若您需要查詢您所在地的附近景點，請點選[附近有什麼]按鍵。\n定位啟用: (設定 > 隱私權 > 定位服務)"
    msg.append(line_tool.TextSendMessage(txt))
    line_bot_api.reply_message(event.reply_token,msg)
    data_analysis.RenewGPS(DB,event.source.user_id,latitude_txt,longitude_txt)

# 回應 ImageMessage
@handler.add(line_tool.MessageEvent, message = line_tool.ImageMessage)
def ImageEcho(event):
    url_a = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/NCULogo.svg/1200px-NCULogo.svg.png'
    line_bot_api.reply_message(event.reply_token,line_tool.ImageSendMessage(original_content_url= url_a, preview_image_url= url_a))

if __name__ == "__main__":
    App.run()
