from django.db import models
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField

# Create your models here.
class Tracker(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  TherapyType = (
    ('Chemotherapy'),
    ('Radiation'),
    ('Hormonal'),
    ('Biological'),
    ('Surgery')
  )
  # Therapy = models.CharField(max_length = 20, choices = TherapyType)
  Symptoms = (
    ('nausea'),
    ('hair loss'),
    ('anemia'),
    ('fatigue')
  )

  owner = models.ForeignKey(
      get_user_model(),
      therapyType = models.ChoiceField(
        max_length = 20,
        choices = TherapyType,
        default = 'Chemotherapy'
      ),
      symptoms=models.ChoiceField(
        max_length = 20,
        choices = Symptoms
      ),
      related_name = 'tracker',
      on_delete = models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The therapy type of this therapy is '{self.therapy_type}'."

  def as_dict(self):
    """Returns dictionary version of Deck models"""
    return {
        'id': self.id,
        'therapy_type': self.therapy_type,
        'symptoms':
    }
