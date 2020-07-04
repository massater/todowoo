from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer
from todo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@csrf_exempt
def signup(request):
    if request.method == 'POST':

            try:
                data = JSONParser().parse(request)
                username = data['username']
                password = data['password']
                user = User.objects.create_user(username=username, password=password)
                user.save()
                token = Token.objects.create(user=user)
                return JsonResponse({'token': str(token)},  status=201)
            except IntegrityError:


                return JsonResponse({'error': 'That username is taken. Please choose another username'}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = user = authenticate(request, username=data['username'], password=data['password'])

        if user is None:
            return JsonResponse({'error': 'Unable to login. Please check username and password'}, status=400)
        try:
            token = Token.objects.get(user=user)
        except IntegrityError:
            token = Token.objects.create(user=user)
        return JsonResponse({'token': str(token)}, status=201)


class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print("User: ", user)
        return Todo.objects.filter(user=user, date_completed__isnull=False).order_by('-date_completed')


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print("User: ", user)
        return Todo.objects.filter(user=user)


class TodoComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print("User: ", user)
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.datacompleted = timezone.now()
        serializer.save()

class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print("User: ", user)
        return Todo.objects.filter(user=user, date_completed__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)