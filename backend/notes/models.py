from django.db import models

class ObsiNote(models.Model):
    filename = models.CharField(max_length=255, unique=True)
    source = models.URLField(blank=True, null=True)
    published = models.DateField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)  # タグはリストで保存
    image_urls = models.JSONField(blank=True, null=True)  # 画像URLリスト
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
