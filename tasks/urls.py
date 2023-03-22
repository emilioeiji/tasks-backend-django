from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/get/', views.GetTasksView.as_view(), name='get_tasks'),
    path('tasks/create/', views.CreateTaskView.as_view(), name='create_tasks'),
    path('tasks/<int:task_id>/delete/',
         views.DeleteTaskView.as_view(), name='delete_task'),
]
