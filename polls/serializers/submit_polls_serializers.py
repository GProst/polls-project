from rest_framework import serializers

from ..models import Answer, Question

class AnswerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Answer
    fields = ['id', 'answer', 'question']
    read_only_fields = ['id']

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


class SubmitPollsSerializer(serializers.Serializer):
  answers = AnswerSerializer(many=True, required=True)
  user_id = serializers.IntegerField()

  def validate(self, data):
    user_id = data['user_id']
    poll = self.context['view'].get_object()
    poll_question_ids = poll.questions.values_list('id', flat=True)
    existing_answers_count = Answer.objects.filter(question__in=poll_question_ids, user_id=user_id).count()
    if existing_answers_count > 0:
      raise serializers.ValidationError(f"User with ID = {user_id} already submitted answers for the poll with ID = {poll.id}")
    answers_count = len(data['answers'])
    questions_count = poll.questions.all().count()
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

  def save(self):
    user_id = self.validated_data.pop('user_id')
    answers_data = [{**answer_data, 'user_id': user_id} for answer_data in self.validated_data.pop('answers')]
    for answer_data in answers_data:
      Answer.objects.create(**answer_data)