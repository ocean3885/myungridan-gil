from django.contrib import admin
from .models import Submit, Person

class PersonInline(admin.StackedInline):
    model = Person

class SubmitAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'adress', 'phone', 
                    'created', 'process')
    inlines = (
        PersonInline,
    )

admin.site.register(Submit, SubmitAdmin)




