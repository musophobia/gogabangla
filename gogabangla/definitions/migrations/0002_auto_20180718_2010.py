# Generated by Django 2.0.7 on 2018-07-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='word_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
