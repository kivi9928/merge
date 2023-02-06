from django.urls import path
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<str:slug>/detail/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path('signup/', views.signup, name='signup'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile_edit/<str:username>/', views.profile_edit, name='profile_edit'),
    path('category/<str:slug>/', views.category, name='category'),
    path('tag/<str:slug>/', views.tag, name='tag'),
    
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    