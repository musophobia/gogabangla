from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm, Textarea, ModelMultipleChoiceField, ModelChoiceField
from django import forms
from django.utils.encoding import force_text
from django_select2.forms import Select2MultipleWidget, Select2TagWidget, ModelSelect2TagWidget
from .models import Tag, Word, Definition
from social_django.models import UserSocialAuth
from django.utils.translation import gettext_lazy as _


class MyModelSelect2TagWidget(ModelSelect2TagWidget):
    queryset = Tag.objects.all()
    search_fields = ['tag__icontains']

    # def build_attrs(self):
    #     self.attrs.setdefault('data-token-separators', [])
    #     self.attrs.setdefault('data-width', '500px')
    #     self.attrs.setdefault('data-tags', 'true')
    #     return super().build_attrs(self)

    def value_from_datadict(self,data,files,name):
        values=super().value_from_datadict(data,files,name)
        print(values)
        # qs = self.queryset.filter(**{'pk__in': list(values)})
        # pks = set(str(getattr(o, pk)) for o in qs)
        queryset = self.get_queryset()
#        pks = queryset.filter(**{'pk__in': list(values)}).values_list('pk', flat=True)
        cleaned_values = []
        for val in values:
            if type(val)!=int:
                val = queryset.create(tag=val).pk
                #Tag.objects.create(tag=val)
            cleaned_values.append(val)
        # for val in values:
        #     if str(val) not in pks:
        #         val = queryset.create(tag=val).pk
        #         t=Tag.objects.get_or_create(tag=val)
        #         p=t.pk
        #         print(t)
        #         cleaned_values.append(p)
        #     else:
        #         cleaned_values.append(val)
        return cleaned_values


class DefinitionForm(forms.ModelForm):
    word=forms.CharField(required=True, label='Word', max_length=100)
    define=forms.CharField(required=True, label='define',
                           widget=Textarea(attrs={'placeholder':'write bitch', 'rows':'2','cols':'100',
                                                  'id':'def', 'class':'form-group'}),
                           max_length=800)
    sentence_ex=forms.CharField(required=True, label='Example', widget= Textarea(attrs={'placeholder':'write bitch',
                                                  'rows':'4','cols':'100',
                                                  'id':'ex', 'class':'form-group'}), max_length=1000)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), label='Tags', widget=
    MyModelSelect2TagWidget)
    synonyms= ModelMultipleChoiceField(required=False, queryset=Word.objects.all(), label='Synonyms', widget=
    Select2MultipleWidget(attrs={'data-placeholder': 'Please choose synonyms', 'id':'syn'}))
    antonyms = ModelMultipleChoiceField(required=False, queryset=Word.objects.all(), label='বিপরীত শব্দ', widget=
    Select2TagWidget(attrs={'data-placeholder': 'Please choose antonyms', 'id':'ant'}))

    class Meta:
        model = Definition
        fields = ['word', 'define', 'sentence_ex', 'tags', 'synonyms', 'antonyms']

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(DefinitionForm, self).__init__(*args, **kwargs)

    def clean_word(self):
        w= self.cleaned_data['word']
        #tas = self.cleaned_data['tags']
        #print(tas)
        #print(w)
        try:
            wo=Word.objects.get(word_name=w)
        except Word.DoesNotExist:
            u = UserSocialAuth.objects.get(pk=1)
            Word.objects.create(word_name=w, adder=u)
            wo = Word.objects.get(word_name=w)
        return wo

    def clean_sentence_ex(self):
        word = self.cleaned_data['word']
        w=word.word_name
        s=self.cleaned_data['sentence_ex']
        #print(s)
        if w not in s:
            raise forms.ValidationError("udahorone shobdo din")
        return s

    # def clean_tags(self):
    #     w=self.cleaned_data['tags']
    #     print(w)
    #     for t in w:
    #         try:
    #             t1=t.tag
    #             print(t1)
    #             wo = Tag.objects.get(tag=t1)
    #         except Tag.DoesNotExist:
    #             Tag.objects.create(tag=t1)
    #             wo = Tag.objects.get(tag=t1)
    #         print(wo)
    #     return w
