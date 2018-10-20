from django.http import JsonResponse
import json
from telegram import Update
from bot.config import BOT
from bot.config import DIS


def webhooks(request, bot_token):
    try:
        upd = Update.de_json(json.loads(request.body.decode("utf-8")), BOT)
    except Exception as e:
        return JsonResponse({})
    DIS.process_update(upd)
    return JsonResponse({}, status=200)
