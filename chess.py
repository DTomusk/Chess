class Board:
	def __init__(self):
		# place all the pieces at the start of the game 
		row0 = [Rook(True, [0,0]), Knight(True, [0,1]), Bishop(True, [0,2]), King(True, [0,3]), Queen(True, [0,4]), Bishop(True, [0,5]), Knight(True, [0,6]), Rook(True, [0,7])]
		row1 = []
		row2 = []
		row3 = []
		row4 = []
		row5 = []
		row6 = []
		row7 = [Rook(False, [7,0]), Knight(False, [7,1]), Bishop(False, [7,2]), King(False, [7,3]), Queen(False, [7,4]), Bishop(False, [7,5]), Knight(False, [7,6]), Rook(False, [7,7])]
		for i in range(8):
			row1.append(Pawn(True, [1,i]))
			row2.append(0)
			row3.append(0)
			row4.append(0)
			row5.append(0)
			row6.append(Pawn(False, [6,i]))
		self.grid = [row0, row1, row2, row3, row4, row5, row6, row7]
		self.game = True
		self.whiteScore = 0
		self.blackScore = 0	

	def display(self):
		for i in range(8):
			row = ''
			for j in range(8):
				current = self.grid[j][i]
				if isinstance(current, Piece):
					char = current.display
				else:
					char = '__'
				row = row + '|' + char + '|'
			print row

	def move(self, color):
		# legalMoves should be passed here with full certainty they're legal, all checks done in legalMoves
		legalMoves = []
		while len(legalMoves) == 0:
			x, y = input()
			if isinstance(self.grid[int(x)][int(y)], Piece):
				if self.grid[int(x)][int(y)].color == color:
					legalMoves = self.grid[int(x)][int(y)].getLegal(self)
				else:
					print "Wrong color"
				if len(legalMoves) ==  0:
					print "No legal moves"
			else: 
				print "No piece at: " + x + ", " + y
		print legalMoves
		# need to update position of pawn itself here 
		move = int(input())
		X = legalMoves[move][0]
		Y = legalMoves[move][1]
		if isinstance(self.grid[X][Y], Piece):
			if isinstance(self.grid[X][Y], King):
				self.game = False
			elif self.grid[X][Y].color == True:
				self.whiteScore += self.grid[X][Y].value
			else: 
				self.blackScore += self.grid[X][Y].value
		self.grid[X][Y] = self.grid[int(x)][int(y)]
		self.grid[X][Y].x = X
		self.grid[X][Y].y = Y
		self.grid[int(x)][int(y)] = 0

	# check whether a player is in check
	# need to check whether a move would result in check  
	# go through all tiles, all pieces, all moves to see if the king is under attack 
	def checkCheck(self, color):
		for i in range(8):
			for j in range(8):
				if isinstance(self.grid[i][j], Piece):
					if not(self.grid[i][j].color == color):
						legalMoves = self.grid[i][j].getLegal(self)
						for x in legalMoves:
							if isinstance(self.grid[x[0]][x[1]], King):
								if color == True:
									print "Black is in check"
								else:
									print "White is in check"
								return True
		return False


	@staticmethod
	def inBoard((x, y)):
		if x<=7 and x>=0 and y<=7 and y>=0:
			return True
		else:
			return False

	@staticmethod
	def isAlly(self, color, (x, y)):
		if isinstance(self.grid[x][y], Piece):
			if self.grid[x][y].color == color:
				return True
		return False

	@staticmethod
	def isEnemy(self, color, (x, y)):
		if isinstance(self.grid[x][y], Piece):
			if self.grid[x][y].color != color:
				return True
		return False

	@staticmethod
	def isEmpty(self, (x, y)):
		if not(isinstance(self.grid[x][y], Piece)):
			return True
		return False

class Piece(object):
	def __init__(self, color, position):
		self.color = color
		self.x = position[0]
		self.y = position[1]

	def getLegal(): 
		pass

class Pawn(Piece):
	def __init__(self, color, position):
		super(Pawn, self).__init__(color, position)
		if self.color == True:
			self.direction = 1
			self.starting = 1
			self.display = 'PB'
		else:
			self.direction = -1
			self.starting = 6
			self.display = 'PW'
		self.value = 1


	def getLegal(self, board):
		# could have some kind of modifier based on whether color is black or white 
		# direction is negative for whites
		# end of the board is 7 for black, 0 for white 
		# would essentially have to copy and paste all of black's code to get white 

		# want just one block of code that works for both black and white 
		legalMoves = []
		x = self.x
		y = self.y
		direction = self.direction

		# need to check that piece has space to move (isn't on the edge of the board)
		# there might be a more clever way of doing this but I don't really care too much 
		if Board.inBoard((x+direction, y)):
			# pawn can move one forward
			if Board.isEmpty(board, (x+direction, y)):
				legalMoves.append((x+direction, y))
				# pawn can move two forward if at starting position 
				if x == self.starting and Board.isEmpty(board, (x+2*direction, y)):
					legalMoves.append((x+2*direction, y))
			# pawn can take one space diagonally 
			if Board.inBoard((x+direction, y+1)):
				if Board.isEnemy(board, self.color, (x+direction, y+1)):
					legalMoves.append((x+direction, y+1))
			if Board.inBoard((x+direction, y-1)):
				if Board.isEnemy(board, self.color, (x+direction, y-1)):
					legalMoves.append((x+direction, y-1))

		return legalMoves

class King(Piece):
	# Kind doesn't need a special initialiser 
	def __init__(self, color, position):
		super(King, self).__init__(color, position)
		if self.color == True:
			self.display = 'KB'
		else:
			self.display = 'KW'

	def getLegal(self, board):
		legalMoves = []
		x = self.x 
		y = self.y

		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				if i != 0 or j != 0:
					if Board.inBoard((x+i, y+j)):
						if Board.isEmpty(board, (x+i, y+j)) or Board.isEnemy(board, self.color, (x+i, y+j)):
							legalMoves.append((x+i, y+j))

		return legalMoves

class Knight(Piece):
	def __init__(self, color, position):
		super(Knight, self).__init__(color, position)
		if self.color == True:
			self.display = 'NB'
		else:
			self.display = 'NW'
		self.value = 3

	def getLegal(self, board):
		legalMoves = []
		x = self.x 
		y = self.y 

		for i in [-2, 2]:
			for j in [-1, 1]:
				if Board.inBoard((x+i, y+j)):
					if Board.isEnemy(board, self.color, (x+i, y+j)) or Board.isEmpty(board, (x+i, y+j)):
						legalMoves.append((x+i, y+j))
				if Board.inBoard((x+j, y+i)):
					if Board.isEnemy(board, self.color, (x+j, y+i)) or Board.isEmpty(board, (x+j, y+i)):
						legalMoves.append((x+j, y+i))
		return legalMoves

class Rook(Piece):
	def __init__(self, color, position):
		super(Rook, self).__init__(color, position)
		if self.color == True:
			self.display = 'RB'
		else:
			self.display = 'RW'
		self.value = 5

	def getLegal(self, board):
		legalMoves = []
		x = self.x
		y = self.y

		direction = ((1,0),(-1,0),(0,1),(0,-1))

		for dire in direction:
			mod = 1
			while Board.inBoard((x+mod*dire[0], y+mod*dire[1])):
				potential = (x+mod*dire[0], y+mod*dire[1])
				if Board.isEnemy(board, self.color, potential) or Board.isEmpty(board, potential):
					legalMoves.append(potential)
					if Board.isEnemy(board, self.color, potential):
						break
					mod += 1
				else:
					break 
		return legalMoves

class Bishop(Piece):
	def __init__(self, color, position):
		super(Bishop, self).__init__(color, position)
		if self.color == True:
			self.display = 'BB'
		else:
			self.display = 'BW'
		self.value = 3

	def getLegal(self, board):
		legalMoves = []
		x = self.x 
		y = self.y

		direction = ((1,1),(-1,1),(1,-1),(-1,-1))

		for dire in direction:
			mod = 1
			while Board.inBoard((x+mod*dire[0], y+mod*dire[1])):
				potential = (x+mod*dire[0], y+mod*dire[1])
				if Board.isEnemy(board, self.color, potential) or Board.isEmpty(board, potential):
					legalMoves.append(potential)
					if Board.isEnemy(board, self.color, potential):
						break
					mod += 1
				else:
					break 
		return legalMoves

class Queen(Piece):
	def __init__(self, color, position):
		super(Queen, self).__init__(color, position)
		if self.color == True:
			self.display = 'QB'
		else: 
			self.display = 'QW'
		self.value = 9

	def getLegal(self, board):
		legalMoves = []
		x = self.x 
		y = self.y

		direction = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1))

		for dire in direction:
			mod = 1
			while Board.inBoard((x+mod*dire[0], y+mod*dire[1])):
				potential = (x+mod*dire[0], y+mod*dire[1])
				if Board.isEnemy(board, self.color, potential) or Board.isEmpty(board, potential):
					legalMoves.append(potential)
					if Board.isEnemy(board, self.color, potential):
						break
					mod += 1
				else:
					break 
		return legalMoves

def main():
	myBoard = Board()
	Board.display(myBoard)

	while myBoard.game == True:
		print "White move:"
		myBoard.move(False)
		Board.display(myBoard)
		myBoard.checkCheck(True)
		print "White score: " + str(myBoard.whiteScore)
		if myBoard.game == False:
			print "The whities win"
			break
		print "Black move:"
		myBoard.move(True)
		Board.display(myBoard)
		myBoard.checkCheck(False)
		print "Black score: " + str(myBoard.blackScore)
		if myBoard.game == False:
			print "Black wins"
			break

if __name__=="__main__":
	main()

# want to be able to play a full game with just pawns (or as close as possible) before adding other pieces
# that means refining the code that I have now, simplifying input 