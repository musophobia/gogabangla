from django.contrib.auth.models import User
from django.contrib.auth.views import logout
from django.core.serializers import json
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from social_django.models import UserSocialAuth
from django.shortcuts import render, get_object_or_404, redirect
from notifications.signals import notify
from .forms import DefinitionForm, SearchForm, UpdateForm, UserNameForm
from .models import Definition, Word, Tag, Like, Dislike
import datetime
import random
from .decorators import user_is_entry_author
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import UpdateView
from .serializers import definitionSerializer
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
	searchform = SearchForm()
	latest_def = Definition.objects.all().order_by('-added_at')
	page = request.GET.get('page', 1)
	paginator = Paginator(latest_def, 20)
	try:
		latest_def = paginator.page(page)
	except PageNotAnInteger:
		latest_def = paginator.page(1)
	except EmptyPage:
		latest_def = paginator.page(paginator.num_pages)
	return render(request, 'home.html', {'searchform':searchform, 'latest_def':latest_def} )


def show_word(request, word):
    word_def =''
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        variable = request.POST.get('variable',None)
        word_def = get_object_or_404(Definition, id=slug)
        if  variable == 'likebutton':
            print(slug)
            try:
                Liked = Like.objects.get(liker=user, definition=word_def)
            except Like.DoesNotExist:
                Liked = None
            try:
                Dliked = Dislike.objects.get(dliker=user, definition=word_def)
            except Dislike.DoesNotExist:
                Dliked = None
            if Liked is not None:
                word_def.like_count-=1
                Liked.delete()
            else:
                if Dliked is not None:
                    Dliked.delete()
                    word_def.dislike_count-=1
                word_def.like_count+=1
                Like.objects.create(liker=user, definition=word_def)
                # notify.send(user, recipient=user, verb=request.user + ' liked your definition of ' + word_def.word)
            word_def.save()
            str1 = str(word_def.like_count)+","+str(word_def.dislike_count)+","+str(slug);
            return HttpResponse(str1)

        elif variable == 'dislikebutton':
            print("sldfl")
            try:
                DLiked = Dislike.objects.get(dliker=user, definition=word_def)
            except Dislike.DoesNotExist:
                DLiked = None
            try:
                liked = Like.objects.get(liker=user, definition=word_def)
            except Like.DoesNotExist:
                liked = None
            if DLiked is not None:
                word_def.dislike_count-=1
                DLiked.delete()
            else:
                if liked is not None:
                    liked.delete()
                    word_def.like_count-=1
                word_def.dislike_count+=1
                Dislike.objects.create(dliker=user, definition=word_def)
            word_def.save()
            str1 = str(word_def.like_count) + "," + str(word_def.dislike_count) + "," + str(slug);
            return HttpResponse(str1)
        else:
            return HttpResponse(10)
    word = Word.objects.get(word_name=word)
    definition = Definition.objects.filter(word=word).order_by('-like_count')
    #like dislike er jonno ei duita pathaite hobe

    #likes=Like.objects.filter(liker=request.user, definition__word_name=word)
    #dislikes = Like.objects.filter(dliker=request.user, definition__word_name=word)

    searchform = SearchForm()
    context = {
        'word': word,
        'definitions': definition,
    	#'likes':likes,
    	#'dislikes':dislikes,
        'searchform':searchform
    }

    ##way 2###return HttpResponse(template.render(context, request))
    return render(request, 'show_word.html', context)
    #return HttpResponse(json.dumps(context), content_type='application/json')


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

def show_def(request, def_id):
	word_def =''
	if request.method == 'POST':
		user = request.user
		slug = request.POST.get('slug', None)
		variable = request.POST.get('variable',None)
		word_def = get_object_or_404(Definition, id=slug)
		if  variable == 'likebutton':
			print(slug)
			try:
				Liked = Like.objects.get(liker=user, definition=word_def)
			except Like.DoesNotExist:
				Liked = None
			try:
				Dliked = Dislike.objects.get(dliker=user, definition=word_def)
			except Dislike.DoesNotExist:
				Dliked = None
			if Liked is not None:
				word_def.like_count-=1
				Liked.delete()
			else:
				if Dliked is not None:
					Dliked.delete()
					word_def.dislike_count-=1
				word_def.like_count+=1
				Like.objects.create(liker=user, definition=word_def)
                # notify.send(user, recipient=user, verb=request.user + ' liked your definition of ' + word_def.word)
			word_def.save()
			str1 = str(word_def.like_count)+","+str(word_def.dislike_count)+","+str(slug);
			return HttpResponse(str1)

		elif variable == 'dislikebutton':
			print("sldfl")
			try:
				DLiked = Dislike.objects.get(dliker=user, definition=word_def)
			except Dislike.DoesNotExist:
				DLiked = None
			try:
				liked = Like.objects.get(liker=user, definition=word_def)
			except Like.DoesNotExist:
				liked = None
			if DLiked is not None:
				word_def.dislike_count-=1
				DLiked.delete()
			else:
				if liked is not None:
					liked.delete()
					word_def.like_count-=1
				word_def.dislike_count+=1
				Dislike.objects.create(dliker=user, definition=word_def)
			word_def.save()
			str1 = str(word_def.like_count) + "," + str(word_def.dislike_count) + "," + str(slug);
			return HttpResponse(str1)
		else:
			return HttpResponse(10)
    
	word_def = get_object_or_404(Definition, id=def_id)
	searchform = SearchForm()
	context = {
    	'def':word_def,
    	'searchform':searchform,
    }
	return render(request, 'show_def.html', context)

def show_tag(request, tag_name):
    tag = get_object_or_404(Tag, tag=tag_name)
    #word = get_object_or_404(Word, pk=nu)
    #print(word.word_name)
    definition = Definition.objects.filter(tags__tag=tag_name).order_by('-added_at')
    searchform=SearchForm()
    context = {
        'tag': tag,
        'definitions': definition,
        'searchform':searchform,
    }
    ##way 2###return HttpResponse(template.render(context, request))
    return render(request, 'show_tag.html', context)

def lettersearch(request, let):
    #print(word.word_name)
    words = Word.objects.filter(word_name__startswith=let).order_by('-added_at')
    fh=Word.objects.filter(word_name__startswith=let).count()
    searchform=SearchForm()
    context = {
        'word':words,
        'ew':fh,
        'ter':let,
        'searchform':searchform,
    }
    ##way 2###return HttpResponse(template.render(context, request))
    return render(request, 'letter_search.html', context)

@login_required
def add_word(request):
    if request.method == "POST":
        form = DefinitionForm(request.POST, user=request.user)
        if form.is_valid():
            model_instance=form.save(commit=False)
            model_instance.word=Word.objects.get(word_name=form.cleaned_data['word'])
            model_instance.adder= request.user
            model_instance.save()
            form.save_m2m()
            word=get_object_or_404(Word, word_name=model_instance.word)
            definition = Definition.objects.filter(word=word)
            searchform = SearchForm()
            context = {
                'word': word,
                'definitions': definition,
                'searchform': searchform
            }
            return redirect('/')
       # print(form.cleaned_data)
    else:
        form = DefinitionForm(user=request.user)

    searchform = SearchForm()
    return render(request, "addword.html", {'form': form, 'searchform':searchform})

def auto_complete(request):
    if request.method=="POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_word = form.cleaned_data['word_name']
            print(search_word)
            wo = Word.objects.filter(word_name__icontains=search_word)
            print(wo)
            searchform = SearchForm()
            context = {
            	'search_word':search_word,
                'word': wo,
                'searchform': searchform
            }
            return render(request, 'search_page.html', context)
    return render(request, 'search_page.html')



class updateview(UpdateView):
   # def get_queryset(self):
   #     base_qs = super(UpdateForm, self).get_queryset()
   #     return base_qs.filter(user=self.request.user)
    model=Definition
    #fields = ['define', 'sentence_ex', 'tags', 'synonyms', 'antonyms']
    form_class = UpdateForm
    template_name='addword.html'
    template_name_field = ['define', 'sentence_ex', 'tags', 'synonyms', 'antonyms']

def search_page(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['word_name']
            word = Word.objects.get(word_name=name).order_by('-like_count')
            definition = Definition.objects.filter(word=word)
            searchform = SearchForm()
            context = {
                'word': word,
                'definitions': definition,
                'searchform' : searchform
            }
            return render(request, 'show_word.html', context)
    searchform=SearchForm()
    return render(request, 'search.html', {'searchform':searchform} )


def profile(request, name):
    user=get_object_or_404(User, username=name)
    print(user)
    defins = Definition.objects.filter(adder_id__pk=user.id).order_by('-added_at')
    print(defins)
    def_count =  Definition.objects.filter(adder_id__pk=user.id).count
    word_count= Word.objects.filter(adder__pk=user.id).count
    print(word_count)
    searchform = SearchForm()
    return render(request, 'profile_page.html', {'defon':defins,'user':user, 'dc':def_count, 'wc':word_count, 'searchform': searchform})


# @login_required
# def username_set(request):
#     form=UserNameForm()
#     if request.method=="POST":
#         form=UserNameForm(request.POST)
#         if form.is_valid():
#             user=get_object_or_404(User, pk=request.user.id)
#             usename=form.cleaned_data['username']
#             user.username=usename
#             user.save()
#             return redirect('/')
#     return render(request,'username_set.html', {'UserNameForm':form})


@login_required
def username_set(request):
	if request.method=="POST":
		form=UserNameForm(request.POST)
		if form.is_valid():
			usename=form.cleaned_data['username']
			user=get_object_or_404(User, pk=request.user.id)
			try:
				newuser=User.objects.get(username=usename)
				errorMessage="এই ছদ্মনামটি ইতিমধ্যে ব্যবহার করা হয়ে গেছে। নতুন ছদ্মনাম দিন।"
				form=UserNameForm()
				searchform=SearchForm()
				return render(request,'username_set.html', {'UserNameForm':form, 'searchform':searchform, 'errorMessage':errorMessage})

			except User.DoesNotExist:
				user.username=usename
				user.save()
				return redirect('/')
				
	form=UserNameForm()
	searchform=SearchForm()
	return render(request,'username_set.html', {'UserNameForm':form, 'searchform':searchform})


@login_required
def logout(request):
    logout(request)
    searchform = SearchForm()
    return render(request, 'home.html', {'searchform': searchform})

@login_required
def ulgin(request):
	curr=datetime.datetime.now() - datetime.timedelta(seconds=30)
	user=get_object_or_404(User, pk=request.user.id)
	date_join = user.date_joined
	last_login = user.last_login

	start_time = date_join.utcnow()
	end_time = last_login.utcnow()

	#date_joined = datetime.combine(user.date_joined.date(), time(user.date_joined.hour, user.date_joined.minute))
	#last_login = datetime.combine(user.last_login.date(), time(user.last_login.hour, user.last_login.minute))
	if user.last_login - user.date_joined <= datetime.timedelta(seconds=1):
	#if start_time == end_time:	
		form=UserNameForm()
		if request.method=="POST":
			form=UserNameForm(request.POST)
			if form.is_valid():
				user=get_object_or_404(User, pk=request.user.id)
				usename=form.cleaned_data['word_name']
				user.username=usename
				user.save()
				return redirect('/')
		return render(request,'username_set.html', {'UserNameForm':form})
	else:
		searchform = SearchForm()
		latest_def = Definition.objects.all().order_by('-added_at')[:25:1]
		return render(request, 'home.html', {'searchform':searchform, 'latest_def':latest_def} )
		#return render(request, 'home.html')
	

class DefinitionViewSet(APIView):
    def get(self, request):
        count=Definition.objects.all().count()
        rand=random.randint(28,count)
        queryset = Definition.objects.get(pk=rand)
        serializer = definitionSerializer(queryset)
        serializer_context = {
            'request': request,
        }
        return Response(definitionSerializer(queryset, context=serializer_context).data)