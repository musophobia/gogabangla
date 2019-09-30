from .models import Word,Tag
from django.contrib.auth.models import User
import random
from datetime import date, timedelta
from django.utils import timezone
import random

def today_word(request):
	#some_day_last_week = timezone.now().date() - timedelta(days=2)
	#today=Word.objects.filter(added_at__ = some_day_last_week).order_by('added_at')[0]
	# counter=Word.objects.all().count()
	# Day = int(datetime.now().day)
	# Month = int(datetime.now().month)
	# Year = int(datetime.now().year)
	# rand=(Year+Month*2+Day*3)
	# random=rand%counter
	today_word=Word.objects.all().order_by('-added_at')[:100]
	today=random.choice(today_word)
	# tags=Tag.objects.all()[:10]
	tags=Tag.objects.all()
	#except Word.DoesNotExist:
		#user= User.objects.get(id=1)
		#today = Word.objects.create(adder=user, word_name='বাঁকাডেমি')
	return {'today_word': today,'tags':tags}