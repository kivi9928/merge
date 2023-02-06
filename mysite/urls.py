"""mysite URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from blog.api_url import api_view


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('userinfo', api_view.getData),
    path('', include('blog.urls')),
    path('blog/', include('blog.api_url')),
    # path('userinfo/',api_view.getData),
    # path('userinfo/<int:pk>/', api_view.getData),
    # path('postinfo/',api_view.postData),
    # path('categoryinfo/',api_view.categoryData),
    # path('categoryinfo/<int:pk>/',api_view.categoryData),
    path('polls/', include('polls.urls')),
   
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)


