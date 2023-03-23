from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('login/signin/', views.Signin.as_view(), name='signin'),
    path('login/test/', views.ProtectedView.as_view(), name='test'),
    path('logout/', views.LogoutView.as_view(), name='token_blacklist'),
]
