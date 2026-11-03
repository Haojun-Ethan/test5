from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets # new added
from django.shortcuts import get_object_or_404
from django.utils import timezone
from decimal import Decimal

from modules.models import Module
from .models import Question, Choice, Attempt, AttemptAnswer
from .serializers import QuestionSerializer, AttemptSerializer, ChoiceSerializer # new added

class ModuleQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        questions = Question.objects.filter(module_id=pk, is_active=True).order_by('order')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class StartAttemptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        module = get_object_or_404(Module, pk=pk)
        attempt = Attempt.objects.create(user=request.user, module=module)
        return Response({
            'id': attempt.id,
            'moduleId': module.id,
            'startedAt': attempt.started_at
        }, status=status.HTTP_201_CREATED)


class SubmitAttemptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        attempt = get_object_or_404(Attempt, pk=pk, user=request.user)
        
        if attempt.submitted_at:
            return Response({'message': 'This attempt has already been submitted.'}, status=status.HTTP_400_BAD_REQUEST)

        answers_data = request.data.get('answers', {})
        total_points = 0
        earned_points = 0
        
        questions = Question.objects.filter(module=attempt.module, is_active=True)
        
        for question in questions:
            total_points += question.points
            user_answer = answers_data.get(str(question.id)) or answers_data.get(question.id)
            
            if user_answer is not None:
                correct_choices = list(question.choices.filter(is_correct=True).values_list('id', flat=True))
                is_correct = False
                
                if question.question_type == 'SINGLE':
                    is_correct = int(user_answer) in correct_choices
                elif question.question_type == 'MULTIPLE':
                    if isinstance(user_answer, list):
                        user_choices = [int(uid) for uid in user_answer]
                        is_correct = set(user_choices) == set(correct_choices)
                
                if is_correct:
                    earned_points += question.points
                    AttemptAnswer.objects.create(
                        attempt=attempt, 
                        question=question, 
                        selected_choice_id=int(user_answer[0]) if isinstance(user_answer, list) else int(user_answer),
                        is_correct=True, 
                        points_awarded=question.points
                    )

        if total_points > 0:
            score_percent = (Decimal(earned_points) / Decimal(total_points)) * 100
        else:
            score_percent = Decimal(0)

        passed = score_percent >= attempt.module.pass_mark

        attempt.submitted_at = timezone.now()
        attempt.score_percent = score_percent
        attempt.passed = passed
        attempt.save()

        return Response({
            'id': attempt.id,
            'scorePercent': float(score_percent),
            'passed': passed,
            'userAnswers': answers_data
        })


class QuestionViewSet(viewsets.ModelViewSet): # new added
    queryset = Question.objects.all() # new added
    serializer_class = QuestionSerializer # new added
    permission_classes = [IsAuthenticated] # new added


class ChoiceViewSet(viewsets.ModelViewSet): # new added
    queryset = Choice.objects.all() # new added
    serializer_class = ChoiceSerializer # new added
    permission_classes = [IsAuthenticated] # new added