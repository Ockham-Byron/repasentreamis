# Generated by Django 5.0.1 on 2024-02-01 10:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0002_initial'),
        ('recettes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='menu',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='groups.customgroup'),
        ),
        migrations.AddField(
            model_name='anecdote',
            name='menu',
            field=models.ManyToManyField(blank=True, related_name='anecdotes', to='recettes.menu'),
        ),
        migrations.AddField(
            model_name='music',
            name='menu',
            field=models.ManyToManyField(blank=True, related_name='musics', to='recettes.menu'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='chef',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='groups.customgroup'),
        ),
        migrations.AddField(
            model_name='menu',
            name='recipes',
            field=models.ManyToManyField(blank=True, related_name='menus', to='recettes.recipe'),
        ),
        migrations.AddField(
            model_name='comment',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_comments', to='recettes.recipe'),
        ),
    ]
