from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer

import json

from . import functions as fn


@api_view(['GET'])
def get_version(request):
    return Response({
        "title": "Django API",
        "version": "0.0.1"
    })


@api_view(['GET'])
def get_users(request):

    if request.method == 'GET':
        # Get all objects in User's database (It returns a queryset)
        users = User.objects.all()

        # Serialize the object data into json (Has a 'many' parameter cause it's a queryset)
        serializer = UserSerializer(users, many=True)

        # Return the serialized data
        return Response(serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def get_by_nick(request, nick):
    try:
        user = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)

        print('Resultado Final ', fn.soma(4, 5))

        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# CRUD
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request):
    if request.method == 'GET':
        try:
            # Check if there is a get parameter called 'user' (/?user=xxxx&...)
            # if request.GET['user'] and request.GET['task_id]:
            if request.GET['user']:
                # Find get parameter
                user_nickname = request.GET['user']

                try:
                    # Get the object in database
                    user = User.objects.get(pk=user_nickname)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                # Serialize the object data into json
                serializer = UserSerializer(user)

                # Return the serialized data
                return Response(serializer.data)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # Criando Dados
    if request.method == 'POST':
        new_user = request.data

        serializer = UserSerializer(data=new_user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Editando Dados
    if request.method == 'PUT':
        nickname = request.data['user_nickname']

        try:
            updated_user = User.objects.get(pk=nickname)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        print(f'Data = {request.data}')

        serializer = UserSerializer(updated_user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Deletando Dados
    if request.method == 'DELETE':
        try:
            user_to_delete = User.objects.get(pk=request.data['user_nickname'])
            user_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# def databaseEmDjango():
# data = User.objects.get(pk='anderson')    -> Objeto
# data = User.objects.filter(user_age='32') -> QuerySet
# data = User.objects.exclude(user_age='25')  -> QuerySet
# data.save()
# data.delete()
