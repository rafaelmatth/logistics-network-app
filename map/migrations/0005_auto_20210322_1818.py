# Generated by Django 3.1.7 on 2021-03-22 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_auto_20210322_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logisticsnetwork',
            name='destination_city',
        ),
        migrations.RemoveField(
            model_name='logisticsnetwork',
            name='origin_city',
        ),
        migrations.AlterModelTable(
            name='logisticsnetwork',
            table='map_logistics_network',
        ),
    ]