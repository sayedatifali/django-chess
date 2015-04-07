class History(object):

    def __init__(self):
        self._killedPiece = []
        self._totalMoves = 0
        self._fromPosition = []
        self._toPosition = []

    def makeMove(self, fromPosition, toPosition, killedPiece):
        self._totalMoves += 1
        self._fromPosition.append(fromPosition)
        self._toPosition.append(toPosition)
        self._killedPiece.append(killedPiece)

    def canUndoLastMove(self):
        return self._totalMoves > 0

    def undoLastMove(self):
        if self._totalMoves == 0:
            print 'No moves to undo'
            return (None, None, None)

        self._totalMoves -= 1
        fromPosition = self._fromPosition.pop()
        toPosition = self._toPosition.pop()
        killedPiece = self._killedPiece.pop()
        return (fromPosition, toPosition, killedPiece)
