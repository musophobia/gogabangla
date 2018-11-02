from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm, Textarea, ModelMultipleChoiceField, ModelChoiceField, TextInput
from django import forms
from django.utils.encoding import force_text
from django_select2.forms import Select2MultipleWidget, Select2TagWidget, ModelSelect2TagWidget, Select2Widget
from select2.fields import ChoiceField

from .models import Tag, Word, Definition
from langdetect import detect
from social_django.models import UserSocialAuth
from django.utils.translation import gettext_lazy as _
import regex



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
        #print(values)
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
        return cleaned_values


class DefinitionForm(forms.ModelForm):
    word=forms.CharField(required=True, label='শব্দ', max_length=100, widget=
                        TextInput(attrs={'id':'words', 'class':'form-group form-control','placeholder':"এখানে শব্দটি লিখুন..."}))
    define=forms.CharField(required=True, label='শব্দের ব্যাখ্যা',
                           widget=Textarea(attrs={'placeholder':'শব্দের ব্যাখ্যা লিখুন...', 'rows':'2',
                                                  'id':'def', 'class':'form-group form-control'}),
                           max_length=800)
    sentence_ex=forms.CharField(required=True, label='শব্দটি সম্বলিত একটি বাক্য', widget= Textarea(attrs={'placeholder':'এখানে বাক্যটি লিখুন...',
                                                  'rows':'4',
                                                  'id':'ex', 'class':'form-group form-control'}), max_length=1000)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), label='ট্যাগসমূহ', widget=
    MyModelSelect2TagWidget(attrs={'id':'tags', 'class':'form-group form-control mb-2', 'placeholder':''}))
    synonyms= ModelMultipleChoiceField(required=False, queryset=Word.objects.all(), label='সমার্থক শব্দ', widget=
    Select2MultipleWidget(attrs={'data-placeholder': 'সমার্থক শব্দ বাছাই করুন', 'id':'syn',  'class':'form-group form-control  mb-2'}))
    antonyms = ModelMultipleChoiceField(required=False, queryset=Word.objects.all(), label='বিপরীত শব্দ', widget=
    Select2TagWidget(attrs={'data-placeholder': 'বিপরীত শব্দ বাছাই করুন', 'id':'ant',   'class':'form-group form-control '}))

    class Meta:
        model = Definition
        fields = ['word', 'define', 'sentence_ex', 'tags', 'synonyms', 'antonyms']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('user', None)
        super(DefinitionForm, self).__init__(*args, **kwargs)


    #
    def clean_word(self):
        w= self.cleaned_data['word']
        print(self.cleaned_data)
        #tas = self.cleaned_data['tags']
        #print(tas)
        #print(w)

        try:
            wo=Word.objects.get(word_name=w)
        except Word.DoesNotExist:
            isBang = True
            for c in w:
                if c != ' ':
                    if detect(c) != 'bn':
                        isBang = False

            if isBang == False:
                raise forms.ValidationError("মাঙ্গের পুলা বাংলা দে ")

            u = self.request
            Word.objects.create(word_name=w, adder=u)
            wo = Word.objects.get(word_name=w)
        return wo

    # def clean_sentence_ex(self):
    #     w = self.cleaned_data
    #     print(w)
    #     w=w.get('word')
    #     s=self.cleaned_data['sentence_ex']
    #     #print(s)
    #
    #     try:
    #         wo=Word.objects.get(word_name=w)
    #         if w not in s:
    #             raise forms.ValidationError("উদাহরণে শব্দটি দিন")
    #     except Word.DoesNotExist:
    #         return s
    #
    #
    #     return s

    def clean_sentence_ex(self):
        data = super().clean()
        #print('hui')
        s = data.get('sentence_ex')
        try:
            w=(data.get('word')).word_name
        except:
            return s
        #print('chui')


        #print(s)
        if w not in s:
            raise forms.ValidationError("উদাহরণ দিলেন যার মধ্যে শব্দই নাই। ফাইজলামি?")
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

class SearchForm(forms.Form):
    word_name=forms.CharField(required=True, label="", max_length=100, widget=
                        TextInput(attrs={'id':'words', 'class':'form-group form-control rounded','placeholder':"এখানে শব্দটি লিখুন..."}))



class UserNameForm(forms.Form):
    word_name=forms.CharField(required=True, label="ছদ্মনাম", max_length=100, widget=
                        TextInput(attrs={'id':'username', 'class':'form-group form-control   border-top-0 border-left-0 border-right-0','placeholder':"এখানে ছদ্মনামটি লিখুন..."}))

    def clean_word_name(self):
        w = self.cleaned_data['word_name']
        print(self.cleaned_data)
        try:
            user=User.objects.get(username=w)
            raise forms.ValidationError("ei naam khali nai")
        except:
            print("ldsfdosgbi")
        return w
# class SearchForm(forms.Form):
#
#
#     word_name = ModelChoiceField( queryset=Word.objects.all(), label='শব্দ', widget=
#     Select2Widget(
#         attrs={'placeholder': 'শব্দ বাছাই করুন', 'id': 'search', 'class': 'form-control'}))

    # def is_valid(self):
    #     # run whatever ModelForm validations you need
    #     return super(SearchForm, self).is_valid()

    # def clean_data(self):
    #     w= self.cleaned_data['word_name']
    #     return w