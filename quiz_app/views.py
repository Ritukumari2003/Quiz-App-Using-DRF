from django.shortcuts import render
from .models import *

from .serializers import QuizSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    @action(detail=True, methods=['POST'])
    def submit_answer(self, request, pk=None):
        question_id = request.data.get('question_id')
        answer_id = request.data.get('answer_id')

        try:
            question = Question.objects.get(id = question_id, quiz_id=pk)
        except Question.DoesNotExist:
            return Response({'error': 'Invalid Question ID'}, status = status.HTTP_404_BAD_REQUEST)
        
        try:
            answer = question.answers.get(id = answer_id)
        except Answer.DoesNotExist:
            return Response({'error': 'Invalid Question ID'}, status = status.HTTP_404_BAD_REQUEST)
        
        if answer.is_correct():
            return Response({'message': 'Correct Answer'}, status= status.HTTP_200_OK)
        else:
            return Response({'message': 'Incorrect Answer'}, status= status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def add_question(self, request, pk=None):
        quiz = self.get_object()
        question_text = request.data.get('text')
        answers_data = request.data.get('answers', [])

        if not question_text:
            return Response({'error': 'Question Text is required!!!..'}, status=status.HTTP_400_BAD_REQUEST)
        
        question = Question.objects.create(quiz=quiz, text=question_text)

        for answer_data in answers_data:
            Answer.objects.create(
                question=question,
                text=answer_data['text'],
                is_correct=answer_data['is_correct']
            )

        return Response({'message': 'Question Added Successfully'}, status=status.HTTP_201_CREATED)


