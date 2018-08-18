# Generated by Django 2.0.7 on 2018-07-20 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='antonyms',
            field=models.ManyToManyField(blank=True, null=True, related_name='antonyms', to='definitions.Word'),
        ),
        migrations.AlterField(
            model_name='definition',
            name='synonyms',
            field=models.ManyToManyField(blank=True, null=True, related_name='synonyms', to='definitions.Word'),
        ),
        migrations.AlterField(
            model_name='definition',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='definitions.Tag'),
        ),
    ]