"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http.response import HttpResponse
from django.contrib import admin
from django.urls import path

from line_bot.webhook import webhook

urlpatterns = [
    path('webhook/', webhook),
    path('admin/', admin.site.urls),
]

def err404(request, exception):
  return HttpResponse('''
    <script>
      document.location.href = "https://github.com/BWsix/line-to-discord";
    </script>
  ''')

handler404 = err404
