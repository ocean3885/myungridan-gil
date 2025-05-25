from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from manseryuk.views import Msr_Calculator
from manseryuk.calculator import determine_zodiac_hour_str, descending_tens, generate_baby_cycles
from .utils import fetch_estimate_data_from_api
from .forms import EstimateForm, CommentForm
from .models import Estimate, Comment
from post.models import Post
from datetime import datetime
from django.http import JsonResponse
from .models import InmyungHanja

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

def estimate_form(request):
    submitForm = EstimateForm(request.POST or None)

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

            if api_data is None:
                errors = {"api": "외부 API 호출 실패"}
                context = {"submit": submitForm, "errors": errors}
                return render(request, "estimate/estimate_form.html", context)
            obj.data = {"datas": api_data}
            obj.save()
            return redirect("estimate-detail", pk=obj.pk)
        else:
            errors = submitForm.errors
            context = {"submit": submitForm, "errors": errors}
            return render(request, "estimate/estimate_form.html", context)

    # GET 요청 또는 유효하지 않은 폼의 경우 초기 폼 표시
    context = {"submit": submitForm}
    return render(request, "estimate/estimate_form.html", context)


def estimate_detail(request, pk):
    submit = get_object_or_404(Estimate, pk=pk)
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
    grouped_data = zip(
            descending_tens(submit.data['datas']['daewoon_num']),
            submit.data['datas']['daewoon'][1],
            submit.data['datas']['daewoon'][2],
            grouped_data_visibility
        )

    all_false = all(not value for value in grouped_data_visibility)
    context = {
        "submit": submit,
        'grouped_data': grouped_data,
        "groups_with_visibility": groups_with_visibility,
        "all_false": all_false,
        "comments": comments,
        "comment_form": comment_form,
        'nowcycle': nowcycle,
    }
    return render(request, "estimate/estimate_detail.html", context)


def estimate_list(request):
    submits = Estimate.objects.all()
    count = submits.count()
    submits = submits.order_by("-created")
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)

    # 페이지네이션
    paginator = Paginator(submits, 20)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get("page")  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴

    context = {
        "page_obj": page_obj,
        "count": count,
        "posts1": posts1,
        "posts2": posts2,
    }

    return render(request, "estimate/estimate_list.html", context)


def estimate_edit(request, pk):
    submit = get_object_or_404(Estimate, pk=pk)
    if request.method == "POST":
        submitForm = EstimateForm(request.POST, instance=submit)
        if submitForm.is_valid():
            obj = submitForm.save(commit=False)
            if request.user.is_authenticated:
                obj.user = request.user
            data = Msr_Calculator()
            time = determine_zodiac_hour_str(obj.hour, obj.min)
            datas = data.getAll(obj.year, obj.month, obj.day, time, obj.sl, obj.gen)
            obj.data = {"datas": datas}
            obj.save()
            return redirect("estimate-detail", pk)
    else:
        submitForm = EstimateForm(instance=submit)
        context = {"submit": submitForm}
    return render(request, "estimate/estimate_form.html", context)


def verify_edit(request, pk):
    if request.method == "POST":
        submit = get_object_or_404(Estimate, pk=pk)
        estimate_name = request.POST.get("estimate_name")
        estimate_phone = request.POST.get("estimate_phone")
        if submit.name == estimate_name and submit.phone == estimate_phone:
            request.session["estimate_name"] = estimate_name
            request.session["estimate_phone"] = estimate_phone
            return redirect("estimate-edit", pk)
        else:
            return render(request, "estimate/verify_form.html", {"wrong": True})
    else:
        return render(request, "estimate/verify_form.html")


def verify_delete(request, pk):
    if request.method == "POST":
        submit = get_object_or_404(Estimate, pk=pk)
        estimate_name = request.POST.get("estimate_name")
        estimate_phone = request.POST.get("estimate_phone")
        if submit.name == estimate_name and submit.phone == estimate_phone:
            submit.delete()
            return redirect("estimate-list")
        else:
            return render(request, "estimate/verify_form.html", {"wrong": True})
    else:
        return render(request, "estimate/verify_form.html", {"delete": True})


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
