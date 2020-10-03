from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.deck import Deck
from .models.user import User
from .models.card import Card



class CardSerializer(serializers.ModelSerializer):
  deck_id = serializers.StringRelatedField(read_only=True)
  # only runs through when we're trying to Read the books, not create or update
  # like the string defined in the author model
  class Meta:
    model = Card
    fields = ('id', 'question','answer', 'created_at', 'updated_at', 'deck_id', 'owner')

class CardReadSerializer(CardSerializer):
    deck = serializers.StringRelatedField(read_only=True)
    question = serializers.CharField(max_length=100)
    answer = serializers.CharField(max_length=100)

# card_views - update route potentially needs this serializer
# class CardWriteSerializer(CardSerializer):
#     update = serializers.CharField(max_length=150, write_only=True)

class DeckSerializer(serializers.ModelSerializer):
    cards = CardReadSerializer(many=True, read_only=True)
    class Meta:
        model = Deck
        fields = ('id', 'topic', 'cards', 'owner')

class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserLoginSerializer(UserSerializer):
    # Require email, password for sign in
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)
