# Generated by Django 2.1.7 on 2019-07-18 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190716_1406'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-pubdate']},
        ),
    ]
