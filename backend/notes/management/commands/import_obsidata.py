import os
import re
import yaml
from datetime import datetime
from django.core.management.base import BaseCommand
from notes.models import ObsiNote

class Command(BaseCommand):
    help = 'ObsidianのMarkdownファイルを読み込んでDBに取り込む'

    def add_arguments(self, parser):
        parser.add_argument('folder', type=str, help='Obsidianリポジトリのローカルフォルダパス')

    def handle(self, *args, **options):
        folder = options['folder']
        md_files = [f for f in os.listdir(folder) if f.endswith('.md')]
        self.stdout.write(f'Found {len(md_files)} Markdown files in {folder}')

        for filename in md_files:
            path = os.path.join(folder, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # YAML front matterの抽出
            yaml_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
            if yaml_match:
                yaml_str = yaml_match.group(1)
                body = yaml_match.group(2)
                meta = yaml.safe_load(yaml_str)
            else:
                meta = {}
                body = content

            source = meta.get('source')
            published_val = meta.get('published')
            published = None

            if published_val:
                if isinstance(published_val, str):
                    try:
                        published = datetime.strptime(published_val, '%Y-%m-%d').date()
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f'Invalid date format in {filename}: {published_val}'))
                else:
                    published = published_val


            tags = meta.get('tags', [])

            # 画像URL抽出
            image_urls = re.findall(r'!\[.*?\]\((.*?)\)', body)

            # DB保存・更新
            obj, created = ObsiNote.objects.update_or_create(
                filename=filename,
                defaults={
                    'source': source,
                    'published': published,
                    'tags': tags,
                    'image_urls': image_urls,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} {filename}: {len(image_urls)} images found')

        self.stdout.write(self.style.SUCCESS('Import finished!'))
