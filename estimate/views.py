from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import EstimateForm
from .models import Estimate
from django.http import Http404
import requests

def estimate_form(request):
    submitForm = EstimateForm(request.POST or None)
    
    if request.method == "POST":
        # 제출된 폼 검증
        if submitForm.is_valid(): 
            obj = submitForm.save(commit=False)
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()
            return render(request, 'estimate/estimate_detail.html', {'submit': obj})
        else:
            context = {'submit': submitForm}
            return render(request, 'estimate/estimate_form.html', context)

    # GET 요청 또는 유효하지 않은 폼의 경우 초기 폼 표시
    context = {'submit': submitForm}
    return render(request, 'estimate/estimate_form.html', context)

