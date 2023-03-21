from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('login/sigin/', views.Sigin.as_view(), name='sigin'),
    path('logout/', views.LogoutView.as_view(), name='token_blacklist'),
]
