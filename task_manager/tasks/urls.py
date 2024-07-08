from django.urls import path

from . import views

urlpatterns = [
    path('task/create/', views.TaskAPICreate.as_view(), name='task_create'),
    path('task/list/', views.TaskAPIList.as_view(), name='task_list'),
    path('task/update/<int:pk>/', views.TaskAPIUpdate.as_view(), name='task_update'),
    path('task/detail/<int:pk>/', views.TaskAPIRetrieve.as_view(), name='task_detail'),
    path('task/assign/<int:pk>/', views.TaskAPIAssign.as_view(), name='task_assign'),
    path('task/complete/<int:pk>/', views.TaskAPIComplete.as_view(), name='task_complete'),
]
