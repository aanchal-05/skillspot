from django.db import models

from authentication.models import UserDetails
# from star_ratings.models import RatingField


class Review(models.Model):
    reviewer = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='reviews_given' ,max_length=1000,blank=True, null=True)
    user_being_reviewed = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='reviews_received')
    content = models.TextField()
    rating = models.IntegerField(default=0)

    # rating = models.IntegerField()

    # def __str__(self):
    #     return f"{self.reviewer.username} -> {self.user_being_reviewed.username}"
