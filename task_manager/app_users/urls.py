from django.urls import path

from . import views

urlpatterns = [
    path('login', views.UserLogin.as_view()),
    path('user-create', views.UserAPICreate.as_view()),
    path('user-list', views.UserList.as_view()),
    path('user', views.UserRetrieve.as_view()),
]
