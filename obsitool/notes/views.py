from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ObsiNote


def search_view(request):
    query = request.GET.get('q', '').strip()
    mode = request.GET.get('mode', 'title')
    results = []

    if query:
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

    # ページネーション設定
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 10)  # 1ページあたり10件表示

    try:
        paginated_results = paginator.page(page)
    except PageNotAnInteger:
        paginated_results = paginator.page(1)
    except EmptyPage:
        paginated_results = paginator.page(paginator.num_pages)

    return render(request, 'notes/search.html', {
        'results': paginated_results,
        'query': query,
        'mode': mode,
        'paginator': paginator,
    })
