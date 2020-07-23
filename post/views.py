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

