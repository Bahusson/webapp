# Generated by Django 2.1.1 on 2018-09-23 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_job_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tech',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images')),
                ('body', models.TextField()),
                ('link', models.CharField(blank=True, max_length=500)),
            ],
        ),
    ]
