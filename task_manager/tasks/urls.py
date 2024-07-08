from django.urls import path

from . import views

urlpatterns = [
    path('task-create', views.TaskAPICreate.as_view()),
    path('task-list', views.TaskAPIList.as_view()),
    path('task-update/<int:pk>', views.TaskAPIUpdate.as_view()),
    path('task/<int:pk>', views.TaskAPIRetrieve.as_view()),
    path('task-assign/<int:pk>', views.TaskAPIAssign.as_view(), name='task-assign'),
    path('task-complete/<int:pk>', views.TaskAPIUpdate.as_view(), name='task-complete'),
]
