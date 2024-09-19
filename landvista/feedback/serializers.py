'''
This file contains serializers for the Question and Feedback models.
Serializers are used to convert complex data types, such as Django models, into native Python data types that can then be easily rendered into JSON or other content types.

The serializers also handle validation and transformation of incoming data.

This file:
   Sets up logging
   Has a Write-only field for the text of the question
   Has a Read-only field for the related question object
'''

from rest_framework import serializers
from .models import Question, Feedback

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text']

class FeedbackSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(write_only=True)
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'question', 'question_text', 'response']

    def validate(self, data):
        question_text = data.get('question_text')
        if not Question.objects.filter(text=question_text).exists():
            raise serializers.ValidationError({"question_text": "Question with this text does not exist"})
        return data

    def create(self, validated_data):
        question_text = validated_data.pop('question_text')
        question = Question.objects.get(text=question_text)
        validated_data['question'] = question
        return super().create(validated_data)