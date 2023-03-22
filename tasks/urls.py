from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/get/', views.TasksView.as_view(), name='get_tasks'),
]
