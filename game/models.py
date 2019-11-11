from django.db import models
from django.core.exceptions import ValidationError
import game.constants
import json

# Create your models here.
def validate_col_range(value):
    if value < 0 or value > game.constants.MAX_COLS - 1:
        raise ValidationError('Out of range',)

def validate_row_range(value):
    if value < 0 or value > game.constants.MAX_ROWS - 1:
         raise ValidationError('Out of range',)

def validate_unique_tag(value):
    for player in Player.objects.all():
        if player.tag == value:
            raise ValidationError('Tag already taken',)

def validate_player_count(value):
    players = Player.objects.all()
    if len(players) > 1:
        raise ValidationError('Too many players')

class Player(models.Model):
    tag = models.CharField(max_length=1, validators=[validate_unique_tag, validate_player_count])
    row = models.IntegerField(validators=[validate_row_range])
    col = models.IntegerField(validators=[validate_col_range])

    def __str__(self):
        return self.tag + ' @(' + str(self.row) + ',' + str(self.col) + ')'

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self._prev_row = self.row
        self._prev_col = self.col

    def clean(self):
        if self._prev_row != None:
            if abs(self.row - self._prev_row) > 1:
                raise ValidationError('Row too far')
            if abs(self.col - self._prev_col) > 1:
                raise ValidationError('Column too far')
            if abs(self.col - self._prev_col) == 1 and abs(self.row - self._prev_row) == 1:
                raise ValidationError('No Diagonal Moves')

class PlayerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return { 'id': obj.id, 'tag': obj.tag, 'row': obj.row, 'col': obj.col }
        return json.JSONEncoder.default(self, obj)

class BoardEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Board):
            return { 'grid': obj.grid }
        return json.JSONEncoder.default(self, obj)


class Board():
    players= []
    grid = ''

    def __init__(self):
        self.initBoard()

    def initBoard(self):
        self.grid = [["_" for x in range(game.constants.MAX_COLS)] for y in range(game.constants.MAX_ROWS)]

    def getPlayers(self):
         self.players = Player.objects.all()
         self.makeMove()

    def makeMove(self):
        self.initBoard()
        for player in self.players:
            self.grid[player.row][player.col] = player.tag
