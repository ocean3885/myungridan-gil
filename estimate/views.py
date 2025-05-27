from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from manseryuk.calculator import descending_tens, generate_baby_cycles
from .utils import fetch_estimate_data_from_api
from .forms import EstimateForm, CommentForm
from .models import Estimate, Comment
from post.models import Post
from datetime import datetime
from django.http import JsonResponse
from .models import InmyungHanja
from .utils import get_hanja_details_as_json, get_name_suri_details, count_elements
from django.contrib import messages

def get_hanja(request):
    if request.method == 'GET':
        name = request.GET.get('name', '')
        result = []

        for char in name:
            hanja_list = list(
                InmyungHanja.objects.filter(pron=char).values('char', 'main_mean')
            )
            result.append(hanja_list)        
        return JsonResponse({'data': result})

def estimate_form(request, pk=None):
    if pk:
        obj = get_object_or_404(Estimate, pk=pk)
        # 운영자가 아니고, 세션 인증이 없으면 비밀번호 페이지로 리다이렉트
        if not (request.user.is_staff or request.user.is_superuser):
            if not request.session.get(f'estimate_{pk}_auth'):
                return redirect('estimate-password', pk=pk)
        submitForm = EstimateForm(request.POST or None, instance=obj)
        name_hanja = obj.name_hanja
        pk_number = pk
    else:
        submitForm = EstimateForm(request.POST or None)
        name_hanja = ''
        pk_number = None

    if request.method == "POST":
        # 제출된 폼 검증
        if submitForm.is_valid():
            obj = submitForm.save(commit=False)
            if request.user.is_authenticated:
                obj.user = request.user
            # utils.py 함수 호출해서 데이터 가져오기
            api_data = fetch_estimate_data_from_api(
                obj.year,
                obj.month,
                obj.day,
                obj.hour,
                obj.min,
                obj.sl,
                obj.gen,
            )            
            json_output = get_hanja_details_as_json(obj.name_hanja)
            suri_detail = get_name_suri_details(json_output)
            if api_data is None:
                errors = {"api": "외부 API 호출 실패"}
                context = {"submit": submitForm, "errors": errors}
                return render(request, "estimate/estimate_form.html", context)
            obj.data = {"datas": api_data, "hanjainfo": json_output , "suri81": suri_detail}
            obj.save()
            request.session[f'estimate_{obj.pk}_auth'] = True
            return redirect("estimate-detail", pk=obj.pk)
        else:
            errors = submitForm.errors
            context = {"submit": submitForm, "errors": errors}
            return render(request, "estimate/estimate_form.html", context)

    # GET 요청 또는 유효하지 않은 폼의 경우 초기 폼 표시
    context = {"submit": submitForm, "name_hanja": name_hanja, "pk_number": pk_number}
    return render(request, "estimate/estimate_form.html", context)


def estimate_detail(request, pk):
    submit = get_object_or_404(Estimate, pk=pk)
    if submit.is_secret:
        # 세션에 인증 기록이 없으면 비밀번호 페이지로 리다이렉트
        if not request.session.get(f'estimate_{pk}_auth'):
            return redirect('estimate-password', pk=pk)
    submit.count += 1
    submit.save()
    comments = submit.comments.all()
    comment_form = CommentForm()
    grouped_chunks = submit.data['datas']['decadeCycles']
    current_year = datetime.now().year
    nowcycle = generate_baby_cycles(current_year)
    groups_with_visibility = []
    grouped_data_visibility = []
    for group in grouped_chunks:
        visible = any(year == current_year for year, _, _ in group)
        groups_with_visibility.append((group, visible))
        grouped_data_visibility.append(visible)
    grouped_data_visibility.reverse()
    grouped_data = zip(
            descending_tens(submit.data['datas']['daewoon_num']),
            submit.data['datas']['daewoon'][1],
            submit.data['datas']['daewoon'][2],
            grouped_data_visibility
        )
    all_false = all(not value for value in grouped_data_visibility)
    chars = submit.data['datas']['year_hgan'] + submit.data['datas']['month_hgan'] + submit.data['datas']['day_hgan'] + submit.data['datas']['time_hgan'] + submit.data['datas']['year_hji'] + submit.data['datas']['month_hji'] + submit.data['datas']['day_hji'] + submit.data['datas']['time_hji'] 
    context = {
        "submit": submit,
        'grouped_data': grouped_data,
        "groups_with_visibility": groups_with_visibility,
        "all_false": all_false,
        "comments": comments,
        "comment_form": comment_form,
        'nowcycle': nowcycle,
        'chartdata': count_elements(chars)
    }
    return render(request, "estimate/estimate_detail.html", context)


def estimate_password(request, pk):
    post = get_object_or_404(Estimate, pk=pk)
    if request.method == 'POST':
        input_password = request.POST.get('password')
        if input_password == post.password:  # 실제 암호 비교 로직
            # 세션에 인증 표시
            request.session[f'estimate_{pk}_auth'] = True
            return redirect('estimate-detail', pk=pk)
        else:
            error = '비밀번호가 틀렸습니다.'
            return render(request, 'estimate/verify_form.html', {'submit': post, 'error': error})
    return render(request, 'estimate/verify_form.html', {'submit': post})

def estimate_list(request):
    submits = Estimate.objects.all()
    count = submits.count()
    submits = submits.order_by("-created")
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)

    # 페이지네이션
    paginator = Paginator(submits, 15)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get("page")  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴

    context = {
        "page_obj": page_obj,
        "count": count,
        "posts1": posts1,
        "posts2": posts2,
    }

    return render(request, "estimate/estimate_list.html", context)


def estimate_delete(request, pk):
    obj = get_object_or_404(Estimate, pk=pk)
    
    # 권한 체크: 운영자 아니고, 세션 인증 없으면 비밀번호 페이지로 리다이렉트
    if not (request.user.is_staff or request.user.is_superuser):
        if not request.session.get(f'estimate_{pk}_auth'):
            return redirect('estimate-password', pk=pk)
    
    if request.method == "POST":
        obj.delete()
        messages.success(request, "감명신청이 삭제되었습니다.")
        return redirect('estimate-list')  # 리스트 페이지 이름으로 바꾸세요
    
    # GET 요청이면 삭제 확인 페이지 보여주기
    return render(request, 'estimate/estimate_confirm_delete.html', {'submit': obj})



def add_comment(request, pk):
    submit = get_object_or_404(Estimate, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = submit
            submit.process = 2
            comment.save()
            submit.save()
            return redirect("estimate-detail", pk)


def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    submit = get_object_or_404(Estimate, pk=post_id)
    comment.delete()
    if not submit.comments.count():
        comment.post.process = 1
        comment.post.save()
    return redirect("estimate-detail", post_id)
