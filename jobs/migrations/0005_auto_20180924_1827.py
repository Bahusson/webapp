# Generated by Django 2.1.1 on 2018-09-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_tech'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tech',
            name='link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
