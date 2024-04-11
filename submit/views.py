from django.shortcuts import render


def jm_submit(request):
    return render(request, 'submit/jm_submit.html')

def gm_submit(request):
    return render(request, 'submit/gm_submit.html')

def sj_submit(request):
    return render(request, 'submit/sj_submit.html')

def etc_submit(request):
    return render(request, 'submit/etc_submit.html')