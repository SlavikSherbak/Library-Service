from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    HARD = "HA"
    SOFT = "SO"
    COVER_CHOICES = [
        (HARD, "Hard"),
        (SOFT, "Soft"),
    ]
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=2,
        choices=COVER_CHOICES,
        default=SOFT,
    )
    inventory = models.IntegerField(validators=MinValueValidator(1))
    daily_fee = models.FloatField()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} (authors: {self.author})"
