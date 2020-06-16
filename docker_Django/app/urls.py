from django.urls import path, include
from . import views


urlpatterns = [
    path('hi/', views.hi, name='hi'),
    path('home/', views.home, name='home'),
]
