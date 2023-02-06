from django.urls import path
from . import api_view
# from .api_view import  SignupApiView


urlpatterns = [
    
    path('user_api/', api_view.UserDetail.as_view(), name='user_api'),
    path('post_api/',api_view.PostList.as_view(),name='post_api' ),
    path('post_api/<int:pk>/',api_view.PostDetail.as_view(),name='post_api' ),
    path('category_api/',api_view.CategoryListDetail.as_view()),
    path('category_api/<int:pk>/',api_view.CategoryDetail.as_view()),
    path('tag_api/',api_view.TagDetail.as_view()),
    path('signup_api/', api_view.SignupApiView.as_view(), name='signup-api'),
    path('login_api/', api_view.LoginApiView.as_view(), name='login-api'),
    path('comment_api/',api_view.CommentDetail.as_view()),
]