from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest

from .commands import Commands, line_bot_api, handler

from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

cmd = Commands()

@csrf_exempt
@require_POST
def callback(request: HttpRequest):
  signature = request.headers["X-Line-Signature"]
  body = request.body.decode()

  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    messages = ("Invalid signature.")
    return HttpResponseBadRequest(messages)
  return HttpResponse("OK")
  

def reply_line(event, content):
  return line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=content)
  )

def create_request_data(event, content=None) -> dict:
  try:
    request_data = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
    username = request_data.display_name
  except LineBotApiError:
    username = "unknown"

  try:
    summary = line_bot_api.get_group_summary(event.source.group_id)
    avatar_url = summary.picture_url
    username += f" from {summary.group_name}"
  except LineBotApiError:
    avatar_url = None
    username += f" (group_name not found)"


  return {
    'content' : content,
    'username' : username,
    'avatar_url' : avatar_url,
  }

def get_binary(event):
  content = line_bot_api.get_message_content(event.message.id)

  file = b""
  for chunk in content.iter_content():
    file += chunk

  return file


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  if event.source.type == 'user':
    return reply_line(event, "hi, I'm an epico messenger😎")

  if event.message.text == 'discohook':
    return cmd.handle_create(event)
  if event.message.text.split('\n')[0] == 'discolink':
    return cmd.handle_link(event)
  if event.message.text.split('\n')[0] == 'discounlink':
    return cmd.handle_unlink(event)
  if event.message.text == 'discoquery':
    return cmd.handle_query(event)
  if event.message.text == 'discohelp':
    return cmd.handle_help(event)
  

  request_data = create_request_data(event, event.message.text)
  
  cmd.post(event, data=request_data)


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
  request_data = create_request_data(event, "**(sticker)**")

  cmd.post(event, data=request_data)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
  request_data = create_request_data(event)
  file = get_binary(event)
  
  cmd.post(event, data=request_data, files={'media.jpg':file})

@handler.add(MessageEvent, message=VideoMessage)
def handle_video(event):
  request_data = create_request_data(event)
  file = get_binary(event)

  cmd.post(event, data=request_data, files={'media.mp4':file})

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
  request_data = create_request_data(event)
  file = get_binary(event)

  cmd.post(event, data=request_data, files={'media.mp3':file})

@handler.add(MessageEvent, message=FileMessage)
def hendle_file(event):
  request_data = create_request_data(event)
  file = get_binary(event)

  cmd.post(event, data=request_data, files={event.message.file_name:file})

@handler.add(FollowEvent)
def handle_follow(event):
  request_data = create_request_data(event, "**(joined the group)**")
  
  cmd.post(event, data=request_data)

@handler.add(UnfollowEvent)
def handle_unfollow(event):
  request_data = create_request_data(event, "**(left the group)**")

  cmd.post(event, data=request_data)
