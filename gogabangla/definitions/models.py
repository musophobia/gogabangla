from django.db import models

# Create your models here.
from social_django.models import UserSocialAuth


class GogaPerson(models.Model):
    provider = models.CharField(max_length=1000)
    user_id = models.CharField(max_length=1000)
    user_name = models.CharField(max_length=1000)
    user_email = models.CharField(max_length=1000)
    gender = models.CharField(max_length=10, null=True)

    # avatar = models.ImageField(null=True)
    # Balance = models.FloatField(default=0)

    # gender = models.CharField(max_length=10, null=True)
    # Date_of_birth = models.DateField(null=True)
    def __str__(self):
        return str(self.user_name)


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return str(self.tag)


class Word(models.Model):
    # adder_id = models.CharField(max_length=100)
    adder = models.ForeignKey(UserSocialAuth, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    word_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.word_name)


class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    adder = models.ForeignKey(UserSocialAuth, on_delete=models.CASCADE)
    synonyms = models.ManyToManyField(Word, related_name='synonyms')
    antonyms = models.ManyToManyField(Word, related_name='antonyms')
    define = models.CharField(max_length=300)
    sentence_ex = models.CharField(max_length=1000)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField
    tags = models.ManyToManyField(Tag)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.define)


class Like(models.Model):
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE)
    liker = models.ForeignKey(UserSocialAuth, on_delete=models.CASCADE)


class Dislike(models.Model):
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE)
    dliker = models.ForeignKey(UserSocialAuth, on_delete=models.CASCADE)
