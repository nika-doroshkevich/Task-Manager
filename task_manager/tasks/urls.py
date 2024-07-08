from django.urls import path

from . import views

urlpatterns = [
    path('task-create', views.CompanyAPICreate.as_view()),
    path('task-list', views.TaskList.as_view()),
    path('task/<int:pk>', views.TaskAPIRetrieveUpdate.as_view()),
    path('task-assign/<int:pk>', views.TaskAssignAPI.as_view(), name='task-assign'),
    path('task-complete/<int:pk>', views.TaskAPIRetrieveUpdate.as_view(), name='task-complete'),
]
