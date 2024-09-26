from rest_framework import serializers
from .models import Question, Feedback

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text']

class FeedbackSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(write_only=True)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)  # Updated to allow setting question directly

    class Meta:
        model = Feedback
        fields = ['id', 'question', 'question_text', 'response']

    def validate(self, data):
        question_text = data.get('question_text')
        
        # Ensure the question exists based on question_text
        question = Question.objects.filter(text=question_text).first()
        if not question:
            raise serializers.ValidationError({"question_text": "Question with this text does not exist"})

        # Validate the response
        response = data.get('response').lower()
        if response not in ['yes', 'no']:
            raise serializers.ValidationError({"response": "Response must be either 'yes' or 'no'"})

        # Set the question in validated data
        data['question'] = question
        return data

    def create(self, validated_data):
        validated_data.pop('question_text', None)  # Remove question_text since we already set question
        return super().create(validated_data)
