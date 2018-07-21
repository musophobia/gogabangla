from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm, Textarea
from .models import Definition


class DefinitionForm(ModelForm):
    class Meta:
        model = Definition
        fields = ['word', 'define', 'sentence_ex', 'tags', 'synonyms', 'antonyms']

        widgets = {
            'word': Textarea(attrs={'cols':10, 'rows': 1}),
        }

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }