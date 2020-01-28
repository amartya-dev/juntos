# Generated by Django 2.2.5 on 2020-01-28 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200126_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='highlightedevents',
            name='slug',
            field=models.SlugField(default='hello', max_length=250, unique_for_date='publish'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.SlugField(default='hello', max_length=250, unique_for_date='publish'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donations',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='highlightedevents',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='news',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='news',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
    ]
