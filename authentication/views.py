from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import (render, get_object_or_404)
from django.contrib.auth.models import User
from authentication.forms import ProfileEditForm


def profile(request, username=None):

    user = get_object_or_404(User, username=username)

    # user_context = {'username': user.username}

    return render(request, template_name='profile.html')


def edit_profile(request, username=None):

    if request.method == 'POST':
        form = ProfileEditForm(request.POST)

    else:
        form = ProfileEditForm(instance=request.user.profile)

    return render(request, template_name='edit_profile.html', context={'form': form})
