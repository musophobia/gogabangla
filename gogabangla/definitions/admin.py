from django.contrib import admin
from .models import GogaPerson, Tag, Definition, Word

# Register your models here.
admin.site.register(GogaPerson)
admin.site.register(Tag)
admin.site.register(Definition)
admin.site.register(Word)
