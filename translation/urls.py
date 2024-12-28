from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='hello'),   # Default "Hello" endpoint
    path('translate/', views.translate, name='translate'),  # Translation endpoint
]
