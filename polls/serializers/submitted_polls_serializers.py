from rest_framework import serializers

class SubmittedPollSerializer(serializers.BaseSerializer):
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
        'answer': question.answers.get(user_id=user_id).answer
      } for question in poll.questions.all()]
    }