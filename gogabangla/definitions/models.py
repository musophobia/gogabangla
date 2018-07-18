from django.db import models


# Create your models here.


class GogaPerson(models.Model):
    provider = models.CharField(max_length=1000)
    user_id = models.CharField(max_length=1000)
    user_name = models.CharField(max_length=1000)
    user_email = models.CharField(max_length=1000)
    #avatar = models.ImageField(null=True)
    #Balance = models.FloatField(default=0)

    # Gender = models.CharField(max_length=10, null=True)
    # Date_of_birth = models.DateField(null=True)

    class Meta:
        db_table = 'ProfileMod'

    def __str__(self):
        return str(self.Name)


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    class Meta:
        db_table = "tag_table"

    def __str__(self):
        return self.tag


class Word(models.Model):
    #adder_id = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    word_name = models.CharField(max_length=100)
    synonym = models.ManyToManyField("self")
    antonym = models.ManyToManyField("self")

    class Meta:
        db_table = "word_table"

    def __str__(self):
        return self.word_name


class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    #adder_id = models.CharField(max_length=100)
    define = models.CharField(max_length=300)
    sentence_ex = models.CharField(max_length=1000)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField
    tags = models.ManyToManyField(Tag)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = "definition"

    def __str__(self):
        return self.defs
