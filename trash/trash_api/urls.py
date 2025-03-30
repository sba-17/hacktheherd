from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_api,name="index_api")
]