from rest_framework import serializers

from ..models import Choice

class ChoiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Choice
    fields = ['id', 'text', 'question']
    read_only_fields = ['id', 'question']