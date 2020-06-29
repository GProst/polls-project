from django.db import models

class Poll(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
