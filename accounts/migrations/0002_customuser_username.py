# Generated by Django 4.1.7 on 2023-03-21 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='emilioeiji', max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
