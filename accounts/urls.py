from django.urls import path

from . import views

urlpatterns = [
    path('accounts/', views.Accounts, name='accounts'),
    path('accounts/signup/', views.criar_usuario, name='signup')
]
