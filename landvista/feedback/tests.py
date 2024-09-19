'''
This file contains unit tests for the feedback API endpoints.
The tests check the API endpoints for handling Questions and Feedback submissions.

In this file:
- The `QuestionViewSetTest` class tests the creation and listing of questions.
- The `FeedbackViewSetTest` class tests the submission of feedback.
- The `QuestionResponseViewTest` class tests retrieving response counts for specific questions.
'''

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Question, Feedback

class QuestionViewSetTest(APITestCase):
    def setUp(self):
        self.question = Question.objects.create(id=1, text="Is this a test?")

    def test_create_question(self):
        url = reverse('question-list')
        data = {'id': 2, 'text': 'Is this another test?'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_create_question_with_existing_id(self):
        url = reverse('question-list')
        data = {'id': 1, 'text': 'Is this a duplicate test?'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_questions(self):
        url = reverse('question-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class FeedbackViewSetTest(APITestCase):
    def setUp(self):
        self.question = Question.objects.create(id=1, text="Is this a test?")

    def test_submit_feedback(self):
        url = reverse('feedback-list')
        data = {'feedbacks': [{'question_text': 'Is this a test?', 'response': 'yes'}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feedback.objects.count(), 1)

    def test_feedback_with_invalid_question(self):
        url = reverse('feedback-list')
        data = {'feedbacks': [{'question_text': 'Non-existent question?', 'response': 'yes'}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class QuestionResponseViewTest(APITestCase):
    def setUp(self):
        self.question = Question.objects.create(id=1, text="Is this a test?")
        Feedback.objects.create(question=self.question, response='yes')
        Feedback.objects.create(question=self.question, response='no')

    def test_get_question_response(self):
        url = reverse('question-response', args=[self.question.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['positive'], 1)
        self.assertEqual(response.data['negative'], 1)

    def test_get_non_existent_question_response(self):
        url = reverse('question-response', args=[999])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
