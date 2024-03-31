from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')

def about(request):
    return render(request, 'base/introduce.html')

def jmsubmit(request):
    return render(request, 'base/jmsubmit.html')

