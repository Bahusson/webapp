# Generated by Django 2.1.1 on 2018-09-15 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lotto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('readme', models.TextField()),
                ('image', models.ImageField(upload_to='images')),
                ('version', models.CharField(max_length=25)),
                ('weight', models.CharField(max_length=25)),
                ('compatible', models.CharField(max_length=200)),
                ('downlink', models.TextField()),
            ],
        ),
    ]