from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Text, Image
from .forms import PostForm, TextForm, ImageForm


def saju_list(request):
    return render(request, 'post/saju_list.html')

def naming_list(request):
    return render(request, 'post/naming_list.html')

def post_create(request):
    TextFormSet = inlineformset_factory(Post, Text, form=TextForm, extra=1, can_delete=True)
    ImageFormSet = inlineformset_factory(Post, Image, form=ImageForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            created_post = post_form.save()
            text_formset = TextFormSet(request.POST, instance=created_post)
            image_formset = ImageFormSet(request.POST, request.FILES, instance=created_post)
            if text_formset.is_valid() and image_formset.is_valid():
                text_formset.save()
                image_formset.save()
                return redirect('post-detail', post_id=created_post.pk)
    
    else:
        post_form = PostForm()
        text_formset = TextFormSet()
        image_formset = ImageFormSet()
    
    context = {
        'post_form': post_form,
        'text_formset': text_formset,
        'image_formset': image_formset,
    }
    return render(request, 'post/post_create.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post/post_detail.html', {'post': post})



