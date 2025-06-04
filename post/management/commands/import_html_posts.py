import os
import re
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files import File
from django.contrib.auth.models import User
from post.models import Post, Category  


class Command(BaseCommand):
    help = 'Import HTML files from the data folder and save them as posts in numerical order'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')
        img_dir = os.path.join(data_dir, 'img')
        default_image_path = os.path.join(data_dir, 'default.jpg')

        if not os.path.exists(data_dir):
            self.stderr.write(self.style.ERROR(f"Data directory does not exist: {data_dir}"))
            return

        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR("User with ID 1 does not exist."))
            return

        try:
            category = Category.objects.get(id=1)
        except Category.DoesNotExist:
            self.stderr.write(self.style.ERROR("Category with ID 1 does not exist."))
            return

        # img 폴더의 png 파일 목록 로드
        png_files = {}
        if os.path.exists(img_dir):
            png_files = {
                os.path.splitext(png)[0]: os.path.join(img_dir, png)
                for png in os.listdir(img_dir)
                if png.endswith(".png")
            }
        else:
            self.stdout.write(self.style.WARNING(f"Image directory does not exist: {img_dir}. Proceeding without specific images."))

        # HTML 파일 목록을 가져와서 정렬
        html_filenames = []
        for f_name in os.listdir(data_dir):
            if f_name.endswith(".html"):
                html_filenames.append(f_name)

        # 파일명 시작의 숫자를 추출하여 정렬하기 위한 함수
        def extract_number(filename):
            # "1. filename.html" -> "1"
            # "10. filename.html" -> "10"
            match = re.match(r"(\d+)\.", filename)
            if match:
                return int(match.group(1))
            return float('inf') # 숫자로 시작하지 않는 파일은 맨 뒤로 (또는 에러 처리)

        html_filenames.sort(key=extract_number) # 숫자 기준으로 파일명 정렬

        if not html_filenames:
            self.stdout.write(self.style.WARNING(f"No HTML files found in {data_dir}"))
            return

        for filename in html_filenames: # 정렬된 파일 목록으로 반복
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error reading file {filename}: {e}"))
                continue # 다음 파일로 넘어감

            title = os.path.splitext(filename)[0]

            # 이미지 매칭: png 파일명(확장자 제외)이 html 파일명(확장자 제외)에 포함되면 해당 이미지 사용
            matched_image_path = None
            # png_files의 키(파일명)가 현재 html 제목(title)에 포함되는지 확인
            # 예를 들어, title="1. introduction" 이고 png_files에 "introduction" 키가 있다면 매칭
            for keyword, path in png_files.items():
                # 보다 정확한 매칭을 위해, title에서 숫자와 점, 공백을 제거한 부분과 비교할 수도 있습니다.
                # 예: "1. topic name" -> "topic name"
                # clean_title_part = re.sub(r"^\d+\.\s*", "", title)
                # if keyword.lower() in clean_title_part.lower():
                if keyword in title: # 기존 로직 유지
                    matched_image_path = path
                    break

            try:
                post = Post(
                    title=title,
                    content=content,
                    user=user,
                    category=category,
                    # created_at, updated_at은 model에서 auto_now_add=True, auto_now=True로 설정하는 것이 일반적
                    # 여기서는 명시적으로 설정
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )

                # 이미지 저장
                image_attached = False
                if matched_image_path and os.path.exists(matched_image_path):
                    with open(matched_image_path, 'rb') as img_file:
                        image_filename = os.path.basename(matched_image_path)
                        post.image.save(image_filename, File(img_file), save=False) # post.save()는 나중에 한번만
                        image_attached = True
                elif os.path.exists(default_image_path):
                    with open(default_image_path, 'rb') as default_file:
                        post.image.save('default.jpg', File(default_file), save=False) # post.save()는 나중에 한번만
                        image_attached = True
                else:
                    self.stdout.write(self.style.WARNING(f"No specific or default image found for post: {title}"))

                post.save() # Post 객체와 함께 FileField에 연결된 파일도 이때 저장됩니다.
                if image_attached:
                    self.stdout.write(self.style.SUCCESS(f"✅ Imported post: {title} with image: {post.image.name}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"✅ Imported post: {title} (no image attached)"))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error creating post for {filename}: {e}"))