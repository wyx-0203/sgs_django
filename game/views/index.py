from django.shortcuts import render


def index(request):
    return render(request, 'multiends/index.html')

def acapp(request):
    return render(request, 'multiends/acapp.html')