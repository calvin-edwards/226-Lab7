from django.shortcuts import render
from django.http import HttpResponse
from game.models import Player, Board, PlayerEncoder, BoardEncoder
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
import json

board = Board()

def index(request):
    board.getPlayers()
    board.makeMove()
    return HttpResponse(json.dumps(board, cls=BoardEncoder))

# Create your views here.
def get_player(request, id):
    player = Player.objects.filter(id=id)
    if (len(player) == 1):
        return HttpResponse(json.dumps(player[0], cls=PlayerEncoder))
    else:
        return HttpResponse("No such player")

class PlayerCreate(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('index')

class PlayerUpdate(UpdateView):
    model = Player
    fields = ['row', 'col']
    success_url = reverse_lazy('index')
