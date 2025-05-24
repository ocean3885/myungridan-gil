from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import random
from datetime import timedelta
from django.utils import timezone
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


def generate_virtual_submits(existing_submits_count, target_count=5):
    """
    Generates virtual submit data to fill up to a target_count if needed.
    """
    virtual_submits = []
    num_virtual_submits = target_count - existing_submits_count

    if num_virtual_submits <= 0:
        return virtual_submits # No virtual submits needed

    korean_surnames = [
        '김', '이', '박', '최', '정', '강', '조', '윤', '장', '임',
        '한', '오', '서', '신', '권', '황', '안', '송', '전', '홍'
    ]

    for i in range(num_virtual_submits):
        # 1. Name
        random_surname = random.choice(korean_surnames)
        virtual_name = f"{random_surname}ㅇㅇ"

        # 2. Category
        if random.random() < 0.7:
            virtual_category = random.choice(['신생아작명', '개명신청'])
        else:
            virtual_category = '사주상담'

        # 3. Created Date
        if i < 2: # First 2 are today
            virtual_created = timezone.now()
        elif i < 4: # Next 2 are yesterday
            virtual_created = timezone.now() - timedelta(days=1)
        else: # Last one is two days ago
            virtual_created = timezone.now() - timedelta(days=2)

        # Add slight time variance
        virtual_created -= timedelta(minutes=random.randint(0, 59), seconds=random.randint(0, 59))

        # 4. Process Status
        if virtual_created.date() == timezone.now().date():
            virtual_process = '진행중'
        else:
            virtual_process = '완료'

        virtual_submit = {
            'name': virtual_name,
            'get_category_display': virtual_category,
            'created': virtual_created,
            'get_process_display': virtual_process,
        }
        virtual_submits.append(virtual_submit)

    return virtual_submits