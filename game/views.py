from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Game, Task, FullName, Progress
from rest_framework import generics
from .serializers import GameSerializer


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
        model = FullName(FIO_user=request.data["FIO_user"], user=request.user)
        try:
            model.save()
            return Response({
                "status": "ok",
            })
        except Exception:
            return Response({"status": "error"})


class ProgressAPIAdd(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        game = Game.objects.get(pk=request.data["id_game"])
        is_progress = Progress.objects.filter(user=request.user).exists()
        if is_progress:
            is_progress = Progress.objects.get(user=request.user)
            return Response({
                "checkpoint": is_progress.checkpoint,
                "task": is_progress.task,
            })
        model_progress = Progress(game=game, user=request.user, checkpoint=request.data["checkpoint"],
                                  task=request.data["task"])
        try:
            model_progress.save()
        except Exception:
            return Response({"status": "error"})
        request.user.fullname.progress_game.add(model_progress)
        return Response({
            "status": "ok",
        })
