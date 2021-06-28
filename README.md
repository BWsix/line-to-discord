# Line to Discord

暫時想不到名字的機器人  
會將line群組的訊息轉發到discord上


## **🧐 內容**

- [關於](#about)
- [指令列表](#commands)
- [使用教學](#getting_started)


## **👀 關於** <a name = "about"></a>

這個機器人會將他所在line群組內的訊息轉發到discord群組裡  
包含`圖片`, `影片`, `加入`, `離開`等訊息  
並支援**單一line群組對多個discord頻道**  

因為line的隱私政策  
未經官方認證的linebot帳號在尚未被用戶加入好友前  
無法透過userId取得任何使用者相關資料  
所以如果**想要傳送到discord內的訊息顯示"line用戶名稱"的話**  
需要**該line用戶有將本bot加入好友**

後端是用`django`寫的  
因為我自己架在`heroku`上所以也把`Procfile`等也許你用不到的檔案包進來了  

也許最近會更新...吧


## **📜 指令列表** <a name = "commands"></a>

- discohook : 啟用  
  輸入 `discohook` 者將成為唯一的管理員  
  ***只有管理員能夠使用指令***
  ```
  discohook
  ```

- discolink : 連結discord頻道  
  一個line群組可以連結多個discord頻道  
  ```
  discolink
  頻道名稱  (20字以內)
  Webhook網址
  ```

- discounlink : 取消連結discord頻道  
  ```
  discounlink
  頻道名稱
  ```

- discoquery : 取得已連結的discord頻道列表
  ```
  discoquery
  ```

- discohelp : 取得指令列表
  ```
  discohelp
  ```

## **👌 使用教學** <a name = "getting_started"></a>

### **啟用**

1. 將本linebot (@920xuqql) ([QRcode](https://qr-official.line.me/sid/L/920xuqql.png)) 加入你的line群組
1. 在聊天訊息輸入 `discohook` 便啟用完成

### **連結discord頻道**

1. 到要接收line訊息的**discord文字頻道** (你必須要有管理員身分)  
    到 *編輯頻道* -> *整合* -> *Webhook* -> *新Webhook*  
    設定完後按下 *複製Webhook網址*
1. 在line聊天室按照以下格式輸入設定(分三行)  
    
    ```
    discolink
    頻道名稱  (取消連結時用的，方便記憶即可)
    你剛剛複製的Webhook網址
    ```
    
    範例 :

    ```
    discolink
    班群
    https://discord.com/api/webhooks/00000/xxxxx
    ```

### **取消連結discord頻道**

在line聊天室按照以下格式輸入設定

```
discounlink
頻道名稱
```
    
範例 :

```
discounlink
班群
```
