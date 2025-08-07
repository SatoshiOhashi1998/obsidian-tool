from django.shortcuts import render
from .models import ObsiNote

def search_view(request):
    query = request.GET.get('q', '').strip()
    mode = request.GET.get('mode', 'title')
    results = []

    if query:
        if mode == 'title':
            results = ObsiNote.objects.filter(filename__icontains=query)
        elif mode == 'tag':
            # DBから全部取得 → Pythonで完全一致フィルタ
            all_notes = ObsiNote.objects.all()
            results = [note for note in all_notes if query in note.tags]

    return render(request, 'notes/search.html', {
        'results': results,
        'query': query,
        'mode': mode,
    })
