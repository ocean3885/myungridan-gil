from django.contrib import admin
from .models import Profile, CustomBoard, CustomComment, ScheduledItem


# CustomComment 모델을 CustomBoard와 함께 표시하려면 Inline 클래스를 정의합니다.
class CustomCommentInline(admin.TabularInline):  
    model = CustomComment
    extra = 1  

class CustomBoardAdmin(admin.ModelAdmin):
    inlines = [CustomCommentInline]  # CustomBoard 내에서 CustomComment를 표시

# 모델을 등록합니다.
admin.site.register(Profile)
admin.site.register(CustomBoard, CustomBoardAdmin)
admin.site.register(ScheduledItem)
