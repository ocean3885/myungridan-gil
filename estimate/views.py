from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from manseryuk.views import Msr_Calculator
from manseryuk.calculator import determine_zodiac_hour_str
from .forms import EstimateForm
from .models import Estimate
from datetime import datetime


def estimate_form(request):
    submitForm = EstimateForm(request.POST or None)
    
    if request.method == "POST":
        # 제출된 폼 검증
        if submitForm.is_valid(): 
            obj = submitForm.save(commit=False)            
            if request.user.is_authenticated:
                obj.user = request.user
            data = Msr_Calculator()
            time = determine_zodiac_hour_str(obj.hour, obj.min)
            datas = data.getAll(obj.year, obj.month, obj.day,
                        time, obj.sl, obj.gen)
            obj.data = {'datas':datas}
            obj.save()
            return redirect('estimate-detail', pk=obj.pk)
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
    grouped_data = zip(
            submit.data['datas']['daewoon_num_list'],
            submit.data['datas']['daewoon'][1],
            submit.data['datas']['daewoon'][2]
        )
    grouped_year = zip(
            submit.data['datas']['cycles_100'][0],
            submit.data['datas']['cycles_100'][1],
            submit.data['datas']['cycles_100'][2],
        )
    grouped_list = list(grouped_year)
    grouped_chunks = [grouped_list[i:i + 10] for i in range(0, len(grouped_list), 10)]
    current_year = datetime.now().year
    groups_with_visibility = []
    for group in grouped_chunks:
        visible = any(year == current_year for year, _, _ in group)
        groups_with_visibility.append((group, visible))
    context = {
        'submit': submit,
        'grouped_data': grouped_data,
        'groups_with_visibility': groups_with_visibility
    }
    return render(request, 'estimate/estimate_detail.html', context)        

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
    if request.method == 'POST':
        submitForm =EstimateForm(request.POST, instance=submit)
        if submitForm.is_valid():
            submitForm.save()
            return redirect('estimate-detail', pk=submit.pk)
    else:
        submitForm = EstimateForm(instance=submit)
        context = {'submit': submitForm}
    return render(request, 'estimate/estimate_form.html', context)
    

def estimate_delete(request,pk):
    submit = get_object_or_404(Estimate, pk=pk)
    if not request.user.is_staff:
        return redirect('home')
    submit.delete()
    return redirect('estimate-list')


