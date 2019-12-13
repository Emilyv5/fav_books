from django.urls import path
from . import views
import book_app

urlpatterns = [
    path('', views.index),
    path('addition', views.addition),
    path('check', views.check),
]