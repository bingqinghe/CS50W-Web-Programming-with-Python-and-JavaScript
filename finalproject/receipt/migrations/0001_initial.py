# Generated by Django 3.0.8 on 2020-09-15 02:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import receipt.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Ex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ImageField(default='default.jpg', upload_to=receipt.models.get_profile_path)),
                ('following', models.ManyToManyField(related_name='followers', to='receipt.User_Ex')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=receipt.models.get_post_path)),
                ('title', models.TextField()),
                ('preview', models.TextField()),
                ('receipt', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to='receipt.User_Ex')),
                ('comments', models.ManyToManyField(related_name='commented_posts', to='receipt.Comment')),
                ('likes', models.ManyToManyField(related_name='liked_posts', to='receipt.User_Ex')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='receipt.User_Ex'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='receipt.Post'),
        ),
    ]
