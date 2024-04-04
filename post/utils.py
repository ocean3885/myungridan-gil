from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from ckeditor_uploader.views import ImageUploadView as BaseImageUploadView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import sys
import io
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

@method_decorator(csrf_exempt, name='dispatch')
class CustomImageUploadView(BaseImageUploadView):
    def post(self, request, **kwargs):
        uploaded_file = request.FILES.get('upload')
        if uploaded_file:
            # 이미지 파일을 PIL 이미지 객체로 변환
            image = Image.open(uploaded_file)
            # 리사이징할 이미지 크기 지정
            image = image.resize((800, int((image.height / image.width) * 800)))

            # 리사이징된 이미지를 다시 파일로 변환
            resized_image = io.BytesIO()
            image_format = image.format if image.format else 'JPEG'
            image.save(resized_image, format=image_format)
            resized_image.seek(0)
            uploaded_file.file = resized_image

        # 부모 클래스의 post 메소드 호출
        return super().post(request, **kwargs)