from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    name = '尊敬的各位领导'
    return render(request, 'index.html', {'name':name})