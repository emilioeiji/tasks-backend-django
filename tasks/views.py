from datetime import date

from django.shortcuts import render
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tasks


def home(request):
    return render(request, 'tasks/home.html')


class TasksView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # Verifica se a data foi passada na solicitação GET
        query_date_str = request.query_params.get('date')
        if query_date_str:
            query_date = date.fromisoformat(query_date_str)
        else:
            query_date = date.today()

        # Filtra as tarefas pelo id do usuário e a data estimada
        tasks = Tasks.objects.filter(
            userId=request.user, estimateAt__lte=query_date)

        # Ordena as tarefas pela data estimada
        tasks = tasks.order_by('estimateAt')

        # Cria uma lista de dicionários com os campos de cada tarefa
        tasks_list = []
        for task in tasks:
            task_dict = {
                'id': task.id,
                'desc': task.desc,
                'estimateAt': task.estimateAt.isoformat(),
                'doneAt': task.doneAt.isoformat() if task.doneAt else None,
                'userId': task.userId.id,
            }
            tasks_list.append(task_dict)

        # Retorna a lista de tarefas em formato JSON
        return Response(tasks_list)
