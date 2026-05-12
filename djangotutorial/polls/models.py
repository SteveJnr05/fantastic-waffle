from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choice')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Grade(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="grade")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="grade")
    grade = models.CharField(max_length=3)

    def __str__(self):
        return self.grade

class Difficulty(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='difficulty')
    difficulty = models.PositiveIntegerField(validators=
                                             [MinValueValidator(1), MaxValueValidator(5)])
    
    def __str__(self):
        return f"{self.difficulty}"