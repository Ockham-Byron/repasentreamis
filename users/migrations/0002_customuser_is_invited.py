# Generated by Django 5.0.1 on 2024-02-26 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_invited',
            field=models.BooleanField(default=False),
        ),
    ]