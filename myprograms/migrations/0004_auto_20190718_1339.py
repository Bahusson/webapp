# Generated by Django 2.1.7 on 2019-07-18 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myprograms', '0003_auto_20190718_0916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myprogram',
            options={'ordering': ['-place']},
        ),
    ]
