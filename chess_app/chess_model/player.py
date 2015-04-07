from piece import PieceColor

class Player(object):
    def __init__(self, playerName, color):
        self.playerName = playerName
        self.playerId = color.value
        self.pieceColor = color

    def getPlayerId(self):
        return self.playerId

    def getPlayerName(self):
        return self.playerName

    def getPlayerPieceColor(self):
        return self.pieceColor
