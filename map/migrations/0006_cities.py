# Generated by Django 3.1.7 on 2021-03-22 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_auto_20210322_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Citie Name')),
            ],
            options={
                'verbose_name': 'Citie',
                'verbose_name_plural': 'Cities',
                'db_table': 'map_cities',
            },
        ),
    ]