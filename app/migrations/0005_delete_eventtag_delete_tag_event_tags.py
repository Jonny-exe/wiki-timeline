# Generated by Django 4.0.4 on 2022-05-19 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_eventtag_tag'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventTag',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.CharField(default='', max_length=800),
            preserve_default=False,
        ),
    ]
