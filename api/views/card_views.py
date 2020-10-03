from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token


from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ..models.card import Card
from ..serializers import CardSerializer, CardReadSerializer

# Create your views here.
class Cards(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request):
        """Index Request"""
        # print(request)
        cards = Card.objects.filter(owner=request.user.id)
        cards = Card.objects.all()[:10]
        # [:10] -- this could be a potential way to put a limit on how many cards to create!
        data = CardReadSerializer(cards, many=True).data
        return Response({ 'cards': data })

    serializer_class = CardSerializer
    def post(self, request):
        """Post request"""
        print(request.data)
        request.data['card']['owner'] = request.user.id
        card = CardSerializer(data=request.data['card'])
        if card.is_valid():
            card.save()
            return Response(card.data, status=status.HTTP_201_CREATED)
        else:
            return Response(card.errors, status=status.HTTP_400_BAD_REQUEST)

class CardDetail(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        card = get_object_or_404(Card, pk=pk)
        if not request.user.id == card.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this card')
        data = CardReadSerializer(card).data
        return Response({ 'card': data })

    def partial_update(self, request, pk):
        """Update Request"""
        card = get_object_or_404(Card, pk=pk)
        if request.data['card'].get('owner', False):
            del request.data['card']['owner']
        if not request.user.id == deck_instance.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this card')
        request.data['card']['owner'] = request.user.id
        ms = CardSerializer(card, data=request.data['card'], partial=True)
        if ms.is_valid():
            ms.save()
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete Request"""
        card = get_object_or_404(Card, pk=pk)
        if not request.user.id == deck.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this card')
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
