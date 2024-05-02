from django.shortcuts import render, get_object_or_404
from .models import Profile

def home(request):
    return render(request, 'base/home.html')

def about(request):
    return render(request, 'base/introduce.html')


def view_profile(request,username):
    profile = get_object_or_404(Profile, user__username=username)
    context = {
        'profile': profile,
    }
    return render(request, 'base/profile/profile.html', context)


