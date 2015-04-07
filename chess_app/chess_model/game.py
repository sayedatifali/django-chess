from board import Board
from player import Player
from piece import PieceColor

class Game(object):
    def __init__(self, playerA = "Player A", playerB = "Player B"):
        self._board = Board()
        self.players = [Player(playerA, PieceColor.White), Player(playerB,
        PieceColor.Black)]
        self.playerIdTurn = PieceColor.White.value
        self.winner = ""
        self._gameOver = False
        self.totalMoves = 0

    def play(self):

        while True:
            return

    def isGameOver(self):
        #Check if game is over. Return stalemate or checkmate
        return self._gameOver

    def _setGameOverWithWinner(self, winner):
        self._gameOver = True
        # Notify all observers here that the game is over

    """
    Make move first checks if it's the turn of the current player.
    Then it verifies whether the player is moving his/her own piece.

    At last it'll check if the opponent player can make any legal moves.
    If not, then the game will be declared over.
    """
    def makeMove(self, playerId, fromPosition, toPosition):
        if self.playerIdTurn != playerId:
            raise PlayerTurnError("It's not the turn of player %s"
                    %playerId)

        #TODO: Check if player is moving the correct piece color

        if self.isGameOver():
            return False

        player = self.players[playerId]
        playerColor = player.getPlayerPieceColor()
        validMove = self._board.isMovePossible(playerColor, fromPosition, toPosition)

        if not validMove:
            print 'Cannot move the piece, Invalid move'
            # Construct json object and return information
            return

        # Simulate move and check if the King is checked
        self._board.movePiece(fromPosition, toPosition)

        #TODO: Check for checkmate, en passe, castling or check condition

        # Checks if the current move has caused the current player's king to be
        # checked. Reverts the move if this is the case. Also, returns false
        if self._board.isPlayerChecked(playerColor):
            self._board.undoLastMove()
            print 'Cannot make this move. King is left in a check position'
            return False

        #Check if the opponent's King has been check mate
        opponentId = self.playerIdTurn ^ 1
        opponentPlayer = self.players[opponentId]
        opponentPlayerColor = opponentPlayer.getPlayerPieceColor()

        if self._board.isPlayerCheckMate(opponentPlayerColor):
            self._setGameOverWithWinner(player)

        if self._board.isPlayerChecked(opponentPlayerColor):
            #TODO: Return information in JSON that opponent is in check
            print 'Opponent player has been checked'

        self.totalMoves += 1
        #self._board.movePiece(fromPosition, toPosition)
        self.playerIdTurn ^= 1

    def undoLastMove(self):
        undo = self._board.undoLastMove()
        if not undo:
            print 'Cannot undo any more'
        else:
            self.totalMoves -= 1

    def printGameState(self):
        print '\nGame State after move number %s:\n' \
            %self.totalMoves
        self._board.printCurrentBoardState()

class PlayerTurnError(Exception):
    def __init__(self, message = ""):
        super(PlayerTurnError, self).__init__(message)

if __name__=="__main__":
    game = Game("Atif", "Nitin")
    game.makeMove(0, (0,0), (1,1))
    game.printGameState()
    game.makeMove(0, (1,0), (2,0))
    game.printGameState()
    game.makeMove(1, (7,1), (5,2))
    game.printGameState()

    game.undoLastMove()
    game.printGameState()
    game.undoLastMove()
    game.printGameState()
    game.undoLastMove()

