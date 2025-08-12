# notes/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ObsiNote
from .serializers import ObsiNoteSerializer
from .pagination import StandardResultsSetPagination  # 先ほど作成したクラス

class ObsiNoteViewSet(viewsets.ModelViewSet):
    queryset = ObsiNote.objects.all()
    serializer_class = ObsiNoteSerializer
    pagination_class = StandardResultsSetPagination  # ここでセット

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.GET.get('q', '').strip()
        mode = request.GET.get('mode', 'title')

        queryset = self.queryset

        if query:
            query_terms = [term.strip().lower() for term in query.split() if term.strip()]
            if mode == 'title':
                for term in query_terms:
                    queryset = queryset.filter(filename__icontains=term)
            elif mode == 'tag':
                # tagsがJSONFieldなのでfilterは難しいため、ここはPython側で絞り込み
                # querysetはQuerySetなので、一旦リスト化しちゃう方法
                notes = list(queryset)
                filtered_notes = []
                for note in notes:
                    if isinstance(note.tags, list) and all(
                        any(term in tag.lower() for tag in note.tags) for term in query_terms
                    ):
                        filtered_notes.append(note)
                queryset = filtered_notes

        # ページング処理
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # ページング不要なら通常レスポンス
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
