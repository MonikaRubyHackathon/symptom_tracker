from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.tracker import Tracker
from ..serializers import TrackerSerializer, UserSerializer

# Create your views here.
class Tracker(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = TrackerSerializer
    def get(self, request):
        """Index request"""
        # Get all the decks:
        # decks = deck.objects.all()
        # Filter the decks by owner, so you can only see your owned decks
        tracker = Tracker.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = TrackerSerializer(tracker, many=False).data
        return Response({ 'tracker': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['tracker']['owner'] = request.user.id
        # Serialize/create deck
        tracker = TrackerSerializer(data=request.data['tracker'])
        # If the deck data is valid according to our serializer...
        if tracker.is_valid():
            # Save the created deck & send a response
            tracker.save()
            return Response({ 'tracker': tracker.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(tracker.errors, status=status.HTTP_400_BAD_REQUEST)

class TrackerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the deck to show
        tracker = get_object_or_404(Tracker, pk=pk)
        # Only want to show owned decks?
        if not request.user.id == tracker.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this deck')

        # Run the data through the serializer so it's formatted
        data = TrackerSerializer(tracker).data
        return Response({ 'tracker': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate deck to delete
        tracker = get_object_or_404(Tracker, pk=pk)
        # Check the deck's owner agains the user making this request
        if not request.user.id == tracker.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this deck')
        # Only delete if the user owns the  deck
        tracker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate deck
        # get_object_or_404 returns a object representation of our deck
        tracker_instance = get_object_or_404(Tracker, pk=pk)
        # Remove owner from request object
        # This "gets" the owner key on the data['deck'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        # print(f'update data is {request.data}')
        if request.data['tracker'].get('owner', False):
            del request.data['deck']['owner']

        # Check if user is the same as the request.user.id
        if not request.user.id == tracker_instance.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this deck')

        # Add owner to data object now that we know this user owns the resource
        request.data['tracker']['owner'] = request.user.id
        # Validate updates with serializer
        ts = TrackerSerializer(tracker_instance, data=request.data['tracker'])
        if ts.is_valid():
            # Save & send a 204 no content
            ts.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
