from django.shortcuts import render


def front(request):
    context = {}
    return render(request, "index.html", context)
