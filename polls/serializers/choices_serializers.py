from rest_framework import serializers

from ..models import Choice

class ChoiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Choice
    fields = ['id', 'text']
    read_only_fields = ['id']