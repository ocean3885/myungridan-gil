from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from manseryuk.views import Msr_Calculator
from manseryuk.calculator import determine_zodiac_hour_str
from .forms import EstimateForm
from .models import Estimate

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
            errors = submitForm.errors
            context = {'submit': submitForm,'errors':errors}
            return render(request, 'estimate/estimate_form.html', context)

    # GET 요청 또는 유효하지 않은 폼의 경우 초기 폼 표시
    context = {'submit': submitForm}
    return render(request, 'estimate/estimate_form.html', context)

def estimate_detail(request,pk):
    submit = get_object_or_404(Estimate, pk=pk)
    submit.count += 1
    submit.save()
    data = Msr_Calculator()
    time = determine_zodiac_hour_str(submit.hour, submit.min)
    datas = data.getAll(submit.year, submit.month, submit.day,
                        time, submit.sl, submit.gen)
    return render(request, 'estimate/estimate_detail.html', {'submit': submit,'datas':datas})        

def estimate_list(request):
    submits = Estimate.objects.all()
    count = submits.count()
    submits = submits.order_by('-created')  

    # 페이지네이션
    paginator = Paginator(submits, 20)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴

    context = {
        'page_obj': page_obj,
        'count': count,
    }

    return render(request, 'estimate/estimate_list.html', context)

def estimate_edit(request,pk):
    submit = get_object_or_404(Estimate, pk=pk)
    submitForm = EstimateForm(request.POST)
    if request.method == 'POST':
        submitForm =submitForm(request.POST, instance=submit)
        if submitForm.is_valid():
            submitForm.save()
            return redirect('estimate-detail', pk=submit.pk)
    else:
        submitForm = submitForm(instance=submit)
        context = {'submit': submitForm}
    return render(request, 'estimate/estimate_form.html', context)
    

def estimate_delete(request,pk):
    submit = get_object_or_404(Estimate, pk=pk)
    if not request.user.is_staff:
        return redirect('home')
    submit.delete()
    return redirect('estimate-list')


