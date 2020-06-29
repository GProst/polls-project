from rest_framework import serializers

from ..models import Question, Choice
from .choices_serializers import ChoiceSerializer

class ReadCreateQuestionsSerializer(serializers.ModelSerializer):
  choices = ChoiceSerializer(many=True, required=False)

  class Meta:
    model = Question
    fields = ['id', 'text', 'type', 'choices', 'poll']
    read_only_fields = ['id']

  def validate(self, data):
    if (not data.get('choices', None) or len(data['choices']) < 2) and data.get('type', Question.TEXT_TYPE) != Question.TEXT_TYPE:
      raise serializers.ValidationError({
        "choices": "must contain at least 2 choices"
      })
    return data

  def create(self, validated_data):
    choices_data = None
    if 'choices' in validated_data:
      choices_data = validated_data.pop('choices')
    question = Question.objects.create(**validated_data)
    if validated_data.get('type', Question.TEXT_TYPE) != Question.TEXT_TYPE:
      for choice_data in choices_data:
        Choice.objects.create(question=question, **choice_data)
    return question

class UpdateQuestionsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Question
    fields = ['text']