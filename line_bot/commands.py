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


def reply_line(event, content):
  return line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=content)
)

class Commands:
  
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
      return reply_line(event, "這個群組尚未啟用discohook!\n使用指令 'discohook' 啟用")
    if event.source.user_id != group.manager:
      return reply_line(event, "只有管理員能夠使用指令!")
    
    return group


  def handle_create(self, event):
    try:
      Group.objects.get(id=event.source.group_id)
      return reply_line(event, "指令無效 : discohook已經啟用")
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

    return reply_line(event, "discohook啟用成功\n將我加入好友便能在discord顯示你的姓名")
  
  def handle_link(self, event):
    group = self.admin_checker(event)

    Hook.objects.create(
      owner=group,
      name=event.message.text.split('\n')[1],
      url=event.message.text.split('\n')[2],
    )

    return reply_line(event, "加入完成\n現在開始所有傳送至此群組的訊息將會藉由剛才提供的連結一併傳送至discord群組")
  
  def handle_unlink(self, event):
    group = self.admin_checker(event)
    name = event.message.text.split('\n')[1]
    
    try:
      object = Hook.objects.get(name=name)
      object.delete()
    except Group.DoesNotExist:
      return reply_line(event, f"{name}不在discohook名單中\n使用指令 'discoquery' 取得discohook名單")
    
    return reply_line(event, f"成功解除連結\n將不會傳送訊至{name}")
    
  def handle_query(self, event):
    group = self.admin_checker(event)
    hooks = self.get_hooks(group)

    hook_list = "已連結的群組有 :\n" if hooks else "沒有已連結的群組"
    for item in hooks:
      hook_list += item.name + '\n'
    
    return reply_line(event, hook_list)


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
