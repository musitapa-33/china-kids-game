from django.db import models

class UserScore(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    score = models.IntegerField(default=0)
    visited_provinces = models.JSONField(default=list)
    badges = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} - {self.score}"
