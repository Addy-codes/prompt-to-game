from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from .models import *
import json
from game.creator import *
from .serializers import *
import firebase

firebaseConfig = settings.FIREBASE_CONFIG
app = firebase.initialize_app(firebaseConfig)
auth = app.auth("./keys/client_secret.json")


class MyGames(APIView):
    def get(self, request, format=None):
        try:
            token = request.headers.get('Authorization')
            user = auth.verify_id_token(token)
        except Exception as e:
            return Response({'error': f"Sign in again. Token {str(e)}"}, status=403)
        print(user)
        user_id = user['user_id']
        # print(request.user)
        print("user_id: ", user_id)
        games = UGGame.objects.filter(creatorid=user_id)
        if len(games) < 1:
            return Response({"No games available"}, status=404)
        serializer = UGGameSerializer(games, many=True)
        return Response(serializer.data)


class UGGameListView(APIView):
    def get(self, request, format=None):
        games = UGGame.objects.all()
        serializer = UGGameSerializer(games, many=True)
        return Response(serializer.data)


# class GameList(generics.ListAPIView):
#     queryset = Game.objects.all()
#     serializer_class = RimoraiSerializer


# class GameRetrieve(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Game.objects.all()
#     serializer_class = RimoraiSerializer

class GameList(APIView):
    def get(self, request):
        movies = Game.objects.all()
        serializer = RimoraiSerializer(movies, many=True)
        print(serializer.data)
        if (len(serializer.data) <= 0):
            return Response({'error': 'List is Empty'})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RimoraiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CreateDirectGame(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Frontend: 
            data = request.data
            prompt = data.get('prompt')
            token = request.headers.get('Authorization')
            print(token)
            # API
            # data = json.loads(request.body)
            # prompt = data.get('prompt')

            # JWT provided by firebase
            # token = request.session.get('idToken')

            user = auth.verify_id_token(token)
            print(user)
            user_id = user['user_id']
            # print(request.user)
            print("user_id: ", user_id)

            title, description, thumbnail, url = createGame(prompt, user_id)

            return Response({
                'message': 'Game created successfully',
                'title': title,
                'description': description,
                'thumbnail': thumbnail,
                'url': url,
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)
