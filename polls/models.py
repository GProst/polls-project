from django.db import models
from django.utils import timezone

class PollManager(models.Manager):
  def active(self):
    now = timezone.now()
    return self.filter(start_date__lt=now, end_date__gt=now)

class Poll(models.Model):
  objects = PollManager()

  title = models.CharField(max_length=255)
  description = models.TextField()
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()


class Question(models.Model):
  TEXT_TYPE = 'text'
  SINGLE_CHOICE_TYPE = 'single choice'
  MULTIPLE_CHOICE_TYPE = 'multiple choice'
  QUESTION_TYPES = [
    (TEXT_TYPE, 'text'), (SINGLE_CHOICE_TYPE, 'single choice'), (MULTIPLE_CHOICE_TYPE, 'multiple choice')
  ]

  text = models.CharField(max_length=255)
  type = models.CharField(max_length=255, choices=QUESTION_TYPES, default=TEXT_TYPE)
  poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)


class Choice(models.Model):
  text = models.CharField(max_length=255)
  question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)


class Answer(models.Model):
  answer = models.TextField()
  question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
  user_id = models.IntegerField()
