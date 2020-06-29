from rest_framework import serializers

from ..models import Poll
from .questions_serializers import ReadCreateQuestionsSerializer

class ValidateEndDateMixin(object):
  def validate(self, data):
    """
    Check that start date is before end date.
    """
    if 'end_date' in data and data.get('start_date', self.instance.start_date) > data['end_date']:
      raise serializers.ValidationError({
        "end_date": "end_date must occur after start_date"
      })
    return data


class ReadCreatePollsSerializer(serializers.ModelSerializer):
  questions = ReadCreateQuestionsSerializer(many=True, required=True)

  class Meta:
    model = Poll
    fields = ['id', 'title', 'description', 'start_date', 'end_date', 'questions']
    read_only_fields = ['id']

  def validate(self, data):
    if not data['questions']:
      raise serializers.ValidationError({
        "questions": "must contain at least 1 question"
      })
    return data

  def create(self, validated_data):
    questions_data = validated_data.pop('questions')
    poll = Poll.objects.create(**validated_data)
    for question_data in questions_data:
      # Use question serializer here since we may have even deeper nested fields like 'choices':
      question_serializer = ReadCreateQuestionsSerializer(data=question_data, context={'poll': poll})
      if not question_serializer.is_valid():
        raise serializers.ValidationError(question_serializer.errors)
      question_serializer.save()
    return poll


class UpdatePollsSerializer(ValidateEndDateMixin, serializers.ModelSerializer):
  class Meta:
    model = Poll
    fields = ['title', 'description', 'end_date']


