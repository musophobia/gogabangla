from .models import Word


def today_word(request):
    today=Word.objects.get(id=12)
    return {'today_word': today}
