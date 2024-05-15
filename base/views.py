from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, CustomBoard, CustomComment
from post.models import Post
from .forms import ProfileForm, CustomCommentForm, CustomForm
from .utils import resize_image
from django.core.paginator import Paginator
from django.db.models import Q

def get_filtered_posts():
    posts1 = Post.objects.filter(is_first=True)
    posts2 = Post.objects.filter(is_second=True)
    return {
        'posts1': posts1,
        'posts2': posts2,
    }

def home(request):
    posts = Post.objects.order_by('-created_at')[:5]
    latest = posts.first()
    context = {
        'posts': posts,
        'latest': latest
    }
    return render(request, 'base/home.html', context)

def saju_base(request):
    posts1 = Post.objects.filter(
        Q(category__name="성명학") | 
        Q(category__name="작명사례")
        ).order_by('-created_at')[:8]
    posts = Post.objects.filter(
        Q(category__name="일주론") | 
        Q(category__name="사주학") | 
        Q(category__name="유명인사주")
        ).order_by('-created_at')
    
    # 페이지네이션
    paginator = Paginator(posts, 6)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴
    context = {
        'page_obj' : page_obj,
        'posts1': posts1,
    }
    return render(request, 'base/saju_base.html',context)

def name_base(request):
    posts = Post.objects.filter(
        Q(category__name="성명학") | 
        Q(category__name="작명사례")
        ).order_by('-created_at')
    posts1 = Post.objects.filter(
        Q(category__name="일주론") | 
        Q(category__name="사주학") | 
        Q(category__name="유명인사주")
        ).order_by('-created_at')[:8]
    
    # 페이지네이션
    paginator = Paginator(posts, 6)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴
    context = {
        'page_obj' : page_obj,
        'posts1': posts1,
    }
    return render(request, 'base/name_base.html',context)

def dowon_qna(request):
    context = get_filtered_posts()
    return render(request, 'base/dowon_qna.html',context)

def submit_info(request):
    context = get_filtered_posts()
    return render(request, 'base/submit_info.html',context)

def about(request):
    context = get_filtered_posts()
    return render(request, 'base/introduce.html', context)

def dowon_map(request):
    context = get_filtered_posts()
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



def customer_list(request):
    context = get_filtered_posts()
    posts = CustomBoard.objects.all()
    count = posts.count()
    context['count'] = count

    # 페이지네이션
    paginator = Paginator(posts, 20)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴
    context['page_obj'] = page_obj

    return render(request, 'base/customer_list.html',context)

def customer_write(request):
    context = get_filtered_posts()
    customform = CustomForm(request.POST or None)
    
    if request.method == "POST":
        # 제출된 폼 검증
        if customform.is_valid(): 
            obj = customform.save()            
            return redirect('customer-detail', obj.pk)
        else:
            errors = customform.errors
            context['customform'] = customform
            context['errors'] = errors
            return render(request, 'base/customer_write.html', context)

    # GET 요청 또는 유효하지 않은 폼의 경우 초기 폼 표시
    context['customform'] = customform
    return render(request, 'base/customer_write.html',context)


def customer_detail(request,pk):
    context = get_filtered_posts()
    post = get_object_or_404(CustomBoard, pk=pk)
    comment_form = CustomForm()
    comments = post.board_comments.all()
    context['comments'] = comments
    context['comment_form'] = comment_form
    context['post'] = post

    return render(request, 'base/customer_detail.html', context)

def customer_delete(request,pk):
    pass

def customer_edit(request,pk):
    pass

def customer_comment_write(request,pk):
    post = get_object_or_404(CustomBoard, pk=pk)
    if request.method == 'POST':
        form = CustomCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.board = post
            comment.save()
            return redirect('customer-detail', pk)

def customer_comment_delete(request,pk,c_pk):
    comment = get_object_or_404(CustomComment,pk=c_pk)
    comment.delete()
    return redirect('customer-detail',pk)