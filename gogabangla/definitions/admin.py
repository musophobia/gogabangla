from django.contrib import admin
from .models import GogaPerson, Tag, Definition, Word, Like, Dislike

# Register your models here.
admin.site.register(GogaPerson)
admin.site.register(Tag)
admin.site.register(Definition)
admin.site.register(Word)
admin.site.register(Like)
admin.site.register(Dislike)
