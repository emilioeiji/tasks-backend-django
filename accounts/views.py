from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def Accounts(request):
    return render(request, 'accounts/accounts.html')


@api_view(['POST'])
def criar_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if not username or not password or not email:
        return Response({'erro': 'Informe o nome de usuário, senha e email'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'erro': 'Nome de usuário já está em uso'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(
        username=username, password=password, email=email)
    return Response({'mensagem': 'Usuário criado com sucesso'}, status=status.HTTP_201_CREATED)
