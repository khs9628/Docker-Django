from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hi(request):
    return HttpResponse("Hello, world. Docker_land")

def home(reqeust):
    return HttpResponse('<html><body><h1>Hello World</h1></body></html>')
