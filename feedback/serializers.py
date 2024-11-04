from rest_framework import serializers
from .models import Question, Feedback

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text']

class FeedbackSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(write_only=True)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)  

    class Meta:
        model = Feedback
        fields = ['id', 'question', 'question_text', 'response']

    def validate(self, data):
        question_text = data.get('question_text')
        
        question = Question.objects.filter(text=question_text).first()
        if not question:
            raise serializers.ValidationError({"question_text": "Question with this text does not exist"})

        response = data.get('response').lower()
        if response not in ['yes', 'no']:
            raise serializers.ValidationError({"response": "Response must be either 'yes' or 'no'"})

        data['question'] = question
        return data

    def create(self, validated_data):
        validated_data.pop('question_text', None) 
        return super().create(validated_data)
