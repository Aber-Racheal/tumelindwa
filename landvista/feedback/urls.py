'''This file contains the URL routing for the Feedback app.
It maps URL patterns to view functions or classes to handle HTTP requests.
'''


from django.urls import path
from .views import QuestionListView, FeedbackListView, QuestionResponseView, AllQuestionsResponseView

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('feedbacks/', FeedbackListView.as_view(), name='feedback-list'),
    path('questions/<int:question_id>/responses/', QuestionResponseView.as_view(), name='question-response'),
    path('responses/', AllQuestionsResponseView.as_view(), name='all-questions-response'),
]
