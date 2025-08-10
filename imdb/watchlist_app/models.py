from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class StreamingPlatform(models.Model):
    """
    Model representing a streaming platform.
    """
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    platform = models.ForeignKey(StreamingPlatform, related_name='watchlist', on_delete=models.CASCADE, null=True, blank=True)
    release_date = models.DateField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Order by creation date, newest first
        

class Review(models.Model):
    """
    Model representing a review for a movie in the watchlist.
    """
    watchlist = models.ForeignKey(WatchList, related_name='reviews', on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.watchlist.title} - Rating: {self.rating}'