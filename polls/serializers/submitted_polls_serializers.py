from rest_framework import serializers

from ..models import Question

class SubmittedPollSerializer(serializers.BaseSerializer):
  @staticmethod
  def get_question_representation(question, user_id):
    result = {
      'id': question.id,
      'text': question.text,
      'type': question.type,
      'choices': [{
        'id': choice.id,
        'text': choice.text
      } for choice in question.choices.all()],
      **SubmittedPollSerializer.get_answer_representation(question, user_id)
    }
    if question.type == Question.TEXT_TYPE:
      del result['choices']
    return result

  @staticmethod
  def get_answer_representation(question, user_id):
    answer = question.answers.get(user_id=user_id).answer
    if question.type == Question.TEXT_TYPE:
      return {'answer':answer}
    elif question.type == Question.SINGLE_CHOICE_TYPE:
      return {'selected_choice': int(answer)}
    else:
      return {'selected_choices': [int(a) for a in answer.split(',')]}

  def to_representation(self, poll):
    user_id = self.context['view'].request.query_params['user_id']
    return {
      'id': poll.id,
      'title': poll.title,
      'description': poll.description,
      'start_date': poll.start_date,
      'end_date': poll.end_date,
      'questions': [self.get_question_representation(question, user_id) for question in poll.questions.all()]
    }