from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import (JmSubmitForm, PersonForm)
from .models import Submit, Person
import requests

send_url = 'https://apis.aligo.in/send/'

def jm_submit(request):
    if request.method == "POST":
        submitForm = JmSubmitForm(request.POST)
        personForm = PersonForm(request.POST)
        if all([submitForm.is_valid(), personForm.is_valid()]):
            obj = submitForm.save(commit=False)
            obj.category = "jm"
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()
            person = personForm.save(commit=False)
            person.submit = obj
            person.save()
            sms_data = {'key': 'mbam9e8v586xu9vugol89i2wxvihrv9l',
                        'userid': 'ocean3885',
                        'sender': '01022324548',
                        'receiver': '01022324548',
                        'msg': '작명신청이 접수되었습니다.'
                        }
            send_response = requests.post(send_url, data=sms_data)
            print(send_response.json())
            return redirect('submit-detail', pk=obj.pk)
        else:
            context = {'submit': submitForm, 'person': personForm}
            return render(request, 'submit/jm_submit.html', context)

    submitForm = JmSubmitForm()
    personForm = PersonForm()
    context = {'submit': submitForm, 'person': personForm}
    return render(request, 'submit/jm_submit.html', context)

def submit_detail(request,pk):
    submit = get_object_or_404(Submit, pk=pk)
    person = Person.objects.get(submit__id=submit.id)
    return render(request, 'submit/submit_detail.html', {'submit': submit, 'person': person})


def gm_submit(request):
    return render(request, 'submit/gm_submit.html')

def sj_submit(request):
    return render(request, 'submit/sj_submit.html')

def etc_submit(request):
    return render(request, 'submit/etc_submit.html')

def submit_list(request, status=''):
    if status:
        submits = Submit.objects.filter(process=status)
    else:
        submits = Submit.objects.all()
    
    count = submits.count()
    # 정렬
    submits = submits.order_by('-created')  # 최근 작성된 게시글부터 정렬

    # 페이지네이션
    paginator = Paginator(submits, 10)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴

    context = {
        'page_obj': page_obj,
        'count': count,
        'status': status
    }

    return render(request, 'submit/list.html', context)

def submit_edit(request,pk):
    submit = get_object_or_404(Submit, pk=pk)
    person = Person.objects.get(submit__id=submit.id)
    if request.method == 'POST':
        submitForm = JmSubmitForm(request.POST,instance=submit)
        personForm = PersonForm(request.POST,instance=person)
        if all([submitForm.is_valid(), personForm.is_valid()]):
            submitForm.save()
            personForm.save()
            return redirect('submit-detail', pk=submit.pk)
    else:
        submitForm = JmSubmitForm(instance=submit)
        personForm = PersonForm(instance=person)
        context = {'submit': submitForm, 'person': personForm}
    return render(request, 'submit/jm_submit.html', context)

def submit_delete(request,pk):
    submit = get_object_or_404(Submit, pk=pk)
    submit.delete()
    return redirect('submit-list')
