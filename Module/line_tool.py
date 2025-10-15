from linebot.models import MessageEvent, TextMessage, TextSendMessage,StickerMessage,LocationMessage,StickerSendMessage,ImageMessage,ImageSendMessage,LocationSendMessage,ImagemapSendMessage,FlexSendMessage
from linebot import LineBotApi, WebhookHandler
import json
# 底線暫時不用理會
import Module.doaction as doaction

Photo_Dir_Name = "Photos"
Setting_Dir_Name = "Setting"

# LINE 聊天機器人的基本資料設置
def LineBotSet() :
    settings_path = Setting_Dir_Name + "//" + "settings.json"

    with open(settings_path,'r') as f:
        setting_dict =  json.load(f)

    # Set
    author_key = setting_dict["channel_access_token"]
    line_bot_api = LineBotApi(author_key)
    handler = WebhookHandler(setting_dict["channel_secret"])
    
    # RichMenu
    if setting_dict["RichMenuFlag"] == '0' :
        # Rich Menu
        headers = {"Authorization":"Bearer " + author_key,"Content-Type":"application/json"}

        Id = doaction.FindRichMenusId(headers)

        with open(Photo_Dir_Name + "//" + "Richmenu.png",'rb') as f:
            line_bot_api.set_rich_menu_image(Id, "image/png", f)

        print(doaction.EnableRichMenu(Id,headers))

        setting_dict["RichMenuFlag"] = "1"

        with open(settings_path,'w') as f:
            json.dump(setting_dict,f)
    
    return handler,line_bot_api
