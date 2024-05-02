from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def chatbot(request):
    request.status
    return render(request, 'cardiobot.html')