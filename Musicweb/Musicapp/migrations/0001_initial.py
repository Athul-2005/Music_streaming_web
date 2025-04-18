# Generated by Django 5.1.4 on 2025-04-04 13:16

import Musicapp.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Songs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=50)),
                ('mimage', models.ImageField(default='media/images/default.jpg', upload_to='media/images/')),
                ('sgenre', models.CharField(max_length=50)),
                ('Artist', models.CharField(max_length=50)),
                ('audio', models.FileField(default='Media/audiofiles/default.mp3', upload_to='audiofiles')),
                ('playedbefore', models.BooleanField(default=False)),
                ('play_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='popularsongs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('popularity_score', models.IntegerField(default=0)),
                ('added_date', models.DateField(auto_now_add=True)),
                ('sname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musicapp.songs')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(default=Musicapp.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('songs', models.ManyToManyField(to='Musicapp.songs')),
            ],
        ),
    ]
