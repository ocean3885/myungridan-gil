from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from post.models import Post
from .forms import ProfileForm
from .utils import resize_image
from django.core.paginator import Paginator


def home(request):
    return render(request, 'base/home.html')

def saju_base(request):
    posts = Post.objects.all()
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)
    # 페이지네이션
    paginator = Paginator(posts, 6)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴
    context = {
        'page_obj' : page_obj,
        'posts1': posts1,
        'posts2': posts2,
    }
    return render(request, 'base/saju_base.html',context)

def name_base(request):
    posts = Post.objects.all()
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)
    # 페이지네이션
    paginator = Paginator(posts, 6)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴
    context = {
        'page_obj' : page_obj,
        'posts1': posts1,
        'posts2': posts2,
    }
    return render(request, 'base/name_base.html',context)

def dowon_qna(request):
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)
    context = {
        'posts1': posts1,
        'posts2': posts2,
    }
    return render(request, 'base/dowon_qna.html',context)

def submit_info(request):
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)
    context = {
        'posts1': posts1,
        'posts2': posts2,
    }
    return render(request, 'base/submit_info.html',context)

def about(request):
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)
    context = {
        'posts1': posts1,
        'posts2': posts2,
    }
    return render(request, 'base/introduce.html', context)

def dowon_map(request):
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)
    context = {
        'posts1': posts1,
        'posts2': posts2,
    }
    return render(request, 'base/dowon_map.html', context)


def view_profile(request,username):
    profile = get_object_or_404(Profile, user__username=username)
    context = {
        'profile': profile,
    }
    return render(request, 'base/profile/profile.html', context)


def edit_profile(request,username):
    profile = get_object_or_404(Profile, user__username=username)
    if request.user != profile.user:
        return redirect('view-profile', username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)

             # 이미지 리사이징 로직 호출
            if 'picture' in request.FILES:  # 'image'는 모델의 이미지 필드명과 일치해야 합니다.
                profile.picture = resize_image(request.FILES['picture'],200,200)
            if 'bgimg' in request.FILES:  # 'image'는 모델의 이미지 필드명과 일치해야 합니다.
                profile.bgimg = resize_image(request.FILES['bgimg'],800,600)

            profile.save()
            return redirect('view-profile', username)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form
    }
    return render(request, 'base/profile/profile_form.html', context)