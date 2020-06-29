from rest_framework import serializers

from ..models import Poll, Answer
from .questions_serializers import ReadCreateQuestionsSerializer
from .answers_serializers import AnswerSerializer

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
  # Don't require poll field when passing 'questions' in the Poll form, we will fill those later in 'create' method:
  class QuestionsSerializer(ReadCreateQuestionsSerializer):
    class Meta(ReadCreateQuestionsSerializer.Meta):
      fields = [field for field in ReadCreateQuestionsSerializer.Meta.fields if field != 'poll']

  questions = QuestionsSerializer(many=True, required=True)

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
      question_serializer = ReadCreateQuestionsSerializer(data={**question_data, 'poll': poll.id})
      if not question_serializer.is_valid():
        raise serializers.ValidationError(question_serializer.errors)
      question_serializer.save()
    return poll


class UpdatePollsSerializer(ValidateEndDateMixin, serializers.ModelSerializer):
  class Meta:
    model = Poll
    fields = ['title', 'description', 'end_date']


class SubmitPollsSerializer(serializers.Serializer):
  answers = AnswerSerializer(many=True, required=True)
  user_id = serializers.IntegerField()
  poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.active())

  # Fill all answers with user_id field:
  def to_internal_value(self, data):
    if data.get('user_id', None) and data.get('answers', None) and isinstance(data['answers'], list):
      data['answers'] = [{**answer_data, 'user_id': data['user_id']} for answer_data in data['answers']]
    return super(SubmitPollsSerializer, self).to_internal_value(data)

  def validate(self, data):
    poll = data['poll']
    questions_count = poll.questions.all().count()
    answers_count = len(data['answers'])
    if questions_count != answers_count:
      raise serializers.ValidationError({
        "answers": f"answers count must match poll's questions count (answers: {answers_count}, questions: {questions_count})"
      })
    for answer_data in data['answers']:
      question_id = answer_data['question'].id
      if not poll.questions.filter(pk=question_id).exists():
        raise serializers.ValidationError({
          "answers": f"trying to answer a question that doesn't belong to the poll (question ID = {question_id})"
        })
    return data

  def create(self, validated_data):
    user_id = validated_data.pop('user_id')
    answers_data = [{**answer_data, 'user_id': user_id} for answer_data in validated_data.pop('answers')]
    for answer_data in answers_data:
      Answer.objects.create(**answer_data)
    return validated_data['poll']