from rest_framework import serializers

from .models import Poll

class ReadPollsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Poll
    fields = ['id', 'title', 'description', 'start_date', 'end_date']

class CreatePollsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Poll
    fields = ['id', 'title', 'description', 'start_date', 'end_date']

class UpdatePollsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Poll
    fields = ['title', 'description', 'end_date']
