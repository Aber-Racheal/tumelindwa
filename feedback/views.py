'''
This file contains the API views for handling requests related to Questions and Feedback.
Each view is responsible for processing HTTP requests, interacting with the database, and returning appropriate responses.

The views handle CRUD operations for Questions and Feedback and aggregate feedback data.
Save the new question
Validate that the provided ID does not already exist

this file:
    sets up logging
    Has function to handle listing and creating Questions.
    Has function to retrieve a list of all questions.
    Has function to create a new question if the provided ID does not already exist.
    Has function to submit a list of feedbacks.
    Has function to get feedback response counts for a specific question.
'''

from rest_framework import views, status
from rest_framework.response import Response
from .models import Question, Feedback
from .serializers import QuestionSerializer, FeedbackSerializer


class QuestionListView(views.APIView):
    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question_id = serializer.validated_data.get('id')
            if Question.objects.filter(id=question_id).exists():
                return Response({'error': 'Question with this ID already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackListView(views.APIView):
    def post(self, request, format=None):
        feedback_list = request.data.get('feedbacks', [])
        
        if not isinstance(feedback_list, list):
            return Response({'error': 'Invalid data format, expect              ed a list under the key "feedbacks"'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FeedbackSerializer(data=feedback_list, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Feedback submitted'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class QuestionResponseView(views.APIView):
    def get(self, request, question_id, format=None):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        positive = Feedback.objects.filter(question=question, response='yes').count()
        negative = Feedback.objects.filter(question=question, response='no').count()
        response_counts = {
            'question_id': question.id,
            'question_text': question.text,
            'positive': positive,
            'negative': negative
        }
        return Response(response_counts, status=status.HTTP_200_OK)

class AllQuestionsResponseView(views.APIView):
    def get(self, request, format=None):
        questions = Question.objects.all()
        response_counts = {}
        for question in questions:
            positive = Feedback.objects.filter(question=question, response='yes').count()
            negative = Feedback.objects.filter(question=question, response='no').count()
            response_counts[question.id] = {
                'question': question.text,
                'positive': positive,
                'negative': negative
            }
        return Response(response_counts, status=status.HTTP_200_OK)
