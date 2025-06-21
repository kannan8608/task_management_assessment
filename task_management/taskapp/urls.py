from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/',OverallTasksAPi.as_view(),name='tasksapi'),
    path('tasks/<id>/',TasksAPi.as_view(),name='tasksapi'),
]