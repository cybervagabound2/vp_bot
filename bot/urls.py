from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('<bot_token>', csrf_exempt(views.webhooks), name='webhooks')
]