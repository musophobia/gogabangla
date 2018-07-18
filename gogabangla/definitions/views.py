from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Definition,Word,Tag

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def showword(request, word):
    w=Word.objects.get(word_name=word)
    d=Definition.objects.filter(word=w)
    context = {
        'word': w,
        'define': d,
    }
    ##way 2###return HttpResponse(template.render(context, request))
    return render(request, 'showword.html', context)