from datetime import date

from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.exceptions import (NotFound, PermissionDenied,
                                       ValidationError)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tasks


def home(request):
    return render(request, 'tasks/home.html')


class GetTasksView(APIView):
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


class CreateTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Obtenha o usuário autenticado a partir do token
        user = request.user

        # Verifique se o campo 'desc' está presente nos dados da solicitação POST
        if 'desc' not in request.data:
            return Response({'error': 'Field "desc" is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Crie a nova tarefa
        task = Tasks(desc=request.data['desc'], estimateAt=request.data.get(
            'estimateAt'), userId=user)
        task.save()

        # Crie um dicionário com os campos da nova tarefa
        task_dict = {
            'id': task.id,
            'desc': task.desc,
            'estimateAt': task.estimateAt,
            'doneAt': task.doneAt,
            'userId': task.userId.id,
        }

        # Retorne a resposta com o status 201 (Created) e o dicionário da nova tarefa
        return Response(task_dict, status=status.HTTP_201_CREATED)


class DeleteTaskView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            # Obter a task com o ID passado via parâmetro na URL
            return Tasks.objects.get(id=self.kwargs['task_id'])
        except Tasks.DoesNotExist:
            raise NotFound

    def delete(self, request, *args, **kwargs):
        # Obter a task a ser deletada
        task = self.get_object()

        # Verificar se o usuário que está autenticado é o dono da task
        if task.userId != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Deletar a task
        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleTaskView(generics.UpdateAPIView):
    queryset = Tasks.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            # Obter a task com o ID passado via parâmetro na URL
            return self.queryset.get(id=self.kwargs['task_id'])
        except Tasks.DoesNotExist:
            raise NotFound

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Verificar se o usuário que está autenticado é o dono da task
        if instance.userId != self.request.user:
            raise PermissionDenied

        # Verificar se o campo doneAt já foi preenchido
        if instance.doneAt is None:
            instance.doneAt = date.today()
            instance.save()
            return Response({'success': 'Task concluida.'},
                            status=status.HTTP_200_OK)

        else:
            instance.doneAt = None
            instance.save()
            return Response({'success': 'Task não concluida.'},
                            status=status.HTTP_200_OK)

        return self.partial_update(request, *args, **kwargs)
