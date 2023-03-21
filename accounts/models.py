from django.contrib.auth.models import User
from django.db import models


class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.usuario.username
