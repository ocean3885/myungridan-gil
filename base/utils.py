from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import sys
 

def resize_image(image, max_width=800, max_height=600):
    img = Image.open(image)
    original_width, original_height = img.size

    ratio = min(max_width/original_width, max_height/original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # 임시 메모리 파일로 이미지를 저장합니다.
    img_io = BytesIO()
    
    # 이미지의 형식을 확인하여 저장합니다.
    if img.format == 'JPEG':
        resized_img.save(img_io, format='JPEG', quality=90)
        img_io.seek(0)
        # InMemoryUploadedFile 객체를 생성합니다.
        new_image = InMemoryUploadedFile(
            img_io,
            'ImageField',
            "%s.jpg" % image.name.split('.')[0],  # 파일 이름을 수정하여 확장자를 JPG로 변경합니다.
            'image/jpeg',
            sys.getsizeof(img_io),
            None
        )
    elif img.format == 'PNG':
        resized_img.save(img_io, format='PNG')
        img_io.seek(0)
        # InMemoryUploadedFile 객체를 생성합니다.
        new_image = InMemoryUploadedFile(
            img_io,
            'ImageField',
            "%s.png" % image.name.split('.')[0],  # 파일 이름을 수정하여 확장자를 PNG로 변경합니다.
            'image/png',
            sys.getsizeof(img_io),
            None
        )
    else:
        # 지원하지 않는 형식의 이미지가 입력된 경우, 기본적으로 JPEG 형식으로 저장합니다.
        resized_img.save(img_io, format='JPEG', quality=90)
        img_io.seek(0)
        # InMemoryUploadedFile 객체를 생성합니다.
        new_image = InMemoryUploadedFile(
            img_io,
            'ImageField',
            "%s.jpg" % image.name.split('.')[0],  # 파일 이름을 수정하여 확장자를 JPG로 변경합니다.
            'image/jpeg',
            sys.getsizeof(img_io),
            None
        )

    return new_image