# Generated by Django 4.2a1 on 2023-12-30 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skin_support', '0004_alter_post_pic1_alter_post_pic2_alter_post_pic3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pic1',
            field=models.ImageField(upload_to='pics/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pic2',
            field=models.ImageField(blank=True, upload_to='pics/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pic3',
            field=models.ImageField(blank=True, upload_to='pics/'),
        ),
    ]
