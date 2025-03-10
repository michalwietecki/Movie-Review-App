from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review, Movie

@receiver(post_save, sender=Review)
def update_movie_rating(sender, instance, **kwargs):
    movie = instance.movie_id
    movie.update_rating()

@receiver(post_delete, sender=Review)
def update_movie_rating_on_delete(sender, instance, **kwargs):
    movie = instance.movie_id
    movie.update_rating()
