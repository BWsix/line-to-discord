from .models import Group, Hook
from requests import post

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models.send_messages import TextSendMessage
from linebot.models.events import Event

import environ
env = environ.Env()
environ.Env.read_env()

line_bot_api = LineBotApi(env('channel_access_token'))
handler = WebhookHandler(env('channel_secret'))

from .scripts import scripts
scripts = scripts()


class Commands:
  
  def reply_line(self, event: Event, content: str) -> None:
    """Sends `content` to source line group."""
    return line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text=content))
  
  def get_group(self, event: Event) -> Group:
    """return `None` if Group not in database"""
    try:
      return Group.objects.get(id=event.source.group_id)
    except Group.DoesNotExist:
      return None

  def get_hooks(self, group: Group) -> list[Hook]:
    return Hook.objects.filter(owner=group)

  def admin_checker(self, event: Event) -> Group:
    """return `group` object if the event.source.user is an admin."""
    group = self.get_group(event)

    if group is None:
      return self.reply_line(event, f"這個群組尚未啟用discohook!\n{scripts.get_cmd('discohook')}")
    if event.source.user_id != group.manager:
      return self.reply_line(event, "只有管理員能夠使用指令!")
    
    return group


  def handle_create(self, event: Event) -> None:
    """add source group_id to database."""
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

    return self.reply_line(event, f"啟用成功\n{ scripts.get_cmd('discoquery') }")
  
  def handle_delete(self, event: Event) -> None:
    try:
      Group.objects.get(id=event.source.group_id).delete()
    except Group.DoesNotExist:
      pass

  def handle_link(self, event: Event) -> None:
    """add discord webhook sent by user to database."""
    group = self.admin_checker(event)
    texts = event.message.text.split('\n')
    
    if len(texts) != 3:
      return self.reply_line(event, scripts.err_format)
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
  
  def handle_unlink(self, event: Event) -> None:
    """delete discord webhook sent by user to database."""
    self.admin_checker(event)
    texts = event.message.text.split('\n')
    
    if len(texts) != 2:
      return self.reply_line(event, scripts.err_format)
    
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
      return self.reply_line(event, f"{name}不在已連結群組名單中\n{scripts.get_cmd('discoquery')}")
    

    return self.reply_line(event, f"成功解除連結\n將不會傳送訊至{name}")
    
  def handle_query(self, event: Event) -> None:
    """query all the groups in the database using group_id"""
    group = self.admin_checker(event)
    hooks = self.get_hooks(group)

    hook_list = "已連結的群組有 :\n" if hooks else "沒有已連結的群組"
    for item in hooks:
      hook_list += item.name + '\n'
    
    return self.reply_line(event, hook_list)

  def handle_help(self, event: Event) -> None:
    """send list of all commands to source line group"""
    content = scripts.get_help()

    return self.reply_line(event, content)


  def post(self, event: Event, **kwargs) -> None:
    """post `data` and `file`(optional) to discord group"""
    group = self.get_group(event)
    if group is None: return 
    
    hooks = self.get_hooks(group)
    if hooks is None: return
     
    for hook in hooks:
      try:
        post(hook.url, **kwargs)
      except Exception:
        pass
