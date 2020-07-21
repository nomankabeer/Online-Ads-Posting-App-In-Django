from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from .models import Posts , Gallery as post_gallery
from django.shortcuts import redirect
from django.utils import timezone
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage
import uuid
import os
from .forms import PostFormEditValidation , PostFormValidation
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login , logout as django_logout

@login_required(redirect_field_name='next', login_url='/login')
def dashboard(request):
    return  render(request , 'dashboard.html')


@login_required(redirect_field_name='next', login_url='/login')
@permission_required('post.view_posts', login_url='/login', raise_exception=False)
def postIndex(request):
    posts_all = Posts.objects.order_by('-id').filter(user_id=request.user.id)
    paginator = Paginator(posts_all, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    # posts = Posts.objects.order_by('-id').all()
    context = {'posts': posts}
    return  render(request , 'post/index.html' , context)


@login_required(redirect_field_name='next', login_url='/login')
@permission_required('post.change_posts', login_url='/login', raise_exception=False)
def postEdit(request , post_id):
    try:
        post = Posts.objects.get(id=post_id , user_id = request.user.id)
        context = {'post': post}
        return render(request , 'post/edit.html' , context)

    except :
        return redirect('/u/dashboard/post/index')


@login_required(redirect_field_name='next', login_url='/login')
@permission_required('post.change_posts', login_url='/login', raise_exception=False)
@require_POST
def postUpdate(request , post_id):
    form = PostFormEditValidation(request.POST, request.FILES)
    if not form.is_valid():
        args = {'form' :  form }
        return render(request , 'post/create.html' , args)
    try:
        cover_uploaded_file_url = None
        if request.FILES.get('cover') is not None and request.FILES['cover'] :
            cover = request.FILES['cover'] # .name
            cover_extesion = os.path.splitext(str(cover))[1]
            now = datetime.datetime.now()
            file_path = 'post/' + now.strftime("%Y") + '/' + now.strftime("%m") + '/' + now.strftime("%d") + "/" + uuid.uuid4().hex[:10].lower() + cover_extesion
            fs = FileSystemStorage()
            filename = fs.save(file_path , cover)
            # cover_uploaded_file_url = fs.url(filename)
            cover_uploaded_file_url = file_path

        post = Posts.objects.get(id=post_id , user_id = request.user.id)
        post.title = request.POST['title']
        post.content = request.POST['content']
        if cover_uploaded_file_url is not None :
            post.cover=cover_uploaded_file_url
        post.save()

        if request.FILES.get('gallery') and request.FILES['gallery'] :
            gallery = request.FILES.getlist('gallery') # .name
            for image in gallery :
                image_extesion = os.path.splitext(str(image))[1]
                now = datetime.datetime.now()
                file_path = 'post/' + now.strftime("%Y") + '/' + now.strftime("%m") + '/' + now.strftime("%d") + "/gallery/" + uuid.uuid4().hex[:10].lower() + image_extesion
                fs = FileSystemStorage()
                filename = fs.save(file_path , image)
                gallery_image = post_gallery(post_id=post_id , image=file_path , created_at= timezone.now())
                gallery_image.save()

        messages.info(request, 'Post updated')
    except :
        messages.error(request, 'Something went wrong')
        # pass
    return redirect('/u/dashboard/post/index')


@login_required(redirect_field_name='next', login_url='/login')
@permission_required('post.add_posts', login_url='/login', raise_exception=False)
def postCreate(request):
    return render(request , 'post/create.html')


@login_required(redirect_field_name='next', login_url='/login')
@permission_required('post.add_posts', login_url='/login', raise_exception=False)
@require_POST
def postStore(request):
    form = PostFormValidation(request.POST, request.FILES)
    if not form.is_valid():
        args = {'form' :  form }
        return render(request , 'post/create.html' , args)
    try:
        if request.FILES['cover'] :
            cover = request.FILES['cover'] # .name
            cover_extesion = os.path.splitext(str(cover))[1]
            now = datetime.datetime.now()
            file_path = 'post/' + now.strftime("%Y") + '/' + now.strftime("%m") + '/' + now.strftime("%d") + "/" + uuid.uuid4().hex[:10].lower() + cover_extesion
            fs = FileSystemStorage()
            filename = fs.save(file_path , cover)

        post = Posts(
            title = request.POST['title'] ,
            content = request.POST['content'] ,
            cover=file_path ,
            user_id = request.user.id )
        post.save()

        if request.FILES['gallery'] :
            gallery = request.FILES.getlist('gallery') # .name
            for image in gallery :
                image_extesion = os.path.splitext(str(image))[1]
                now = datetime.datetime.now()
                file_path = 'post/' + now.strftime("%Y") + '/' + now.strftime("%m") + '/' + now.strftime("%d") + "/gallery/" + uuid.uuid4().hex[:10].lower() + image_extesion
                fs = FileSystemStorage()
                filename = fs.save(file_path , image)
                gallery_image = post_gallery(post_id=post.id , image=file_path , created_at= timezone.now())
                gallery_image.save()
        messages.success(request, 'Post Created')
    except :
        messages.error(request, 'Something went wrong')
    return redirect('/u/dashboard/post/index')



