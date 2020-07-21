from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Posts , Gallery as post_gallery
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required

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
