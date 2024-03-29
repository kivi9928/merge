# Generated by Django 3.2.16 on 2022-12-13 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password1',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
