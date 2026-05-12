from django.contrib import admin
from .models import Question, Choice, Grade, Difficulty

admin.site.site_header = "Polling App"
admin.site.site_title = "My custom index"
admin.site.index_title = "My index"

# Register your models here.
# admin.site.register(Question)
# admin.site.register(Choice)
# admin.site.register(Grade)
# admin.site.register(Difficulty)

@admin.register(Question)
class QCAdmin(admin.ModelAdmin):
    exclude = ["pub_date"]
    ordering = ["id"]

@admin.register(Choice)
class QCAdmin(admin.ModelAdmin):
    fields = ["choice_text"]

@admin.register(Grade)
class QCAdmin(admin.ModelAdmin):
    pass

@admin.register(Difficulty)
class QCAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Question, QCAdmin)
# admin.site.register(Choice, QCAdmin)
# admin.site.register(Grade, QCAdmin)
# admin.site.register(Difficulty, QCAdmin)