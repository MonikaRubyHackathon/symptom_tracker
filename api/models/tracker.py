from django.db import models
from django import forms
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField

# Create your models here.
class Tracker(models.Model):
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  # DEFINE CHOICES
  TherapyType = (
    ('item_key1', 'Chemotherapy'),
    ('item_key2', 'Radiation'),
    ('item_key3', 'Hormonal'),
    ('item_key4', 'Biological'),
    ('item_key5', 'Surgery')
  )
  # Therapy = models.CharField(max_length = 20, choices = TherapyType)
  Symptoms = (
    (1, 'nausea'),
    (2, 'hair loss'),
    (3, 'anemia'),
    (4, 'fatigue')
  )
  # DEFINE FIELDS
  therapyType=MultiSelectField(
    choices = TherapyType,
    max_choices = 1
    # default = 'Chemotherapy'
  )
  symptoms=MultiSelectField(
    choices = Symptoms
  )

  owner = models.ForeignKey(
      get_user_model(),
      related_name = 'tracker',
      on_delete = models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The therapy type of this therapy is '{self.therapyType}'."

  def as_dict(self):
    """Returns dictionary version of Deck models"""
    return {
        'id': self.id,
        'therapy_type': self.therapyType,
        'symptoms': self.symptoms
    }
