SITE = "https://github.com/BWsix/line-to-discord"

class scripts:
  cmd = {
    'discohook' : "啟用服務",
    'discolink' : "連結discord頻道",
    'discounlink' : "取消連結discord頻道",
    'discoquery' : "取得已連結的discord頻道列表",
    'discohelp' : "取得指令列表",
  }

  def get_help(self) -> str:
    """
    取得所有指令

    指令列表 : 
      指令 : 說明文字
    """

    content = "指令列表 :\n"
    for cmd, text in self.cmd.items():
      content += f"  {cmd} : {text}\n"
    return content

  def get_cmd(self, command) -> str:
    """
    取得單一指令搭配說明
    
    "輸入 {command} {說明文字}"
    """
    return f"輸入 '{command}' {self.cmd[command]}"

  def welcome(self):
    return """hi, I'm an epico messenger😎
    只需要在群做設定即可啟用本linebot
    啟用後會將此群組內的訊息轉發到discord群組裡
    支援單一群組對多個discord頻道
    可傳送包含圖片, 影片, 任何檔案, 加入/離開等訊息
    不過line貼圖無法在discord顯示，只好以"(sticker)"替代
    """ + f"""\n{self.get_cmd('discohook')}
    *輸入者將成為唯一的管理員*
    *只有管理員能夠使用指令*
    """ + f"""\n{self.get_cmd('discohelp')}
    可以在這裡查看詳細指令列表
    {SITE}
    """

  err_format = f"指令格式有誤，請到以下網址查看指令列表\n{SITE}"
