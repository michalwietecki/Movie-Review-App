from django.db import models

from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.conf import settings

from account.models import Account


# Create your models here.

def upload_location(instance, filename):
    file_path = '{title}/{year}-{filename}'.format(
        title=str(instance.title), year=str(instance.year), filename=filename
    )
    return file_path

class Movie(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    director = models.CharField(max_length=50, null=False, blank=False)
    movie_id = models.CharField(max_length=50, null=False, blank=True, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)


    def save(self, *args, **kwargs):
        if not self.movie_id:
            sanitized_title = self.title.replace(" ", "_")
            self.movie_id = f"{sanitized_title}_{self.year}"
            self.slug = slugify(f"{sanitized_title}_{self.year}")
        super().save(*args, **kwargs)

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum([review.rating for review in reviews])
            self.rating = total_rating / len(reviews)
        else:
            self.rating = 0.0
        self.save()

    def __str__(self):
        return f"{self.title} ({self.year})"

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    account_id = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="reviews",
        to_field="id"
    )
    movie_id = models.ForeignKey(
    'Movie',
        on_delete=models.CASCADE,
        related_name="reviews",
        to_field="movie_id")
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Ocena nie może być mniejsza niż 1."),
            MaxValueValidator(10, message="Ocena nie może być większa niż 10.")
        ],
        null=False,
        blank=False,
        help_text="Rate this movie from 1 to 10."
    )
    review_text = models.TextField(max_length=2000, blank=True, null=True, help_text="Add an optional review.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('account_id', 'movie_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.account_id.username} for {self.movie_id.title} ({self.rating}/10)"