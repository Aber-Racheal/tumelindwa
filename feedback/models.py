'''This file contains the Django models for the Feedback application.
Models define the structure of the database tables and provide methods for interacting with the data.

In this file:
- The `Question` model represents a question that users can provide feedback on.
- The `Feedback` model represents feedback responses given to questions.
'''

from django.db import models
class Question(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text

class Feedback(models.Model):
    question = models.ForeignKey(Question, related_name='feedback', on_delete=models.CASCADE)
    response = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')])

    def __str__(self):
        return f"{self.question.text} - {self.response}"
