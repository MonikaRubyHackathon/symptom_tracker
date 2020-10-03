from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.deck import Deck
from ..serializers import DeckSerializer, UserSerializer

# Create your views here.
class Decks(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = DeckSerializer
    def get(self, request):
        """Index request"""
        # Get all the decks:
        # decks = deck.objects.all()
        # Filter the decks by owner, so you can only see your owned decks
        decks = Deck.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = DeckSerializer(decks, many=True).data
        return Response({ 'decks': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['deck']['owner'] = request.user.id
        # Serialize/create deck
        deck = DeckSerializer(data=request.data['deck'])
        # If the deck data is valid according to our serializer...
        if deck.is_valid():
            # Save the created deck & send a response
            deck.save()
            return Response({ 'deck': deck.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(deck.errors, status=status.HTTP_400_BAD_REQUEST)

class DeckDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the deck to show
        deck = get_object_or_404(Deck, pk=pk)
        # Only want to show owned decks?
        if not request.user.id == deck.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this deck')

        # Run the data through the serializer so it's formatted
        data = DeckSerializer(deck).data
        return Response({ 'deck': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate deck to delete
        deck = get_object_or_404(Deck, pk=pk)
        # Check the deck's owner agains the user making this request
        if not request.user.id == deck.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this deck')
        # Only delete if the user owns the  deck
        deck.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate deck
        # get_object_or_404 returns a object representation of our deck
        deck_instance = get_object_or_404(Deck, pk=pk)
        # Remove owner from request object
        # This "gets" the owner key on the data['deck'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        # print(f'update data is {request.data}')
        if request.data['deck'].get('owner', False):
            del request.data['deck']['owner']

        # Check if user is the same as the request.user.id
        if not request.user.id == deck_instance.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this deck')

        # Add owner to data object now that we know this user owns the resource
        request.data['deck']['owner'] = request.user.id
        # Validate updates with serializer
        ds = DeckSerializer(deck_instance, data=request.data['deck'])
        if ds.is_valid():
            # Save & send a 204 no content
            ds.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
