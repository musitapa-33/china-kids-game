from django.contrib import admin
from .models import Region, Province, QuizQuestion


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'capital', 'abbr', 'region', 'visited_count']
    list_filter = ['region']
    search_fields = ['name', 'capital', 'abbr']
    list_editable = ['visited_count']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'province', 'question_type', 'question_text']
    list_filter = ['question_type', 'province']
    search_fields = ['question_text']
