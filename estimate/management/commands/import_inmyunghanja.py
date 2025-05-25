import csv
from django.core.management.base import BaseCommand
from estimate.models import InmyungHanja

class Command(BaseCommand):
    help = 'CSV 파일을 InmyungHanja 테이블에 임포트합니다.'

    def handle(self, *args, **options):
        file_path = 'estimate/data/inmyunghanja.csv'  # 경로에 맞게 수정하세요

        # 기존 데이터 삭제 (원하지 않으면 주석처리)
        InmyungHanja.objects.all().delete()

        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            objs = []
            for row in reader:
                disused_val = row['disused'].strip().upper()
                disused_bool = True if disused_val == 'TRUE' else False

                obj = InmyungHanja(
                    num=int(row['num']),
                    pron=row['pron'],
                    char=row['char'],
                    main_mean=row['main_mean'],
                    tot_stk=int(row['tot_stk']),
                    main_elem=row['main_elem'],
                    disused=disused_bool,
                    rad_stk=int(row['rad_stk']),
                    rad=row['rad'],
                    rad_elem=row['rad_elem'],
                    detail_mean=row['detail_mean'],
                    meaning=row['meaning'],
                    stk_info=row['stk_info'],
                    rad_id=int(row['rad_id']),
                    no_rad_stk=int(row['no_rad_stk']),
                    rad_mean=row['rad_mean'],
                )
                objs.append(obj)

            InmyungHanja.objects.bulk_create(objs)
            self.stdout.write(self.style.SUCCESS(f'총 {len(objs)}개의 데이터를 성공적으로 삽입했습니다.'))
