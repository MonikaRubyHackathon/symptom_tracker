from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Deck(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  topic = models.CharField(max_length=100)
  owner = models.ForeignKey(
      get_user_model(),
      related_name='decks',
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The topic of this deck is '{self.topic}'."

  def as_dict(self):
    """Returns dictionary version of Deck models"""
    return {
        'id': self.id,
        'topic': self.topic
    }
