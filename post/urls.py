from django.urls import path
from . import views

app_name = "post"
urlpatterns = [
    path('' , views.dashboard , name="dashboard"),
    path('post/index' , views.postIndex , name="index"),
    path('post/<int:post_id>/edit' , views.postEdit , name="edit"),
    path('post/<int:post_id>/update' , views.postUpdate , name="update"),
    path('post/create' , views.postCreate , name="create"),
    path('post/store' , views.postStore , name="store"),
    path('post/<int:post_id>/delete' , views.postDelete , name="delete"),
    path('post/<int:post_id>/gallery/<int:gallery_id>/delete' , views.deletePostGalleryImage , name="deletePostGalleryImage"),
    path('post/<int:post_id>/publish/<int:id>/' , views.publishPost , name="publishPost"),
    path('post/list/' , views.postList , name="postList"),
]

