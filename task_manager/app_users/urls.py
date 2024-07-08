from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('user/create/', views.UserAPICreate.as_view(), name='user_create'),
    path('user/list/', views.UserList.as_view(), name='user_list'),
    path('user/', views.UserRetrieve.as_view(), name='user'),
]
