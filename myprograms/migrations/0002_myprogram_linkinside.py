# Generated by Django 2.1.7 on 2019-07-17 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myprograms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprogram',
            name='linkinside',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]