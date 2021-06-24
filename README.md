# Line to Discord
暫時想不到名字的機器人  
會將line群組的訊息轉發到discord上

## 內容

- [關於](#about)
- [如何安裝](#getting_started)

## 關於 <a name = "about"></a>

這個機器人會將他所在line群組內的訊息轉發到discord群組裡  
包含`圖片`, `影片`, `加入`, `離開`等訊息  

後端是用`django`寫的  
因為我自己架在`heroku`上所以也把`Procfile`等也許你用不到的檔案包進來了  

也許最近會更新...吧🤔

## 如何安裝 <a name = "getting_started"></a>

### 你將會需要

- heroku帳號
- 一個linebot
- github帳號


### **申請Heroku帳號**

Heroku是一個可以免費使用的雲端伺服器，Linebot的終端(?)等等會部署在上面

1. 先到 [**這裡**](https://signup.heroku.com/) 申請Heroku帳號

1. 申請完後到 [**這個頁面**](https://dashboard.heroku.com/apps) ，左上角依序點 **New** -> **Create new app**  
  並填寫你的 **app-name**(因為app-name不能重複註冊，可能要多試幾個才找到可用的)

1. 從上面那排小字找到 **settings**  
  點擊位於第二區塊 **Config Vars** 旁的 **Reveal Config Vars** 按鈕

1. 先停在這個頁面並往下，等等一起設定

### **申請Linebot**

Linebot作為機器人將會進到你的群組聊天室內讀取訊息  
跟著以下步驟申請並調整一些設定

1. 先到 [**Line developers**](https://developers.line.biz/) 登入你的line帳號  
  登入完後點選畫面中間的 **Console按鈕** [**或是這個連結**](https://developers.line.biz/console/) 進入控制台頁面

1. 找到位於畫面中下方 **Providers** 右邊的 **Create** 綠色按鈕並建立provider  
  並在下方欄位點選你剛剛建立的帳號

1. 在新分頁點選 **Create a new channel**  
  並選擇左邊數來第二個的 **Messaging API**

1. 欄位填一填，合約勾一勾後按 **Create** 建立就完成了  
  (名字或頭貼之後都可以改)

1. 接下來要在這個頁面複製兩串字，並貼到剛才 **Heroku** 的 Config Vars
    1. 在 **Basic settings** 滑到最底，將會看到 **Channel secret**  
    完整複製那一串亂碼，並回到 Heroku config vars 的分頁  
    在右側的 **VALUE** 欄位貼上後亂碼後  
    在左側的 **KEY** 欄位貼上 `channel_secret` 並按 **Add**
    
    1. 在 **Messaging API** 滑到最底，將會看到 **Channel access token (long-lived)**  
    按下最右方的黑色 **Issue** 按鈕，並複製亂碼  
    完整複製那一串亂碼，並回到 Heroku config vars 的分頁  
    在右側的 **VALUE** 欄位貼上後亂碼後  
    在左側的 **KEY** 欄位貼上 `channel_access_token` 並按 **Add**
    (先不要關頁面，等等需要用到)

1. 接下來到 [這個網站](https://django-secret-key-generator.netlify.app/) 按 **Copy to clipboard** 複製那串亂碼  
  回到 Heroku config vars 的分頁  
  在右側的 **VALUE** 欄位貼上後亂碼後  
  在左側的 **KEY** 欄位貼上 `SECRET_KEY` 並按 **Add**

1. 接下來到你要傳送line訊息的discord伺服器(你必須要有管理員身分)  
  到 **伺服器設定** -> **整合** -> **Webhook** -> **新Webhook**
  頻道設定為你要傳送訊息的的頻道後  
  按下 **複製Webhook網址** 並回到 Heroku config vars 的分頁
  在右側的 VALUE 欄位貼上後網址後
  在左側的 KEY 欄位貼上 `discohook` 並按 Add

1. 切換 Heroku config vars 的分頁到 Deploy  
  按下正中間的 **Github** 按鈕後停在這個頁面並往下

### **申請Github帳號**

1. 到 [**github**](https://github.com/) 註冊帳號

1. 回到 [這個頁面](https://github.com/BWsix/line-to-discord) 並按下最右上角的 **Fork**

1. 到 [Heroku](https://dashboard.heroku.com/account/applications) 並授權你的github帳號(Third-party Services)

1. 回到剛才的 Deploy 頁面，`F5` 重整後在下方選擇你的帳號後  
  **repo-name** 打上 `line-to-discord`  
  並按下下方 **connect** 按鈕

1. 滑到頁面最下方的 **Manual deploy** 區塊  
  按下 **Deploy Branch** 黑色按鈕  
  (這可能要等一段時間)

1. 當顯示 **Your app was successfully deployed.** 後  
  按下頁面右上方的 **Open app** 並複製 URL
  (Not Found 是正常的)
 
1. 回到 Line Developers 的 **Messaging API**  
  往上找到 **Webhook URL**  
  將剛剛複製的網址貼上後 **後方再加上 `/webhook/`**  
  (也就是說長這樣 : `https://app-name.herokuapp.com/webhook/`)
  並將下方 **Use webhook** 打開

1. 點選 **Allow bot to join group chats**  
  在新頁面 **功能切換** -> **加入群組或多人聊天室** 勾選下面的 **接受**

1. **最~後~**
  複製 **帳號資訊** -> **基本ID** 旁邊的 @xxxxxxx 並加到你的群組就完成了!!
  沒有意外的話啦 **(´。＿。｀)**
