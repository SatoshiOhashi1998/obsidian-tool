from django.shortcuts import render
from .models import ObsiNote

def search_view(request):
    query = request.GET.get('q', '').strip()
    mode = request.GET.get('mode', 'title')
    results = []

    if query:
        # 入力を空白区切りで複数ワードに分割（大文字小文字無視）
        query_terms = [term.strip().lower() for term in query.split() if term.strip()]

        if mode == 'title':
            results = ObsiNote.objects.all()
            for term in query_terms:
                results = results.filter(filename__icontains=term)

        elif mode == 'tag':
            results = [
                note for note in ObsiNote.objects.all()
                if isinstance(note.tags, list) and all(
                    any(term in tag.lower() for tag in note.tags)
                    for term in query_terms
                )
            ]

    return render(request, 'notes/search.html', {
        'results': results,
        'query': query,
        'mode': mode,
    })
