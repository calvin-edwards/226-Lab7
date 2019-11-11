from django.test import TestCase
from game.models import Player, Board
import game.constants
import json
# Create your tests here.
class PlayerTestCase(TestCase):
    def test_duplicate_player(self):
        response = self.client.post("/game/player/create/", { 'tag':'T', 'row':3, 'col': 7 } )
        response = self.client.post("/game/player/create/", { 'tag':'T', 'row':4, 'col': 8 } )
        self.assertFormError(response, 'form', 'tag', 'Tag already taken')

        try:
            player = Player.objects.get(tag='T')
            if player.row != 3 and player.col != 7:
                self.fail()
            pass

        except Exception as e:
            print(e)
            pass

    def test_create_oob_EAST(self):
        response = self.client.post("/game/player/create/", { 'tag':'Q', 'row': game.constants.MAX_ROWS, 'col': 0} )
        self.assertFormError(response, 'form', 'row', 'Out of range')
        try:
            Player.objects.get(tag='Q')
            self.fail()
        except Player.DoesNotExist:
            pass

    def test_create_oob_WEST(self):
        response = self.client.post("/game/player/create/", { 'tag':'Q', 'row':-1, 'col': 0 } )
        self.assertFormError(response, 'form', 'row', 'Out of range')
        try:
            Player.objects.get(tag='Q')
            self.fail()
        except Player.DoesNotExist:
            pass

    def test_create_oob_NORTH(self):
        response = self.client.post("/game/player/create/", { 'tag':'Q', 'row':0, 'col': -1 } )
        self.assertFormError(response, 'form', 'col', 'Out of range')
        try:
            Player.objects.get(tag='Q')
            self.fail()
        except Player.DoesNotExist:
            pass

    def test_create_oob_SOUTH(self):
        response = self.client.post("/game/player/create/", { 'tag':'Q', 'row':0, 'col': game.constants.MAX_COLS } )
        self.assertFormError(response, 'form', 'col', 'Out of range')
        try:
            Player.objects.get(tag='Q')
            self.fail()
        except Player.DoesNotExist:
            pass

    def test_update_oob_WEST(self):
        self.client.post("/game/player/create/", { 'tag':'Q', 'row':0, 'col': 0 } )
        response = self.client.post("/game/player/1/update/", { 'row':-1, 'col': 0 } )
        self.assertIn(b'Out of range', response._container[0])

    
    def test_update_oob_EAST(self):
        self.client.post("/game/player/create/", { 'tag':'Q', 'row': game.constants.MAX_ROWS-1, 'col': 0 } )
        response = self.client.post("/game/player/1/update/", { 'row': game.constants.MAX_ROWS, 'col': 0 } )
        self.assertIn(b'Out of range', response._container[0])

 
    def test_update_oob_NORTH(self):
        self.client.post("/game/player/create/", { 'tag':'Q', 'row':0, 'col': 0 } )
        response = self.client.post("/game/player/1/update/", { 'row':0, 'col': -1 } )
        self.assertIn(b'Out of range', response._container[0])


    def test_update_oob_SOUTH(self):
        self.client.post("/game/player/create/", { 'tag':'Q', 'row':0, 'col': game.constants.MAX_COLS-1 } )
        response = self.client.post("/game/player/1/update/", { 'row':0, 'col': game.constants.MAX_COLS } )
        self.assertIn(b'Out of range', response._container[0])
