from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Definition, Word, Tag

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def show_word(request, word):
    word = Word.objects.get(word_name=word)
    definition = Definition.objects.filter(word=word)

    context = {
        'word': word,
        'definitions': definition,
    }
    ##way 2###return HttpResponse(template.render(context, request))
    return render(request, 'show_word.html', context)


def show_id_word(request, num):
    #word = Word.objects.filter(id=num)
    word = get_object_or_404(Word, pk=num)
    #print(word.word_name)
    definition = Definition.objects.filter(word=word)

    context = {
        'word': word,
        'definitions': definition,
    }
    ##way 2###return HttpResponse(template.render(context, request))
    return render(request, 'show_word.html', context)


def show_tag(request, tag_name):
    tag = get_object_or_404(Tag, tag=tag_name)
    #word = get_object_or_404(Word, pk=nu)
    #print(word.word_name)
    definition = Definition.objects.filter(tags__tag=tag_name).distinct()

    context = {
        'tag': tag,
        'definitions': definition,
    }
    ##way 2###return HttpResponse(template.render(context, request))
    return render(request, 'show_tag.html', context)
