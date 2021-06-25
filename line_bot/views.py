from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from linebot.models.events import FollowEvent, UnfollowEvent
from linebot.models.messages import AudioMessage, FileMessage, ImageMessage, StickerMessage, VideoMessage

from requests import post
import environ

env = environ.Env()
environ.Env.read_env()

line_bot_api = LineBotApi(env('channel_access_token'))
handler = WebhookHandler(env('channel_secret'))
discohook = env('discohook')

@csrf_exempt
@require_POST
def webhook(request: HttpRequest):
  signature = request.headers["X-Line-Signature"]
  body = request.body.decode()

  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    messages = ("Invalid signature.")
    return HttpResponseBadRequest(messages)
  return HttpResponse("OK")
  

def get_profile(event, content=None):
  profile = line_bot_api.get_profile(event.source.user_id)
  
  return {
    'content' : content,
    'username' : profile.display_name,
    'avatar_url' : profile.picture_url,
  }


def get_binary(event):
  content = line_bot_api.get_message_content(event.message.id)

  file = b""
  for chunk in content.iter_content():
    file += chunk

  return file


def tmp_blocker(event, data, files=None, url=discohook):
  try:
    id = event.source.group_id
  except Exception:
    return

  post(discohook, data=data, files=files)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  profile = get_profile(event, event.message.text)

  return tmp_blocker(event, profile)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
  profile = get_profile(event)
  file = get_binary(event)
  
  return tmp_blocker(event, profile, files={'media.jpg':file})


@handler.add(MessageEvent, message=VideoMessage)
def handle_video(event):
  profile = get_profile(event)
  file = get_binary(event)

  return tmp_blocker(event, profile, files={'media.mp4':file})


@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
  profile = get_profile(event)
  file = get_binary(event)

  return tmp_blocker(event, profile, files={'media.mp3':file})


@handler.add(MessageEvent, message=FileMessage)
def hendle_file(event):
  profile = get_profile(event)
  file = get_binary(event)

  return tmp_blocker(event, profile, files={event.message.file_name:file})


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
  profile = get_profile(event, "**(sticker)**")

  return tmp_blocker(event, profile)


@handler.add(FollowEvent)
def handle_follow(event):
  profile = get_profile(event, "**(joined the group)**")
  
  return tmp_blocker(event, profile)


@handler.add(UnfollowEvent)
def handle_unfollow(event):
  profile = get_profile(event, "**(left the group)**")

  return tmp_blocker(event, profile)
