from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Game, Task, FullName, Progress
from rest_framework import generics
from .serializers import GameSerializer
from . import Ai_create_game


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
            is_progress = Progress.objects.filter(game=game).get(user=request.user)
            list_progress = is_progress.progress_user.split(" ")
            try:
                list_progress[int(request.data["chckpint"]) - 1] = request.data["task"]
            except Exception:
                return Response({"status": "error"})
            is_progress.progress_user = " ".join(list_progress)
            try:
                is_progress.save()
                return Response({
                    "status": "ok"
                })
            except Exception:
                return Response({"status": "error"})
        task = Task.objects.get(pk=request.data["id_task"])
        progress_user = ["."] * int(task.task_count)
        try:
            progress_user[int(request.data["chckpint"]) - 1] = request.data["task"]
        except Exception:
            return Response({"status": "error"})
        model_progress = Progress(progress_user=" ".join(progress_user), game=game, user=request.user)
        try:
            model_progress.save()
        except Exception:
            return Response({"status": "error"})
        request.user.fullname.progress_game.add(model_progress)
        return Response({
            "status": "ok",
        })


class ProgressAPILis(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        game = Game.objects.get(pk=request.data["id_game"])
        is_progress = True
        try:
            is_progress = Progress.objects.filter(game=game).get(user=request.user)
        except Exception:
            is_progress = False
        if not is_progress:
            progress_user = ["."] * int(game.count_checkpoint)
            model_progress = Progress(progress_user=" ".join(progress_user), game=game, user=request.user)
            try:
                model_progress.save()
            except Exception:
                return Response({"status": "error"})
        is_progress = Progress.objects.filter(game=game).get(user=request.user)
        lisr_result = []
        count = 0
        for i in game.checkpoint.all():
            if is_progress.progress_user.split(" ")[count] != ".":
                lisr_result.append(int(i.task_count) - int(is_progress.progress_user.split(" ")[count]))
            else:
                lisr_result.append(int(i.task_count))
            count += 1
        return Response({
            "progress": lisr_result,
        })


class FullUserInfoAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        Fio_user = FullName.objects.get(user=request.user).FIO_user.split(" ")
        return Response({
            "name": Fio_user[1],
            "surname": Fio_user[0],
            "login": request.user.username,
            "email": request.user.email,
        }
        )


class CreateTopicAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            resp = Ai_create_game.creat_game(request.data["class_user"], request.data["topic"])
        except Exception:
            return Response({"status": "error"})
        return Response({
            "task": resp[0],
            "response_task": resp[1]
        })
