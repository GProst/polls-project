from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Poll, Question
from . import serializers

class PollsViewSet(viewsets.ModelViewSet):
  """
  list: Get all polls

  active: Get active polls

  retrieve: Get a poll by ID

  update: Update a poll by ID

  create: Create a poll

  partial_update: Update a poll by ID

  destroy: Delete a poll by ID

  questions: Get poll's questions

  create_questions: Create a poll's question
  """
  permission_classes = [IsAdminUser]
  queryset = Poll.objects.all()

  def get_serializer_class(self):
    if self.action in ['list', 'retrieve', 'active', 'create']:
      return serializers.ReadCreatePollsSerializer
    if self.action in ['update', 'partial_update']:
      return serializers.UpdatePollsSerializer
    if self.action in ['create_questions', 'questions']:
      return serializers.ReadCreateQuestionsSerializer
    return

  @action(detail=False, permission_classes=[AllowAny])
  def active(self, request):
    active_polls = Poll.objects.active()
    serializer = self.get_serializer(active_polls, many=True)
    return Response(serializer.data)

  @action(detail=True, methods=['get'])
  def questions(self, request, pk=None):
    poll = self.get_object()
    serializer = self.get_serializer(poll.questions.all(), many=True)
    return Response(serializer.data)

  @questions.mapping.post
  def create_questions(self, request, pk=None):
    poll = self.get_object()
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid()
    if serializer.is_valid():
      question = poll.questions.create(**serializer.data)
      return Response(self.get_serializer(question).data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionsViewSet(viewsets.ModelViewSet):
  """
  list: Get all questions

  retrieve: Get a question by ID

  update: Update a question by ID

  partial_update: Update a question by ID

  destroy: Delete a question by ID
  """
  permission_classes = [IsAdminUser]
  queryset = Question.objects.all()
  http_method_names = ['get', 'put', 'patch', 'delete']

  def get_serializer_class(self):
    if self.action in ['list', 'retrieve', 'create']:
      return serializers.ReadCreateQuestionsSerializer
    if self.action in ['update', 'partial_update']:
      return serializers.UpdateQuestionsSerializer
    return
