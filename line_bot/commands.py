from .models import Group, Hook
from requests import post

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models.send_messages import TextSendMessage

import environ
env = environ.Env()
environ.Env.read_env()

line_bot_api = LineBotApi(env('channel_access_token'))
handler = WebhookHandler(env('channel_secret'))


SITE = "https://github.com/BWsix/line-to-discord"


class Commands:
  
  def reply_line(self, event, content):
    return line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text=content))
  
  def get_group(self, event) -> Group:
    try:
      return Group.objects.get(id=event.source.group_id)
    except Group.DoesNotExist:
      return None

  def get_hooks(self, group) -> list:
    return Hook.objects.filter(owner=group)

  def admin_checker(self, event) -> Group:
    group = self.get_group(event)

    if group is None:
      return self.reply_line(event, "這個群組尚未啟用discohook!\n使用指令 'discohook' 啟用")
    if event.source.user_id != group.manager:
      return self.reply_line(event, "只有管理員能夠使用指令!")
    
    return group


  def handle_create(self, event):
    try:
      Group.objects.get(id=event.source.group_id)
      return self.reply_line(event, "指令無效 : discohook已經啟用")
    except Group.DoesNotExist:
      pass

    try:
      summary = line_bot_api.get_group_summary(event.source.group_id)
      name = summary.group_name
    except LineBotApiError:
      name = "(group name not found)"

    Group.objects.create(
      id=event.source.group_id,
      name=name,
      manager=event.source.user_id,
    )

    return self.reply_line(event, f"啟用成功\n將本bot加入好友便能在discord顯示你的姓名\n請到以下網址查看指令列表\n{SITE}")
  
  def handle_link(self, event):
    group = self.admin_checker(event)
    texts = event.message.text.split('\n')
    
    if len(texts) != 3:
      return self.reply_line(event, f"指令格式有誤，請到以下網址查看指令列表\n{SITE}")
    if len(texts[1]) > 20:
      return self.reply_line(event, f"名稱太長\n必須小於20字")
    
    try:
      hook = Hook.objects.get(name=texts[1])
      return self.reply_line(event, f"這個名稱已被註冊")
    except Hook.DoesNotExist:
      pass

    try:
      hook = Hook.objects.get(url=texts[2])
      return self.reply_line(event, f"這個頻道已被{hook.name}註冊")
    except Hook.DoesNotExist:
      pass

    Hook.objects.create(
      owner=group,
      name=texts[1],
      url=texts[2],
    )

    try:
      summary = line_bot_api.get_group_summary(event.source.group_id)
      group_name = summary.group_name
    except LineBotApiError:
      group_name = "unknown"
    post(texts[2], data={'content':f"(**{group_name}已建立連結**)"})
    
    return self.reply_line(event, "加入完成\n現在開始所有傳送至此群組的訊息將會藉由剛才提供的連結一併傳送至discord群組")
  
  def handle_unlink(self, event):
    self.admin_checker(event)
    texts = event.message.text.split('\n')
    
    if len(texts) != 2:
      return self.reply_line(event, f"指令格式有誤，請到以下網址查看指令列表\n{SITE}")
    
    name = texts[1]
    
    try:
      object = Hook.objects.get(name=name)

      try:
        summary = line_bot_api.get_group_summary(event.source.group_id)
        group_name = summary.group_name
      except LineBotApiError:
        group_name = "unknown"
      
      post(object.url, data={'content':f"(**{group_name}已解除連結**)"})
      object.delete()
    except Hook.DoesNotExist:
      return self.reply_line(event, f"{name}不在已連結群組名單中\n使用指令 'discoquery' 取得已連結群組名單")
    

    return self.reply_line(event, f"成功解除連結\n將不會傳送訊至{name}")
    
  def handle_query(self, event):
    group = self.admin_checker(event)
    hooks = self.get_hooks(group)

    hook_list = "已連結的群組有 :\n" if hooks else "沒有已連結的群組"
    for item in hooks:
      hook_list += item.name + '\n'
    
    return self.reply_line(event, hook_list)

  def handle_help(self, event):
    content = """指令列表 :
    discohook : 啟用服務
    discolink : 連結discord頻道
    discounlink : 取消連結discord頻道
    discoquery : 取得已連結的discord頻道列表
    discohelp : 取得指令列表
    """
    content += f"\n請到以下網址查看詳細指令列表\n{SITE}"

    return self.reply_line(event, content)


  def post(self, event, **kwargs):
    group = self.get_group(event)
    if group is None:
      return 
    
    hooks = self.get_hooks(group)
    if hooks is None:
      return
     
    for hook in hooks:
      try:
        post(hook.url, **kwargs)
      except Exception:
        pass
