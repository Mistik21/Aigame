from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Game, Task
from rest_framework import generics
from .serializers import GameSerializer, FullNameSerializer


class GameAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        model = Game(
            title=request.data["name"],
            class_user=request.data["class"],
            count_checkpoint=len(request.data["count-checkpoint"]),
            status=request.data["status"],
            img=request.data["background"],
            author=request.user,
        )
        try:
            model.save()
        except Exception:
            return Response({"status": "error"})
        count = 1
        for i in request.data["checkpoint"]:
            model_task = i[count]
            if model_task["link"] == "None":
                link = ""
            else:
                link = model_task["link"]
            tasks = Task(task_count=model_task["task-count"], topic=model_task["topic"], link=link)
            try:
                tasks.save()
            except Exception:
                return Response({"status": "error"})
            model.task.add(tasks)
            count += 1
        return Response({
            "status": "ok",
            "game-id": model.id,
        })


class GameListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameAPIObject(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class FullNameAPIAdd(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FullNameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok"
            })

        return Response({
            "status": "error"
        })
