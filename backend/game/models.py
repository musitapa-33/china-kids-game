from django.db import models

class PuzzleProgress(models.Model):
    user_id = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    completed = models.BooleanField(default=False)
    correct_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} - {self.difficulty}"
