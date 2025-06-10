from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Profile, CustomBoard, CustomComment
from post.models import Post
from submit.models import Submit
from .forms import ProfileForm, CustomCommentForm, CustomForm
from .utils import generate_virtual_submits
from .utils import resize_image
from django.core.paginator import Paginator
from django.db.models import Q
from submit.utils import get_client_ip, is_rate_limited, update_last_post_time
from django.http import HttpResponse


def get_filtered_posts():
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)
    return {
        "posts1": posts1,
        "posts2": posts2,
    }

def home(request):
    # 최신 게시글 5개 추출
    posts = Post.objects.order_by("-created_at")[:5]

    # 최신 커스텀 보드 5개 추출 및 댓글 수 계산
    boards = CustomBoard.objects.order_by("-created_at")[:5]
    for board in boards:
        board.comment_count = board.board_comments.count()

    # 가장 최신 게시글 (Post 모델)
    latest = posts.first()

    # Submit 모델에서 최근 3일 이내 올라온 글 추출
    three_days_ago = timezone.now() - timedelta(days=3)
    recent_submits = Submit.objects.filter(created__gte=three_days_ago).order_by(
        "-created"
    )[:5]
    submits = list(recent_submits)

    # Generate virtual submits if needed
    if len(submits) < 5:
        virtual_submits = generate_virtual_submits(len(submits))
        submits = submits + virtual_submits
        # Sort and limit again to ensure exactly 5 in descending order
        submits = sorted(
            submits,
            key=lambda x: x.created if hasattr(x, "created") else x["created"],
            reverse=True,
        )[:5]
        
    # Context 딕셔너리 생성
    context = {
        "posts": posts,
        "latest": latest,
        "boards": boards,
        "submits": submits,
    }

    return render(request, "base/home.html", context)


def saju_base(request):
    posts1 = Post.objects.filter(
        Q(category__name="성명학") | Q(category__name="작명사례")
    ).order_by("-created_at")[:8]
    posts = Post.objects.filter(
        Q(category__name="일주론")
        | Q(category__name="사주학")
        | Q(category__name="유명인사주")
    ).order_by("-created_at")

    # 페이지네이션
    paginator = Paginator(posts, 6)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get("page")  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴
    context = {
        "page_obj": page_obj,
        "posts1": posts1,
    }
    return render(request, "base/saju_base.html", context)


def name_base(request):
    posts = Post.objects.filter(
        Q(category__name="성명학") | Q(category__name="작명사례")
    ).order_by("-created_at")
    posts1 = Post.objects.filter(
        Q(category__name="일주론")
        | Q(category__name="사주학")
        | Q(category__name="유명인사주")
    ).order_by("-created_at")[:8]

    # 페이지네이션
    paginator = Paginator(posts, 6)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get("page")  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴
    context = {
        "page_obj": page_obj,
        "posts1": posts1,
    }
    return render(request, "base/name_base.html", context)


def dowon_qna(request):
    context = get_filtered_posts()
    return render(request, "base/dowon_qna.html", context)


def submit_info(request):
    context = get_filtered_posts()
    return render(request, "base/submit_info.html", context)


def about(request):
    context = get_filtered_posts()
    return render(request, "base/introduce.html", context)


def dowon_map(request):
    context = get_filtered_posts()
    return render(request, "base/dowon_map.html", context)


def view_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    context = {
        "profile": profile,
    }
    return render(request, "base/profile/profile.html", context)


def edit_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    if request.user != profile.user:
        return redirect("view-profile", username)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)

            # 이미지 리사이징 로직 호출
            if (
                "picture" in request.FILES
            ):  # 'image'는 모델의 이미지 필드명과 일치해야 합니다.
                profile.picture = resize_image(request.FILES["picture"], 200, 200)
            if (
                "bgimg" in request.FILES
            ):  # 'image'는 모델의 이미지 필드명과 일치해야 합니다.
                profile.bgimg = resize_image(request.FILES["bgimg"], 800, 600)

            profile.save()
            return redirect("view-profile", username)
    else:
        form = ProfileForm(instance=profile)

    context = {"profile": profile, "form": form}
    return render(request, "base/profile/profile_form.html", context)


def customer_list(request):
    context = get_filtered_posts()
    posts = CustomBoard.objects.all().order_by("-created_at")
    for post in posts:
        post.comment_count = post.board_comments.count()
    count = posts.count()
    context["count"] = count

    # 페이지네이션
    paginator = Paginator(posts, 20)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get("page")  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴
    context["page_obj"] = page_obj

    return render(request, "base/customer_list.html", context)


def customer_write(request):
    context = get_filtered_posts()
    customform = CustomForm(request.POST or None)

    if request.method == "POST":
        
        # 작성 제한 시간 (예: 60초)
        limit_seconds = 60
        # IP 주소 가져오기
        ip_address = get_client_ip(request)
        # 캐시 키 설정 (IP 기반)
        cache_key = f'post_limit_{ip_address}'
        # 속도 제한 확인
        is_limited, remaining_time = is_rate_limited(cache_key, limit_seconds)
        if is_limited:
            return HttpResponse("글 작성은 60초 후에 가능합니다.", status=429)
        
        # 제출된 폼 검증
        if customform.is_valid():
            obj = customform.save()
            update_last_post_time(cache_key, timeout=limit_seconds)
            return redirect("customer-detail", obj.pk)
        else:
            errors = customform.errors
            context["customform"] = customform
            context["errors"] = errors
            return render(request, "base/customer_write.html", context)

    # GET 요청 또는 유효하지 않은 폼의 경우 초기 폼 표시
    context["customform"] = customform
    return render(request, "base/customer_write.html", context)


def customer_detail(request, pk):
    context = get_filtered_posts()
    post = get_object_or_404(CustomBoard, pk=pk)
    if not request.user.is_staff and post.is_secret:
        verification_key = f'post_{pk}_verified_for_view'
        if not request.session.get(verification_key):
            return redirect('customer-password-check', pk=pk, action='view')
        else:
            # 인증 정보를 확인했으면 바로 삭제
            del request.session[verification_key] 
        
    comment_form = CustomForm()
    comments = post.board_comments.all()
    context["comments"] = comments
    context["comment_form"] = comment_form
    context["post"] = post

    return render(request, "base/customer_detail.html", context)


def customer_delete(request, pk):
    post = get_object_or_404(CustomBoard, pk=pk)
    
    # 관리자라면 바로 삭제
    if request.user.is_staff:
        post.delete()
        return redirect("customer-list")
    
    verification_key = f'post_{pk}_verified_for_delete'
    if not request.session.get(verification_key):
        return redirect('customer-password-check', pk=pk, action='delete')
    
    if request.method == "POST":
        password = request.POST.get("password")
        if post.password == password:
            post.delete()
            del request.session[verification_key]
            return redirect("customer-list")
        else:
            context = {"error":True, "action": "delete"}
            return render(request, "base/verify_form.html", context)
    context = { "action": "delete"}
    return render(request, "base/verify_form.html", context)


def customer_edit(request, pk):
    context = get_filtered_posts()
    post = get_object_or_404(CustomBoard, pk=pk)
    verification_key = f'post_{pk}_verified_for_edit'
    if not request.session.get(verification_key):
        return redirect('customer-password-check', pk=pk, action='edit')
    # 인증 정보를 사용한 후에는 삭제하여 재사용 방지
    if request.method == "POST":
        customform = CustomForm(request.POST, instance=post)
        if customform.is_valid():
            customform.save()
            if verification_key in request.session:
                del request.session[verification_key]
            request.session[f'post_{pk}_verified_for_view'] = True
            return redirect("customer-detail", pk)
    customform = CustomForm(instance=post)
    context["customform"] = customform
    # context["error"] = False
    return render(request, "base/customer_write.html", context)


def customer_password_check(request, pk, action):
    post = get_object_or_404(CustomBoard, pk=pk)

    if request.method == "POST":
        password = request.POST.get("password")
        if post.password == password:
            request.session[f'post_{pk}_verified_for_{action}'] = True
            if action == 'view':
                return redirect('customer-detail', pk=pk)
            elif action == 'edit':
                return redirect('customer-edit', pk=pk)
            elif action == 'delete':
                return redirect('customer-delete', pk=pk)
        else:
            context = {"error": True, "action": action}
            return render(request, "base/verify_form.html", context)
    else:
        context = {"action":action}
        return render(request, "base/verify_form.html", context)


def customer_comment_write(request, pk):
    post = get_object_or_404(CustomBoard, pk=pk)
    if request.method == "POST":
        form = CustomCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.board = post
            comment.save()
            return redirect("customer-detail", pk)


def customer_comment_delete(request, pk, c_pk):
    comment = get_object_or_404(CustomComment, pk=c_pk)
    comment.delete()
    return redirect("customer-detail", pk)
