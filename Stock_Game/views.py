from django.shortcuts import render

def index(request):
    return render(request, 'Stock_Game/main.html')
# Create your views here.
