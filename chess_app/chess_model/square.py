from piece import *
from logger import logger
import pdb

class Square(object):
    def __init__(self, position):
        self.piece = None
        self.row = position[0]
        self.col = position[1]
        self.position = position

        self.piece = PieceFactory.createPieceWithPos(position)
        if self.piece is not None:
            logger.debug(self.piece)

    def setPieceSquare(self):
        if self.piece is not None:
            self.piece.setSquare(self)

    def setPieceWithId(self, pieceId):
        self.piece = PieceFactory.createPieceWithId(pieceId)
        #logger.debug(self.piece)

    def setPiece(self, piece):
        self.piece = piece

    def removePiece(self):
        #pdb.set_trace()
        if self.piece:
            self.piece.clearSquare()
        self.piece = None

    def getPiece(self):
        return self.piece

    def getPosition(self):
        return self.position

    def isEmpty(self):
        if self.piece is not None:
            return False
        return True

    def isOccupied(self):
        return not isEmpty()

    def getPieceColorAtSquare(self):
        if isEmpty():
            return -1
        return self.piece.pieceColor

    def getPieceInfoAtSquare(self):
        if not self.piece:
            return '...'
        return self.piece.getPiece()

    def __str__(self):
        return "Square with position (%s, %s)" %(self.row, self.col)

class WhiteSquare(Square):
    def __init__(self, position):
        super(WhiteSquare, self).__init__(position)
        self.squareColor = SquareType.White

class BlackSquare(Square):
    def __init__(self, position):
        super(BlackSquare, self).__init__(position)
        self.squareColor = SquareType.Black

class SquareType(Enum):
    White = 0
    Black = 1
