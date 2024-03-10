# Generated by Django 4.2a1 on 2023-12-30 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skin_support', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='age',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AddField(
            model_name='post',
            name='country',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='post',
            name='ddx1',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='post',
            name='ddx2',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='post',
            name='ethnicity',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='post',
            name='gender',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='post',
            name='provdx',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='post',
            name='skin_location',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
