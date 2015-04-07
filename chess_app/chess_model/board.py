from square import *
from history import History

class Board(object):
    def __init__(self):
        self.rows = 8
        self.cols = 8
        #self._squares = [[Square((row, col)) for col in xrange(self.cols)]
        #        for row in xrange(self.rows)]
        self._squares = []
        self._history = History()
        for row in xrange(self.rows):
            boardCol = []
            for col in xrange(self.cols):
                if (row + col) % 2 == 0:
                    square = BlackSquare((row, col))
                else:
                    square = WhiteSquare((row, col))

                square.setPieceSquare()
                boardCol.append(square)

            self._squares.append(boardCol)

    def checkBounds(self, location):
        row = location[0]
        col = location[1]

        if (row < 0 or row > 7 or col < 0 or col > 7):
            return False

        return True

    def isMovePossible(self, playerColor, fromPosition, toPosition):

        if not (self.checkBounds(fromPosition) and self.checkBounds(toPosition)):
            return False

        fromSquare = self._getSquareAtPosition(fromPosition)
        toSquare = self._getSquareAtPosition(toPosition)
        fromPiece = fromSquare.piece
        toPiece = toSquare.piece

        # No chess piece found at from location
        if not fromPiece:
            return False

        # Check if player is trying to move opponent's piece
        if fromPiece.pieceColor != playerColor:
            return False

        validPieceMove = fromPiece.isValidPieceMove(fromSquare,
                toSquare)

        if not validPieceMove:
            return False

        return self._canTraverseIntermediatePath(fromSquare, toSquare, fromPiece,
                toPiece)

    def _canTraverseIntermediatePath(self, fromSquare, toSquare, fromPiece,
            toPiece):

        # Get move square locations excluding the begin and end squares
        movePath = fromPiece.getIntermediateMovePath(fromSquare, toSquare)

        for (row, col) in movePath:
            square = self._squares[row][col]
            piece = square.piece
            if not piece:
                continue
            # A piece is present in the intermediate path, piece cannot skip
            # it
            return False

        if toPiece and fromPiece.pieceColor == toPiece.pieceColor:
            # Pieces are of the same color, cannot move
            return False

        return True

    def _getKingOfPlayer(self, playerColor):
        kingPiece = None
        kingPosition = None

        for row in xrange(self.rows):
            for col in xrange(self.cols):
                square = self._getSquareAtPosition((row, col))
                piece = square.piece
                # Finds the king piece belonging to this player
                if piece and piece.isPieceKing() and \
                    piece.getPieceColor() == playerColor:
                    kingPiece = piece
                    kingPosition = square.position

        return kingPiece, kingPosition

    def _getAllPiecesOfColor(self, color):
        pieces = []
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                piece = self._getPieceAtPosition((row,col))
                if piece and piece.getPieceColor() == color:
                    pieces.append(piece)

        return pieces

    def isPlayerChecked(self, playerColor, kingPiece = None, kingPosition =
            None):

        if not (kingPiece and kingPosition):
            kingPiece, kingPosition = self._getKingOfPlayer(playerColor)

        # Check each opponent piece if it is attacking the King
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                square = self._squares[row][col]
                piece = square.piece
                if piece and piece.getPieceColor() != playerColor:
                    movePossible = self.isMovePossible(piece.getPieceColor(),
                            square.position, kingPosition)
                    if movePossible:
                        return True

        return False

    """
    Try to move all pieces of player to all locations and check if there
    exists a valid legal move. If there is none, then the player has been
    check mated
    """
    def isPlayerCheckMate(self, playerColor):
        kingPiece, kingPosition = self._getKingOfPlayer(playerColor)
        pieces = self._getAllPiecesOfColor(playerColor)

        for piece in pieces:
            fromPosition = piece.getPiecePosition()
            for row in xrange(self.rows):
                for col in xrange(self.cols):
                    toPosition = (row, col)
                    movePossible = self.isMovePossible(playerColor, fromPosition,
                            toPosition)
                    if movePossible and not \
                    self.isPlayerChecked(playerColor, kingPiece, kingPosition):
                        return False

        return True


    def movePiece(self, fromPosition, toPosition):
        fromSquare = self._getSquareAtPosition(fromPosition)
        toSquare = self._getSquareAtPosition(toPosition)
        fromPiece = fromSquare.piece
        toPiece =  toSquare.piece
        fromSquare.removePiece()
        toSquare.setPiece(fromPiece)
        fromSquare.setPieceSquare()
        #fromPiece.setSquare(toSquare)

        #TODO: Add undo logic to store moved and killed piece locations
        self._history.makeMove(fromPosition, toPosition, toPiece)

    """
    Restores board state before the last move, if possible
    """
    def undoLastMove(self):
        if self._history.canUndoLastMove():
            fromPosition, toPosition, killedPiece = self._history.undoLastMove()
            piece = self._getPieceAtPosition(toPosition)
            fromSquare = self._getSquareAtPosition(fromPosition)
            toSquare = self._getSquareAtPosition(toPosition)
            fromSquare.setPiece(piece)
            toSquare.setPiece(killedPiece)
            fromSquare.setPieceSquare()
            toSquare.setPieceSquare()

            return True

        return False

    def _getSquareAtPosition(self, position):
        row = position[0]
        col = position[1]
        return self._squares[row][col]

    def _getPieceAtPosition(self, position):
        square = self._getSquareAtPosition(position)
        return square.getPiece()

    @property
    def getCurrentBoardState(self):
        return self._squares

    def printCurrentBoardState(self):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                print self._squares[row][col].getPieceInfoAtSquare(),
            print '\n'

