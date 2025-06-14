from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .utils import resize_image 
from .models import Post, Category
from .forms import PostForm


def saju_list(request):
    return render(request, 'post/saju_list.html')

def naming_list(request):
    return render(request, 'post/naming_list.html')

def post_create(request):
    
    if request.method == 'POST':
        post_form = PostForm(request.POST,request.FILES)
        if post_form.is_valid():
            created_post = post_form.save(commit=False)
            created_post.user = request.user

            # 이미지 리사이징 로직 호출
            if 'image' in request.FILES:  # 'image'는 모델의 이미지 필드명과 일치해야 합니다.
                created_post.image = resize_image(request.FILES['image'])
            
            created_post.save()
            return redirect('post-detail', post_id=created_post.pk)
    
    else:
        post_form = PostForm()
    
    context = {
        'post_form': post_form,
    }
    return render(request, 'post/post_create.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)   
    post.count += 1
    post.save() 
    posts1 = Post.objects.filter(is_all=True).exclude(pk=post_id)
    posts2 = Post.objects.filter(is_side=True).exclude(pk=post_id)
    context = {
        'post': post,
        'posts1': posts1,
        'posts2': posts2,
    }
    return render(request, 'post/post_detail.html', context)

def post_always(request, post_id):
    post = get_object_or_404(Post, pk=post_id)   
    post.is_all = not post.is_all
    post.save()
    return redirect('post-detail', post_id)

def post_sideview(request, post_id):
    post = get_object_or_404(Post, pk=post_id)   
    post.is_side = not post.is_side
    post.save()
    return redirect('post-detail', post_id)

def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST,request.FILES,instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('post-detail', post_id=post.pk)

    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_create.html', {'post_form': form})


@require_POST
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('home')

def post_list(request):
    category_id = request.GET.get('category_id')
    if category_id:
        posts = Post.objects.filter(category__id=category_id)  # 선택된 카테고리에 따라 포스트를 필터링합니다.
    else:
        posts = Post.objects.all()  # 모든 포스트를 가져옵니다.

    categories = Category.objects.all()  # 모든 카테고리를 가져옵니다.
    posts = posts.order_by('-created_at')  
    count = posts.count()
    # 페이지네이션
    paginator = Paginator(posts, 20)  # 페이지당 10개의 게시글을 보여줌
    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 게시글을 가져옴

    context = {
        'page_obj': page_obj,
        'count': count,
        'categories': categories,
    }
    return render(request, 'post/post_list.html', context)