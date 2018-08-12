from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm, Textarea, ModelMultipleChoiceField, ModelChoiceField
from django import forms
from django_select2.forms import Select2MultipleWidget
from .models import Tag, Word, Definition
from social_django.models import UserSocialAuth
from django.utils.translation import gettext_lazy as _


class DefinitionForm(forms.ModelForm):
    word=forms.CharField(required=True, label='Word', max_length=100)
    define=forms.CharField(required=True, label='define', max_length=800)
    sentence_ex=forms.CharField(required=True, label='Example', max_length=1000)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(),  widget=Select2MultipleWidget)
    synonyms= ModelChoiceField(required=False, queryset=Word.objects.all(),  widget=Select2MultipleWidget)
    antonyms = ModelChoiceField(required=False, queryset=Word.objects.all(), widget=Select2MultipleWidget)

    class Meta:
        model = Definition
        fields = ['word', 'define', 'sentence_ex', 'tags', 'synonyms', 'antonyms']

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(DefinitionForm, self).__init__(*args, **kwargs)


    def clean_word(self):
        w= self.cleaned_data['word']
        print(w)
        u = UserSocialAuth.objects.get(pk=1)
        try:
            wo=Word.objects.get(word_name=w)
        except Word.DoesNotExist:
            u = UserSocialAuth.objects.get(pk=1)
            Word.objects.create(word_name=w, adder=u)
            wo = Word.objects.get(word_name=w)
        return wo
