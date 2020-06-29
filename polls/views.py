from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.serializers import ValidationError
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

  submit: Submit a poll on behalf of a user (only for active polls).
  If question is a single choice than an answers field should be a choice ID.
  If question is a multiple choice than an answers field should be a choice IDs separated by a comma.
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
    if self.action == 'submit':
      return serializers.SubmitPollsSerializer
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
    serializer_class = self.get_serializer_class()
    serializer = serializer_class(data=request.data, context={'poll': Poll.objects.get(pk=pk)})
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  @action(detail=True, methods=['post'], permission_classes=[AllowAny])
  def submit(self, request, pk=None):
    serializer = self.get_serializer(data={**request.data, 'poll': pk})
    if serializer.is_valid():
      serializer.save()
      return Response("successfully submitted")
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

  # Don't delete the last question of the Poll, there should always be at least 1:
  def perform_destroy(self, instance):
    if instance.poll.questions.count() == 1:
      raise ValidationError({'questions': "Can't delete the last question"})
    instance.delete()
