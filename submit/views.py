from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .utils import staff_or_valid_session_check, user_passes_test_with_request, staff_check
from django.core.paginator import Paginator
from .forms import (NameSubmitForm, SajuSubmitForm, EtcSubmitForm, PersonForm)
from .models import Submit, Person
from django.http import Http404
import requests

send_url = 'https://apis.aligo.in/send/'

def submit_form(request, category):
    # 폼 초기화: 카테고리에 따라 적절한 폼 사용
    if category == "sj":
        submitForm = SajuSubmitForm(request.POST or None)
        personForm = PersonForm(request.POST or None)
    elif category == "etc":
        submitForm = EtcSubmitForm(request.POST or None)
        personForm = None  # 'etc' 카테고리의 경우 personForm이 필요 없음
    elif category in ["jm", "gm"]:
        submitForm = NameSubmitForm(request.POST or None)
        personForm = PersonForm(request.POST or None)
    
    if request.method == "POST":
        # 제출된 폼 검증
        if submitForm.is_valid() and (personForm is None or personForm.is_valid()):
            obj = submitForm.save(commit=False)
            obj.category = category
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()

            # personForm이 존재할 경우 추가 처리
            if personForm is not None:
                person = personForm.save(commit=False)
                person.submit = obj
                person.save()

            # SMS 전송 가정
            sms_data = {
                'key': 'mbam9e8v586xu9vugol89i2wxvihrv9l',
                'userid': 'ocean3885',
                'sender': '01022324548',
                'receiver': '01022324548',
                'msg': '신청이 접수되었습니다.'
            }
            send_response = requests.post(send_url, data=sms_data)  # send_url은 정의되어야 함
            print(send_response.json())
            request.session['submit_name'] = obj.name
            return render(request, 'submit/submit_detail.html', {'submit': obj, 'person': person if personForm else None})
        else:
            context = {'submit': submitForm, 'person': personForm}
            return render(request, 'submit/submit_form.html', context)

    # GET 요청 또는 유효하지 않은 폼의 경우 초기 폼 표시
    context = {'submit': submitForm, 'person': personForm, 'category': category}
    return render(request, 'submit/submit_form.html', context)

def submit_detail(request,pk):
    submit = get_object_or_404(Submit, pk=pk)
    # Person 객체를 안전하게 가져오기
    try:
        person = Person.objects.get(submit__id=submit.id)
    except Person.DoesNotExist:
        person = None  # Person 객체가 없으면 None으로 설정

    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'submit/submit_detail.html', {'submit': submit, 'person': person})    
    
    name = request.session.get('submit_name', False)
    phone = request.session.get('submit_phone', False)
    if name == submit.name:    
        #신청이 2개 이상인경우 submit_phone세션에 phone입력    
        if phone:            
            session = True
            #상세페이지에 session 이 true인 경우에만 목록 표시
            return render(request, 'submit/submit_detail.html', {'submit': submit, 'person': person, 'session': session})        
        else:
            #신청이 1개인경우 home 버튼 표시
            return render(request, 'submit/submit_detail.html', {'submit': submit, 'person': person})        
    else:        
        #운영자도아니고 verify과정도 안거쳤고 신청서작성하지도 않은경우
        return render(request, 'submit/submit_verify.html')


def submit_verify(request):
    if request.method == "POST":
        submit_name = request.POST.get('submit_name')
        submit_phone = request.POST.get('submit_phone')
        submits = Submit.objects.filter(name=submit_name, phone=submit_phone)
        # 객체 수에 따른 조건 분기
        if not submits:
            # 쿼리셋이 비어 있을 경우
            return render(request,'submit/submit_verify.html',{'no_submit': True})  
        elif len(submits) == 1:
            # 쿼리셋에 객체가 하나만 있는 경우
            submit = submits.first()
            person = Person.objects.get(submit__id=submit.id)
            request.session['submit_name'] = submit.name
            request.session.pop('submit_phone', None)
            return render(request,'submit/submit_detail.html',{'submit': submit, 'person': person}) 
        else:
            # 쿼리셋에 여러 객체가 있는 경우
            request.session['submit_name'] = submit_name
            request.session['submit_phone'] = submit_phone
            return redirect('submit-verify-list')
    else:
        return render(request, 'submit/submit_verify.html')
        
    

def submit_verify_list(request):
    name = request.session['submit_name']
    phone = request.session['submit_phone']
    submits = Submit.objects.filter(name=name, phone=phone)
    count = submits.count()
    context = {
        'submits': submits,
        'count': count,
    }

    return render(request,'submit/submit_verify_list.html',context)


@user_passes_test(staff_check, login_url='/')
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

@user_passes_test_with_request(staff_or_valid_session_check)
def submit_edit(request, pk):
    submit = get_object_or_404(Submit, pk=pk)
    category = submit.category

    # 폼 인스턴스를 선택하는 로직
    if submit.category == "sj":
        submitFormClass = SajuSubmitForm
    elif submit.category == "etc":
        submitFormClass = EtcSubmitForm
    else:
        submitFormClass = NameSubmitForm
    
    try:
        # "etc" 카테고리가 아닐 때만 Person 오브젝트를 가져옴
        if submit.category != "etc":
            person = Person.objects.get(submit__id=submit.id)
        else:
            person = None
    except Person.DoesNotExist:
        return Http404("Person object does not exist.")
    
    session_name = request.session.get('submit_name', None)
    if not (request.user.is_staff or (session_name and session_name == submit.name)):
        return redirect('home')

    if request.method == 'POST':
        submitForm = submitFormClass(request.POST, instance=submit)
        if person:
            personForm = PersonForm(request.POST, instance=person)
        if submitForm.is_valid() and (not person or personForm.is_valid()):
            submitForm.save()
            if person:
                personForm.save()
            return redirect('submit-detail', pk=submit.pk)
    else:
        submitForm = submitFormClass(instance=submit)
        if person:
            personForm = PersonForm(instance=person)
        context = {'submit': submitForm, 'person': personForm if person else None, 'category': category}
    return render(request, 'submit/submit_form.html', context)


@user_passes_test_with_request(staff_or_valid_session_check)
def submit_delete(request,pk):
    submit = get_object_or_404(Submit, pk=pk)
    session_name = request.session.get('submit_name', None)
    if not (request.user.is_staff or (session_name and session_name == submit.name)):
        return redirect('home')
    submit.delete()
    return redirect('submit-list')
