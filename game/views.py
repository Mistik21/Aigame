from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Game, Task


class GameAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        model = Game(
            title=request.data["name"],
            class_user=request.data["class"],
            count_checkpoint=request.data["count-checkpoint"],
            status=request.data["status"],
            img=request.data["background"],
            author=request.user,
        )
        try:
            model.save()
        except Exception:
            return Response({"status": "error"})
        for i in request.data["checkpoint"]:
            model = request.data["checkpoint"]
            if model[i]["link"] == "None":
                link = ""
            else:
                link = model[i]["link"]
            tasks = Task(task_count=model[i]["task-count"], topic=model[i]["topic"], link=link)
            try:
                tasks.save()
            except Exception:
                return Response({"status": "error"})
            model.task.add(tasks)
        return Response({
            "status": "ok",
            "game-id": model.id,
        })
