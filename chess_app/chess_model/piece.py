from enum import Enum

class Piece(object):

    pieceNames = ['King', 'Queen', 'Bishop', 'Knight', 'Rook', 'Pawn']
    pieceColors = ['White', 'Black']

    def __init__(self, color, pieceType):
        self.pieceColor = color
        #pieceType is enum of class PieceType
        self.pieceType = pieceType
        #print pieceType
        self.pieceName = Piece.pieceNames[pieceType.value]
        #print self.pieceName
        self.square = None
        self.moved = False

    def __str__(self):
        if self.square is not None:
            return 'Piece is a %s of color %s at postion (%s, %s)' %(self.pieceName,
                self.pieceColor, self.square.row, self.square.col)
        else:
            return 'Piece is a %s of color %s' %(self.pieceName,
                self.pieceColor)

    def setSquare(self, square):
        self.square = square

    def clearSquare(self):
        self.square = None

    def hasPieceEverMoved(self):
        return self.moved

    def getPieceType(self):
        return self.pieceType

    def getPiece(self):
        info = Piece.pieceColors[self.pieceColor.value][:1]
        info += Piece.pieceNames[self.pieceType.value][:2]
        return info

    def getPiecePosition(self):
        return self.square.getPosition()

    def getPieceColor(self):
        return self.pieceColor

    def getMovePath(self, fromSquare, toSquare):
        raise NotImplementedError("Piece subclasses should implement this" \
        "method")

    def getIntermediateMovePath(self, fromSquare, toSquare):
        path = self.getMovePath(fromSquare, toSquare)
        return path[1: -1]

    def isPieceKing(self):
        return False

    def isKingInCheck(self):
        raise NotImplementedError("Piece subclasses should implement this" \
        "method")

    def isValidPieceMove(self, fromSquare, toSquare):
        raise NotImplementedError("Piece subclasses should implement this" \
        "method")

    def movePiece(self, fromSquare, toSquare):
        raise NotImplementedError("Piece subclasses should implement this" \
        "method")

class KingPiece(Piece):

    def __init__(self, pieceColor):
        super(KingPiece, self).__init__(pieceColor, PieceType.King)
        self.castled = False
        self.check = False

    def isPieceKing(self):
        return True

    def isValidPieceMove(self, fromSquare, toSquare):
        diff = abs(fromSquare.row - toSquare.row) + \
                abs(fromSquare.col - toSquare.col)

        if diff == 0 or diff > 2:
            return False

        return True

    def getMovePath(self, fromSquare, toSquare):
        return [fromSquare.position, toSquare.position]

    def isKingInCheck(self):
        return self.check

    def movePiece(self, fromSquare, toSquare):
        self.moved = True
        return True

class QueenPiece(Piece):

    def __init__(self, pieceColor):
        super(QueenPiece, self).__init__(pieceColor, PieceType.Queen)

    def isValidPieceMove(self, fromSquare, toSquare):
        rowMove = abs(fromSquare.row - toSquare.row)
        colMove = abs(fromSquare.col - toSquare.col)

        # Piece did not move
        if rowMove == 0 and colMove == 0:
            return False

        if (rowMove != colMove) and (rowMove != 0 and colMove != 0):
            return False

        return True

    def getMovePath(self, fromSquare, toSquare):
        fromPos = fromSquare.position
        toPos = toSquare.position

        diff = max(abs(toPos[1] - fromPos[1]), abs(toPos[0] - fromPos[0]))

        path = [fromPos]
        mulRow = mulCol = 1

        if fromPos > toPos:
            mulRow = mulCol = -1

        if toPos[0] == fromPos[0]:
            mulRow = 0
        if toPos[1] == fromPos[1]:
            mulCol = 0

        for i in xrange(1, diff + 1):
            path.append((fromPos[0] + mulRow * i, fromPos[1] + mulCol * i))

        return path

    def movePiece(self, fromSquare, toSquare):
        self.moved = True
        return True

class BishopPiece(Piece):

    def __init__(self, pieceColor):
        super(BishopPiece, self).__init__(pieceColor, PieceType.Bishop)

    def setSquare(self, square):
        super(BishopPiece, self).setSquare(square)
        self.squareColor = square.squareColor

    def isValidPieceMove(self, fromSquare, toSquare):
        if fromSquare.squareColor != toSquare.squareColor:
            return False

        rowMove = abs(fromSquare.row - toSquare.row)
        colMove = abs(fromSquare.col - toSquare.col)

        if rowMove != colMove or rowMove == 0:
            return False

        return True

    def getMovePath(self, fromSquare, toSquare):
        fromPos = fromSquare.position
        toPos = toSquare.position

        mulRow = mulCol = 1

        if fromPos > toPos:
            mulRow = mulCol = -1

        diff = abs(toPos[0] - fromPos[0])

        path = [fromPos]

        for i in xrange(1, diff + 1):
            path.append((fromPos[0] + mulRow * i, fromPos[1] + mulCol * i))

        return path

    def movePiece(self, fromSquare, toSquare):
        self.moved = True
        return True

class KnightPiece(Piece):

    def __init__(self, pieceColor):
        super(KnightPiece, self).__init__(pieceColor, PieceType.Knight)

    def isValidPieceMove(self, fromSquare, toSquare):
        fromPos = fromSquare.position
        toPos = toSquare.position

        rowDiff = abs(fromPos[0] - toPos[0])
        colDiff = abs(fromPos[1] - toPos[1])

        if (rowDiff == 1 and colDiff == 2) or (rowDiff == 2 and colDiff ==
                1):
            return True

        return False

    def getMovePath(self, fromSquare, toSquare):
        fromPos = fromSquare.position
        toPos = toSquare.position

        return [fromPos, toPos]

    def movePiece(self, fromSquare, toSquare):
        self.moved = True
        return True

class RookPiece(Piece):

    def __init__(self, pieceColor):
        super(RookPiece, self).__init__(pieceColor, PieceType.Rook)

    def isValidPieceMove(self, fromSquare, toSquare):
        fromPos = fromSquare.getPosition()
        toPos = toSquare.getPosition()

        rowDiff = abs(fromPos[0] - toPos[0])
        colDiff = abs(fromPos[1] - toPos[1])

        if (rowDiff == 0 and colDiff != 0) or (rowDiff != 0 and colDiff ==
                0):
            return True

        return False

    def getMovePath(self, fromSquare, toSquare):
        fromPos = fromSquare.getPosition()
        toPos = toSquare.getPosition()

        mulRow = mulCol = 1

        if fromPos > toPos:
            mulRow = mulCol = -1

        if fromSquare.row == toSquare.row:
            mulRow = 0
        if fromSquare.col == toSquare.col:
            mulCol = 0

        path = [fromPos]
        diff = max(abs(fromSquare.row - toSquare.row), (fromSquare.col -
            toSquare.col))

        for i in xrange(1, diff + 1):
            path.append((fromSquare.row + i * mulRow, fromSquare.col + i *
                mulCol))

        return path

    def movePiece(self, fromSquare, toSquare):
        self.moved = True
        return True

class PawnPiece(Piece):

    def __init__(self, pieceColor):
        super(PawnPiece, self).__init__(pieceColor, PieceType.Pawn)
        self.firstMove = True

    def isValidPieceMove(self, fromSquare, toSquare):
        raise NotImplementedError("PawnPiece subclasses should implement this" \
        "method")

    def _isValidPawnMove(self, fromPiece, toPiece, fromSquare, toSquare):

        if abs(toSquare.col - fromSquare.col) == 0:
            # Possible straight move
            move = abs(toSquare.row - fromSquare.row)
            if move > 2:
                return False
            if move == 2 and not self.firstMove:
                return False
        elif abs(toSquare.col - fromSquare.col) == 1 and abs(toSquare.row -
                fromSquare.row) == 1 and toPiece:
            # Check possible attack move
            if fromPiece.pieceColor == toPiece.pieceColor:
                return False
            print 'Pawn at location %s is attacking piece %s at' \
                    'location %s' %(self.fromPiece.square.position, \
                            self.toPiece.pieceType, self.toPiece.square.position)
        else:
            # Invalid move
            return False

        return True


    def movePiece(self, fromSquare, toSquare):
        self.moved = True
        self.firstMove = False

class WhitePawnPiece(PawnPiece):

    def __init__(self, pieceColor):
        super(WhitePawnPiece, self).__init__(pieceColor)

    def isValidPieceMove(self, fromSquare, toSquare):
        # White pawn moves only down
        fromPiece = fromSquare.piece
        toPiece = toSquare.piece

        # Cannot move up
        if toSquare.row <= fromSquare.row:
            return False

        return self._isValidPawnMove(fromPiece, toPiece, fromSquare,
                toSquare)

    def getMovePath(self, fromSquare, toSquare):
        if not self.isValidPieceMove(fromSquare, toSquare):
            raise ValueError('Invalid value for moves of fromSquare to' \
                'toSquare')

        #TODO: Check if move == 2 and return movepath
        return []

class BlackPawnPiece(PawnPiece):

    def __init__(self, pieceColor):
        super(BlackPawnPiece, self).__init__(pieceColor)

    def isValidPieceMove(self, fromSquare, toSquare):
        # Black pawn moves only up
        fromPiece = fromSquare.piece
        toPiece = toSquare.piece

        # Cannot move down
        if toSquare.row >= fromSquare.row:
            return False

        return self._isValidPawnMove(fromPiece, toPiece, fromSquare,
                toSquare)

    def getMovePath(self, fromSquare, toSquare):
        if not self.isValidPieceMove(fromSquare, toSquare):
            raise ValueError('Invalid value for moves of fromSquare to' \
                    'toSquare')

        return []

class PieceType(Enum):
    King = 0
    Queen = 1
    Bishop = 2
    Knight = 3
    Rook = 4
    Pawn = 5

class PieceColor(Enum):
    White = 0
    Black = 1

class PieceFactory(object):

    def __init__(self):
        return

    @staticmethod
    def createPiece(pieceColor, pieceType):
        if pieceType == PieceType.King:
            return KingPiece(pieceColor)
        elif pieceType == PieceType.Queen:
            return QueenPiece(pieceColor)
        elif pieceType == PieceType.Bishop:
            return BishopPiece(pieceColor)
        elif pieceType == PieceType.Knight:
            return KnightPiece(pieceColor)
        elif pieceType == PieceType.Rook:
            return RookPiece(pieceColor)
        else:
            if pieceColor == PieceColor.White:
                return WhitePawnPiece(pieceColor)
            else:
                return BlackPawnPiece(pieceColor)

    @staticmethod
    def createPieceWithPos(piecePos):
        row = piecePos[0]
        col = piecePos[1]

        if row < 2 or row > 5:
            if row < 2:
                # White pieces
                pieceColor = PieceColor.White
            else:
                # Black pieces
                pieceColor = PieceColor.Black

            if row == 1 or row == 6:
                return PieceFactory.createPiece(pieceColor, PieceType.Pawn)
            elif col == 0 or col == 7:
                return PieceFactory.createPiece(pieceColor, PieceType.Rook)
            elif col == 1 or col == 6:
                return PieceFactory.createPiece(pieceColor, PieceType.Knight)
            elif col == 2 or col == 5:
                return PieceFactory.createPiece(pieceColor, PieceType.Bishop)
            elif col == 3:
                return PieceFactory.createPiece(pieceColor, PieceType.Queen)
            else:
                return PieceFactory.createPiece(pieceColor, PieceType.King)

        return None
