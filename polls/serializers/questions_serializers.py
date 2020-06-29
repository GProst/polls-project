from rest_framework import serializers

from ..models import Question, Choice
from .choices_serializers import ChoiceSerializer

class ReadCreateQuestionsSerializer(serializers.ModelSerializer):
  choices = ChoiceSerializer(many=True, required=False)

  class Meta:
    model = Question
    fields = ['id', 'text', 'type', 'choices', 'poll']
    read_only_fields = ['id', 'poll']

  def to_representation(self, question):
    data = super(ReadCreateQuestionsSerializer, self).to_representation(question)
    if question.type == Question.TEXT_TYPE:
      data.pop('choices', None)
    # If we request question in a context of a poll then no need to include poll ID here:
    if self.context.get('poll', None):
      data.pop('poll', None)
    return data

  def validate(self, data):
    if (not data.get('choices', None) or len(data['choices']) < 2) and data.get('type', Question.TEXT_TYPE) != Question.TEXT_TYPE:
      raise serializers.ValidationError({
        "choices": "must contain at least 2 choices"
      })
    return data

  def create(self, validated_data):
    poll = self.context['poll']
    choices_data = None
    if 'choices' in validated_data:
      choices_data = validated_data.pop('choices')
    question = poll.questions.create(**validated_data)
    if validated_data.get('type', Question.TEXT_TYPE) != Question.TEXT_TYPE:
      for choice_data in choices_data:
        Choice.objects.create(question=question, **choice_data)
    return question

class UpdateQuestionsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Question
    fields = ['text']