# Generated by Django 3.1.7 on 2021-02-25 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0003_auto_20210225_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlalgorithmstatus',
            name='status',
            field=models.CharField(max_length=128),
        ),
    ]