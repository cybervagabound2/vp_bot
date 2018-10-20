from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('vp_bot/', include('bot.urls')),
    path('admin/', admin.site.urls),
]
