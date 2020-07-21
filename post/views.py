from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='next', login_url='/login')
def dashboard(request):
    return  render(request , 'dashboard.html')
