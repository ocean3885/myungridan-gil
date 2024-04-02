from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
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
    return render(request, 'post/post_detail.html', {'post': post})



