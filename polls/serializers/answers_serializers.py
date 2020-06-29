from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import Answer, Question

class AnswerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Answer
    fields = ['id', 'answer', 'question', 'user_id']
    read_only_fields = ['id']

    validators = [
      UniqueTogetherValidator(
        queryset=Answer.objects.all(),
        fields=['user_id', 'question']
      )
    ]

  def validate(self, data):
    question = data['question']
    """
    If question is single choice or multiple choice type then an answer should be a string with choice IDs
    separated by comma:
    """
    if question.type != Question.TEXT_TYPE:
      choice_ids = data['answer'].split(',')
      try:
        choice_ids = [int(choice_id) for choice_id in choice_ids]
      except ValueError:
        if question.type == Question.SINGLE_CHOICE_TYPE:
          raise serializers.ValidationError({
            "answer": f"should be an ID of a choice"
          })
        else:
          raise serializers.ValidationError({
            "answer": f"should be an ID of a choice of multiple choice IDs separated by comma"
          })

      if len(choice_ids) != 1 and question.type == Question.SINGLE_CHOICE_TYPE:
        raise serializers.ValidationError({
          "answer": f"answer should contain a single choice ID for question with ID = '{question.id}'"
        })

      for choice_id in choice_ids:
        if not question.choices.filter(pk=choice_id).exists():
          raise serializers.ValidationError({
            "answer": f"choice with ID = '{choice_id}' not found for question with ID = '{question.id}'"
          })
    return data