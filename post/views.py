from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from .models import Post
from .forms import PostForm
from PIL import Image

def resize_image(image, max_width=800, max_height=600):
    img = Image.open(image)
    original_width, original_height = img.size

    ratio = min(max_width/original_width, max_height/original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    # 임시 메모리 파일로 이미지를 저장합니다.
    img_io = BytesIO()
    resized_img.save(img_io, format='JPEG', quality=90)  # 또는 img.format 사용
    img_io.seek(0)

    # InMemoryUploadedFile 객체를 생성합니다.
    new_image = InMemoryUploadedFile(img_io, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(img_io), None)

    return new_image



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
    return render(request, 'post/post_detail.html', {'post': post})

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