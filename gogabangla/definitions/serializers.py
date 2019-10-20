from .models import Definition
from rest_framework import serializers


class definitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ('define', 'sentence_ex', 'word')

    word=serializers.SerializerMethodField('get_word_name')
    def get_word_name(self,obj):
        return obj.word.word_name