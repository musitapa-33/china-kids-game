from django.db import models

class QuizQuestion(models.Model):
    question = models.TextField()
    choices = models.JSONField()
    answer = models.IntegerField()
    question_type = models.CharField(max_length=20)
    province_id = models.IntegerField()

    def __str__(self):
        return self.question[:50]

class QuizResult(models.Model):
    user_id = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.score}"
