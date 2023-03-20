from django.urls import path

from . import views

urlpatterns = [
    path('accounts/', views.Accounts, name='accounts'),
    path('accounts/create/', views.CreateUserView.as_view(),
         name='create_user'),
]
