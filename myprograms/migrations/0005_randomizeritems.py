# Generated by Django 2.1.7 on 2019-07-18 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myprograms', '0004_auto_20190718_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='RandomizerItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('title_pl', models.CharField(max_length=100, null=True)),
                ('title_en', models.CharField(max_length=100, null=True)),
                ('sel1', models.CharField(max_length=100)),
                ('sel1_pl', models.CharField(max_length=100, null=True)),
                ('sel1_en', models.CharField(max_length=100, null=True)),
                ('sel2', models.CharField(max_length=100)),
                ('sel3', models.CharField(max_length=100)),
                ('sel3_pl', models.CharField(max_length=100, null=True)),
                ('sel3_en', models.CharField(max_length=100, null=True)),
                ('sel4', models.CharField(max_length=100)),
                ('sel4_pl', models.CharField(max_length=100, null=True)),
                ('sel4_en', models.CharField(max_length=100, null=True)),
                ('mark_selection', models.CharField(max_length=100)),
                ('mark_selection_pl', models.CharField(max_length=100, null=True)),
                ('mark_selection_en', models.CharField(max_length=100, null=True)),
                ('start_date', models.CharField(max_length=100)),
                ('start_date_pl', models.CharField(max_length=100, null=True)),
                ('start_date_en', models.CharField(max_length=100, null=True)),
                ('mark_all', models.CharField(max_length=100)),
                ('mark_all_pl', models.CharField(max_length=100, null=True)),
                ('mark_all_en', models.CharField(max_length=100, null=True)),
                ('end_date', models.CharField(max_length=100)),
                ('end_date_pl', models.CharField(max_length=100, null=True)),
                ('end_date_en', models.CharField(max_length=100, null=True)),
                ('gen_stats', models.CharField(max_length=100)),
                ('gen_stats_pl', models.CharField(max_length=100, null=True)),
                ('gen_stats_en', models.CharField(max_length=100, null=True)),
                ('hi_low', models.CharField(max_length=100)),
                ('hi_low_pl', models.CharField(max_length=100, null=True)),
                ('hi_low_en', models.CharField(max_length=100, null=True)),
                ('no_raw', models.CharField(max_length=100)),
                ('no_raw_pl', models.CharField(max_length=100, null=True)),
                ('no_raw_en', models.CharField(max_length=100, null=True)),
                ('mode', models.CharField(max_length=100)),
                ('mode_pl', models.CharField(max_length=100, null=True)),
                ('mode_en', models.CharField(max_length=100, null=True)),
                ('count', models.CharField(max_length=100)),
                ('count_pl', models.CharField(max_length=100, null=True)),
                ('count_en', models.CharField(max_length=100, null=True)),
                ('avg', models.CharField(max_length=100)),
                ('avg_pl', models.CharField(max_length=100, null=True)),
                ('avg_en', models.CharField(max_length=100, null=True)),
                ('gen', models.CharField(max_length=100)),
                ('gen_pl', models.CharField(max_length=100, null=True)),
                ('gen_en', models.CharField(max_length=100, null=True)),
                ('chart', models.CharField(max_length=100)),
                ('chart_pl', models.CharField(max_length=100, null=True)),
                ('chart_en', models.CharField(max_length=100, null=True)),
                ('score', models.CharField(max_length=100)),
                ('score_pl', models.CharField(max_length=100, null=True)),
                ('score_en', models.CharField(max_length=100, null=True)),
                ('save_sc', models.CharField(max_length=100)),
                ('save_sc_pl', models.CharField(max_length=100, null=True)),
                ('save_sc_en', models.CharField(max_length=100, null=True)),
                ('save', models.CharField(max_length=100)),
                ('save_pl', models.CharField(max_length=100, null=True)),
                ('save_en', models.CharField(max_length=100, null=True)),
                ('your', models.CharField(max_length=100)),
                ('your_pl', models.CharField(max_length=100, null=True)),
                ('your_en', models.CharField(max_length=100, null=True)),
                ('play', models.CharField(max_length=100)),
                ('play_pl', models.CharField(max_length=100, null=True)),
                ('play_en', models.CharField(max_length=100, null=True)),
                ('nums', models.CharField(max_length=100)),
                ('nums_pl', models.CharField(max_length=100, null=True)),
                ('nums_en', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
