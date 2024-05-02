from django.db import migrations

def create_profile_for_existing_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')  # Django의 기본 User 모델 사용 시
    Profile = apps.get_model('base', 'Profile')
    for user in User.objects.all():
        # Profile이 존재하지 않는 경우에만 새로 생성
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_profile_bgimg'),
    ]

    operations = [
        migrations.RunPython(create_profile_for_existing_users),
    ]