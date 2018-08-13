from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm, Textarea, ModelMultipleChoiceField, ModelChoiceField
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2TagWidget
from .models import Tag, Word, Definition
from social_django.models import UserSocialAuth
from django.utils.translation import gettext_lazy as _


class DefinitionForm(forms.ModelForm):
    word=forms.CharField(required=True, label='Word', max_length=100)
    define=forms.CharField(required=True, label='define',
                           widget=Textarea(attrs={'placeholder':'write bitch', 'rows':'7','cols':'100',
                                                  'id':'def', 'class':'form-group'}),
                           max_length=800)
    sentence_ex=forms.CharField(required=True, label='Example', widget= Textarea, max_length=1000)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), label='Tags', widget=Select2TagWidget)
    synonyms= ModelMultipleChoiceField(required=False, queryset=Word.objects.all(), label='Synonyms', widget=Select2TagWidget)
    antonyms = ModelMultipleChoiceField(required=False, queryset=Word.objects.all(), label='বিপরীত শব্দ', widget=Select2TagWidget)

    class Meta:
        model = Definition
        fields = ['word', 'define', 'sentence_ex', 'tags', 'synonyms', 'antonyms']

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(DefinitionForm, self).__init__(*args, **kwargs)


    def clean_word(self):
        w= self.cleaned_data['word']
        print(w)
        try:
            wo=Word.objects.get(word_name=w)
        except Word.DoesNotExist:
            u = UserSocialAuth.objects.get(pk=1)
            Word.objects.create(word_name=w, adder=u)
            wo = Word.objects.get(word_name=w)
        return wo

    # def clean_tags(self):
    #     w=self.cleaned_data['tags']
    #     print(w)
    #     for t in w:
    #         try:
    #             wo = Tag.objects.get(tag=t)
    #         except Tag.DoesNotExist:
    #             Tag.objects.create(tag=t)
    #             wo = Tag.objects.get(word_name=w)
    #         print(wo)
    #     return wo