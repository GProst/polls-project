from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Poll
from . import serializers

class PollsViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAdminUser]
  queryset = Poll.objects.all()

  def get_serializer_class(self):
    if self.action in ['list', 'retrieve']:
      return serializers.ReadPollsSerializer
    if self.action == 'create':
      return serializers.CreatePollsSerializer
    if self.action in ['update', 'partial_update']:
      return serializers.UpdatePollsSerializer
    return
