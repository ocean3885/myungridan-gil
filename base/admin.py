from django.contrib import admin
from .models import Profile, CustomBoard, CustomComment, ScheduledItem


# CustomComment 모델을 CustomBoard와 함께 표시하려면 Inline 클래스를 정의합니다.
class CustomCommentInline(admin.TabularInline):  
    model = CustomComment
    extra = 1  

class CustomBoardAdmin(admin.ModelAdmin):
    inlines = [CustomCommentInline]  # CustomBoard 내에서 CustomComment를 표시
    
class ScheduledItemAdmin(admin.ModelAdmin):
    """ScheduledItem 모델을 위한 관리자 페이지 설정"""

    # 2. 목록 페이지에 보여줄 필드들을 지정합니다.
    list_display = ('post_name', 'post_title', 'post_is_secret', 'status')

# 모델을 등록합니다.
admin.site.register(Profile)
admin.site.register(CustomBoard, CustomBoardAdmin)
admin.site.register(ScheduledItem, ScheduledItemAdmin)
