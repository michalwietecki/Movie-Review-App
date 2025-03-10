# Generated by Django 4.2.16 on 2025-01-19 11:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_id',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(help_text='Rate this movie from 1 to 10.', validators=[django.core.validators.MinValueValidator(1, message='Ocena nie może być mniejsza niż 1.'), django.core.validators.MaxValueValidator(10, message='Ocena nie może być większa niż 10.')])),
                ('review_text', models.TextField(blank=True, help_text='Add an optional review.', max_length=2000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.movie')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('account_id', 'movie_id')},
            },
        ),
    ]
