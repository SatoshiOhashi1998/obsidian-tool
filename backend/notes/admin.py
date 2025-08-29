from django.contrib import admin
from .models import ObsiNote

@admin.register(ObsiNote)
class ObsiNoteAdmin(admin.ModelAdmin):
    list_display = ('filename', 'source', 'published')   # 一覧で見たい項目
    search_fields = ('filename', 'source', 'tags')       # 検索できるフィールド
    list_filter = ('published',)                          # 絞り込みできるフィールド
