from django.shortcuts import render

from django.http import HttpRequest, HttpResponse


def front(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "index.html", context)
