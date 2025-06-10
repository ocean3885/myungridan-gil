# your_app/management/commands/import_scheduled_items.py

import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from base.models import ScheduledItem

class Command(BaseCommand):
    help = 'management/commands/data/ 폴더에 있는 CSV 파일을 읽어 ScheduledItem 데이터를 일괄 등록합니다.'

    def add_arguments(self, parser):
        # 인자로 '파일명'을 받습니다.
        parser.add_argument('csv_filename', type=str, help='data 폴더에 위치한 CSV 파일의 이름')

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']

        # 현재 이 커맨드 파일이 있는 디렉터리 경로를 가져옵니다.
        command_dir = os.path.dirname(__file__)
        # 'data' 폴더와 입력받은 파일명을 조합하여 CSV 파일의 전체 경로를 만듭니다.
        csv_file_path = os.path.join(command_dir, 'data', csv_filename)

        # 파일 존재 여부 확인
        if not os.path.exists(csv_file_path):
            raise CommandError(f"파일을 찾을 수 없습니다: '{csv_file_path}'")

        try:
            with transaction.atomic():
                with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
                    reader = csv.DictReader(csv_file)
                    
                    created_count = 0
                    for row_num, row in enumerate(reader, 1):
                        try:
                            is_secret = row['post_is_secret'].strip().upper() == 'TRUE'
                            
                            ScheduledItem.objects.create(
                                post_name=row['post_name'],
                                post_title=row['post_title'],
                                post_is_secret=is_secret,
                                post_content=row['post_content'],
                                comment_content=row['comment_content'],
                            )
                            created_count += 1
                        except Exception as e:
                            self.stderr.write(self.style.ERROR(f'{row_num}번째 행에서 오류가 발생했습니다: {row}'))
                            self.stderr.write(self.style.ERROR(f'오류 내용: {e}'))
                            raise

        except Exception as e:
            raise CommandError(f"CSV 파일 처리 중 심각한 오류가 발생하여 모든 작업을 취소했습니다. 오류: {e}")

        self.stdout.write(self.style.SUCCESS(f"성공적으로 {created_count}개의 ScheduledItem을(를) 등록했습니다."))