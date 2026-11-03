from rest_framework import serializers
from .models import Question, Choice, Attempt, AttemptAnswer

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice

        fields = ['id', 'question', 'text', 'order', 'is_correct'] 

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'module', 'text', 'question_type', 'explanation', 'points', 'order', 'choices']

class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = ['id', 'module', 'started_at', 'submitted_at', 'score_percent', 'passed']