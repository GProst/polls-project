from rest_framework import serializers

from ..models import Question

class SubmittedPollSerializer(serializers.BaseSerializer):
  @staticmethod
  def get_answer_representation(question, user_id):
    answer = question.answers.get(user_id=user_id).answer
    if question.type == Question.TEXT_TYPE:
      return answer
    elif question.type == Question.SINGLE_CHOICE_TYPE:
      return int(answer)
    else:
      return [int(a) for a in answer.split(',')]

  def to_representation(self, poll):
    user_id = self.context['view'].request.query_params['user_id']

    return {
      'id': poll.id,
      'title': poll.title,
      'description': poll.description,
      'start_date': poll.start_date,
      'end_date': poll.end_date,
      'questions': [{
        'id': question.id,
        'text': question.text,
        'type': question.type,
        'choices': [{
          'id': choice.id,
          'text': choice.text
        } for choice in question.choices.all()],
        'answer': self.get_answer_representation(question, user_id)
      } for question in poll.questions.all()]
    }