from django.urls import path
from . import views

app_name = "post"
urlpatterns = [
    path('' , views.dashboard , name="dashboard"),
    path('post/index' , views.postIndex , name="index"),
]

