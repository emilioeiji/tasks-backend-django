from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('login/token/', views.TokenSerializer.as_view(), name='auth_token'),
    path('login/api/', views.UserLoginView.as_view(), name='login_api'),
]
